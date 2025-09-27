from math import radians, sin, cos, asin, sqrt
import h3
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd

EARTH_R = 6371000.0  # meters

def haversine_m(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2 * EARTH_R * asin(sqrt(a))

def h3_to_gdf(hexes):
    polys = []
    for h in hexes:
        # h3 v4 returns [(lat, lng), ...]
        boundary = h3.cell_to_boundary(h)
        poly = Polygon([(lng, lat) for (lat, lng) in boundary])
        polys.append({"h3": h, "geometry": poly})
    return gpd.GeoDataFrame(polys, crs="EPSG:4326")

def hexes_in_radius(center_lat, center_lon, radius_m, res):
    """
    Return GeoDataFrame of H3 hexes (resolution `res`) whose centroids fall
    within `radius_m` of (center_lat, center_lon). Uses h3 v4 API.
    """
    center_cell = h3.latlng_to_cell(center_lat, center_lon, res)

    # Expand outward in H3 "rings" until we've likely covered the radius,
    # then precisely filter by Haversine distance on centroids.
    k = 0
    cells = {center_cell}
    while True:
        k += 1
        cells |= set(h3.grid_disk(center_cell, k))
        gdf_tmp = h3_to_gdf(list(cells))
        centroids = gdf_tmp.geometry.centroid
        if len(centroids) == 0:
            continue
        dists = centroids.apply(lambda p: haversine_m(center_lat, center_lon, p.y, p.x))
        # stop when max centroid distance comfortably exceeds radius
        if dists.max() >= radius_m * 1.2 or k > 12:
            break

    gdf = h3_to_gdf(list(cells))
    gdf["centroid"] = gdf.geometry.centroid
    gdf["geo_dist_m"] = gdf["centroid"].apply(lambda p: haversine_m(center_lat, center_lon, p.y, p.x))
    out = gdf[gdf["geo_dist_m"] <= radius_m].drop(columns=["centroid", "geo_dist_m"]).reset_index(drop=True)
    return out

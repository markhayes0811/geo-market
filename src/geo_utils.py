from math import radians, sin, cos, asin, sqrt
import h3
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import geopandas as gpd
import pandas as pd

EARTH_R = 6371000.0  # meters

def haversine_m(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    return 2 * EARTH_R * asin(sqrt(a))

def hexes_in_radius(center_lat, center_lon, radius_m, res):
    center_hex = h3.geo_to_h3(center_lat, center_lon, res)
    # expand rings until the hex boundary extent exceeds radius; simple approach
    k = 1
    hexes = set([center_hex])
    while True:
        ring = set(h3.k_ring(center_hex, k))
        hexes |= ring
        gdf = h3_to_gdf(list(hexes))
        # quick check: keep only hexes whose centroid within radius
        center = Point(center_lon, center_lat)
        gdf["centroid"] = gdf.geometry.centroid
        gdf["dist"] = gdf["centroid"].distance(gpd.GeoSeries([center], crs='EPSG:4326').to_crs(3857).iloc[0])  # bogus in degrees; fix properly below
        # Instead compute geo distance centroid->center
        gdf["geo_dist_m"] = gdf["centroid"].apply(lambda p: haversine_m(center_lat, center_lon, p.y, p.x))
        if gdf["geo_dist_m"].max() > radius_m * 1.5 and k > 3:
            break
        k += 1
    # filter by true radius
    gdf["keep"] = gdf["geometry"].centroid.apply(lambda p: haversine_m(center_lat, center_lon, p.y, p.x) <= radius_m)
    return gdf[gdf["keep"]].drop(columns=["centroid","dist","geo_dist_m","keep"])

def h3_to_gdf(hexes):
    polys = []
    for h in hexes:
        boundary = h3.h3_to_geo_boundary(h, geo_json=True)  # list of (lat, lon)
        poly = Polygon([(lng, lat) for lat, lng in boundary])
        polys.append({"h3": h, "geometry": poly})
    return gpd.GeoDataFrame(polys, crs="EPSG:4326")

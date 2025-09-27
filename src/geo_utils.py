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
    center_hex = h3.latlng_to_cell(center_lat, center_lon, res)  # updated name
    k = 1
    hexes = set([center_hex])
    while True:
        ring = set(h3.grid_disk(center_hex, k))  # updated name
        hexes |= ring
        if k > 5:  # simple stop condition (you can refine with radius later)
            break
        k += 1
    return h3_to_gdf(list(hexes))

def h3_to_gdf(hexes):
    polys = []
    for h in hexes:
        boundary = h3.cell_to_boundary(h, geo_json=True)  # updated name
        poly = Polygon([(lng, lat) for lat, lng in boundary])
        polys.append({"h3": h, "geometry": poly})
    return gpd.GeoDataFrame(polys, crs="EPSG:4326")

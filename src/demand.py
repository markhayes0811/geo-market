import numpy as np
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from .geo_utils import haversine_m

def synthetic_demand_for_hexes(hex_gdf, seed=42):
    rng = np.random.default_rng(seed)
    # Simple, reproducible synthetic demand scaled by lat/lon to look spatial
    centroids = hex_gdf.geometry.centroid
    base = (centroids.y.values - centroids.y.mean())**2 + (centroids.x.values - centroids.x.mean())**2
    noise = rng.uniform(0.0, 1.0, len(hex_gdf))
    demand = (1.0 / (1.0 + base*50)) + 0.3 * noise
    df = hex_gdf.copy()
    df["demand"] = demand / demand.max()
    return df

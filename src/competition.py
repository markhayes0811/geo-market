import pandas as pd
from .geo_utils import haversine_m

def load_competitors(csv_path):
    df = pd.read_csv(csv_path)
    required = {"name","brand","lat","lon"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"competitors.csv missing columns: {missing}")
    return df

def competition_pressure_for_hexes(hex_gdf, competitors_df, decay_m=3000.0):
    # Sum of decayed proximity to all competitors (higher = more competition)
    centroids = hex_gdf.geometry.centroid
    pressures = []
    for p in centroids:
        lat, lon = p.y, p.x
        dists = competitors_df.apply(lambda r: haversine_m(lat, lon, r['lat'], r['lon']), axis=1)
        # exponential decay: exp(-d/decay)
        press = (dists.apply(lambda d: pow(2.718281828, -d/decay_m))).sum()
        pressures.append(press)
    out = hex_gdf.copy()
    m = max(pressures) if max(pressures) > 0 else 1.0
    out["competition"] = [p/m for p in pressures]
    return out

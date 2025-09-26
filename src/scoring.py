import pandas as pd

def score_sites(hex_with_demand_comp, weight_demand=1.0, weight_competition=1.0):
    df = hex_with_demand_comp.copy()
    # Higher demand is good, higher competition is bad
    df["site_score"] = weight_demand*df["demand"] - weight_competition*df["competition"]
    df = df.sort_values("site_score", ascending=False).reset_index(drop=True)
    return df

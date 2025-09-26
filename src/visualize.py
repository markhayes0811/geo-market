import folium
from folium.features import DivIcon
from branca.colormap import linear

def render_map(hex_scored_gdf, competitors_df, out_path_html="data/outputs/market_map.html", top_n=15):
    m = folium.Map(location=[hex_scored_gdf.geometry.centroid.y.mean(), hex_scored_gdf.geometry.centroid.x.mean()], zoom_start=10, tiles="cartodbpositron")
    # Color by score
    min_s, max_s = hex_scored_gdf["site_score"].min(), hex_scored_gdf["site_score"].max()
    cmap = linear.YlGnBu_09.scale(min_s, max_s)
    for _, row in hex_scored_gdf.iterrows():
        folium.GeoJson(row["geometry"].__geo_interface__,
                       style_function=lambda x, s=row["site_score"]: {"fillColor": cmap(s), "color": "#00000000", "weight": 0.5, "fillOpacity": 0.6}).add_to(m)
    # Competitors
    for _, r in competitors_df.iterrows():
        folium.CircleMarker(location=[r["lat"], r["lon"]], radius=5, popup=f"{r['brand']}: {r['name']}", tooltip=r["brand"]).add_to(m)
    # Labels for top candidates
    top = hex_scored_gdf.head(top_n).copy()
    for i, (_, r) in enumerate(top.iterrows(), start=1):
        c = r.geometry.centroid
        folium.Marker(location=[c.y, c.x], icon=DivIcon(icon_size=(150,36), icon_anchor=(0,0),
                     html=f'<div style="font-size:12px; font-weight:bold;">#{i}</div>'),
                     tooltip=f"Rank {i} — score {r['site_score']:.3f}").add_to(m)
    m.save(out_path_html)
    return out_path_html

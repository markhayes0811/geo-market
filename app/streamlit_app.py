import os
import pandas as pd
import geopandas as gpd
import streamlit as st
from src.config import CENTER_LAT, CENTER_LON, RADIUS_M, H3_RESOLUTION, WEIGHT_DEMAND, WEIGHT_COMPETITION, COMPETITION_DECAY_M, SEED
from src.geo_utils import hexes_in_radius
from src.demand import synthetic_demand_for_hexes
from src.competition import load_competitors, competition_pressure_for_hexes
from src.scoring import score_sites

st.set_page_config(page_title='Geo Market Insights', layout='wide')
st.title('Geo Market Insights — Site Selection')
st.caption('Hex-based scoring of new store locations (demand vs. competition)')

with st.sidebar:
    st.header('Parameters')
    radius_km = st.slider('Radius (km)', min_value=5, max_value=60, value=int(RADIUS_M/1000), step=5)
    res = st.slider('H3 Resolution', min_value=6, max_value=9, value=H3_RESOLUTION, step=1)
    w_d = st.slider('Weight — Demand', 0.0, 3.0, WEIGHT_DEMAND, 0.1)
    w_c = st.slider('Weight — Competition', 0.0, 3.0, WEIGHT_COMPETITION, 0.1)
    decay = st.slider('Competition Decay (m)', 500, 8000, int(COMPETITION_DECAY_M), 100)

hex_gdf = hexes_in_radius(CENTER_LAT, CENTER_LON, radius_km*1000, res)
dem = synthetic_demand_for_hexes(hex_gdf, seed=SEED)
competitors = load_competitors('data/inputs/competitors.csv')
comp = competition_pressure_for_hexes(dem, competitors, decay_m=decay)
scored = score_sites(comp, w_d, w_c)

st.write('Hexes:', len(scored))
st.dataframe(scored[['h3','demand','competition','site_score']].head(20))

st.download_button('Download ranked candidates (CSV)',
                   scored[['h3','demand','competition','site_score']].to_csv(index=False).encode('utf-8'),
                   file_name='candidates_ranked.csv',
                   mime='text/csv')
st.info('To see an interactive map, run the notebook pipeline in /notebooks which writes data/outputs/market_map.html')

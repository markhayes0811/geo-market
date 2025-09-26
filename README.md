# Geo Market Insights — Site Selection & Cannibalization Analysis

An **end-to-end, GitHub-ready project** (with a Google Colab notebook) that solves a real retail business problem:
> *“Where should we open the next store to maximize demand coverage while minimizing cannibalization from competitors (and ourselves)?”*

This repo builds a **hex-based (H3) market potential model** over an area (default: **25 miles around Wilmington, DE 19804**) using open data sources (e.g., OpenStreetMap) and simple demand proxies. It produces:
- A **ranked list of candidate locations**,
- An **interactive Folium map**,
- Reusable, modular Python code (`src/`),
- A **Colab notebook** to run the entire pipeline.

---

## Quick Start (Google Colab)

1. **Open the notebook** (Colab badge below) and run the first cell to install deps.
2. Upload or edit `data/inputs/competitors.csv` if you have your own competitors.
3. Run the notebook end-to-end to produce outputs in `data/outputs/` (maps & CSV).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/your-username/geo-market-insights/blob/main/notebooks/Geo_Market_Insights.ipynb)

> **Note:** If you're running the notebook directly from Colab and not from GitHub, just upload this repository (or mount Google Drive) so relative paths work as-is.

---

## Business Problem & Method

**Problem:** A retailer (e.g., grocery, pharmacy, coffee) wants to find **high-potential areas** for its next store while **avoiding cannibalization** by nearby competitors (and existing stores).

**Approach (lightweight & explainable):**
- Generate an **H3 hex grid** over the target radius.
- Estimate a **demand proxy** per hex (population density × income scale) via public APIs or provided defaults.
- Compute **competition pressure** using competitor/store proximity (Haversine distance with decay).
- Build a **site score = demand - competition** (with tunable weights).
- Rank top **candidate centroids**, and map them along with competitors and coverage.

**You can replace the demand proxy** with real data (Census ACS, mobile foot traffic, card-spend, etc.). The code is modular.

---

## Repo Layout

```
geo-market-insights/
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ .gitignore
├─ data/
│  ├─ inputs/
│  │  └─ competitors.csv     # sample competitors (ShopRite, Acme, ALDI, etc.)
│  └─ outputs/               # generated maps & CSVs (ignored by Git)
├─ notebooks/
│  └─ Geo_Market_Insights.ipynb  # Colab-ready end-to-end pipeline
├─ src/
│  ├─ config.py
│  ├─ geo_utils.py
│  ├─ demand.py
│  ├─ competition.py
│  ├─ scoring.py
│  └─ visualize.py
└─ app/
   └─ streamlit_app.py       # optional: run `streamlit run app/streamlit_app.py`
```

---

## Inputs

- `data/inputs/competitors.csv` — **Name, brand, lat, lon**. Replace with your list.

If you have **existing store** locations, add them to the same file with `brand=OurStore` (or edit `src/competition.py` to load from a second file).

---

## Outputs

- `data/outputs/candidates_ranked.csv`
- `data/outputs/market_map.html` (interactive map you can open in a browser)

---

## Extend / Customize

- Swap in **real demand** (Census/ACS): implement `get_demand_for_hexes()` with API calls.
- Use **travel-time** instead of straight-line distance (OSRM/Valhalla) in `competition.py`.
- Tune **weights** in `src/scoring.py`.
- Drop a **Streamlit** app with sliders for live tuning (`app/streamlit_app.py`).

---

## Colab Tips

- If running on Colab, the notebook includes:
  - `pip install` for requirements,
  - A working directory cell to clone/mount,
  - A **single-run pipeline** (no manual path edits needed).

---

## License

MIT — do what you want, attribution appreciated.

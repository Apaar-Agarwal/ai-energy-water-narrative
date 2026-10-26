# AI infrastructure: do electricity and water limits matter?
**Question:** Should electricity and water constraints limit the expansion of AI infrastructure?
**Persona:** A regional infrastructure planner deciding what evidence should inform approval of new data centres.

## Member 2 - Grid pressure
Ranked bars of data-centre share of electricity demand (IEA regions; US vs China vs rest), with year, measure,
location and planner-threshold interactions. Covers all data centres, not only AI.

## Run locally
```
pip install -r requirements.txt
python prepare_data.py --file data/raw/data-centers-share-electricity-demand.csv   # regenerates processed data
streamlit run app.py
```
## Data
Raw: `data/raw/` (OWID CSV, accessed 21 Oct 2026). Processed: `data/processed/grid_share.csv`. Regenerate with `prepare_data.py`.
Source: Our World in Data, from IEA "Energy and AI" and Ember "Yearly Electricity Data".

## Australia
AEMO-based spotlight tab: `data/processed/australia_aemo.csv`; sources in `data/raw/australia_sources.md`. Not like-for-like with OWID.

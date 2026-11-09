# Processed data

`owid_data_centres_share_clean.csv` is generated from `data/raw/data-centers-share-electricity-demand.csv` by `scripts/process_owid.py`.

Columns: `entity`, `code`, `year`, `share_pct` (percent of total electricity demand, values unchanged), `entity_clean` (" (IEA)" suffix removed for display), `entity_type` (Country / Region / Aggregate). Key: (entity, year). No values are filled, interpolated or rescaled; missing years stay missing.
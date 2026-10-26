# Water, before expansion

Standalone Streamlit dashboard for the individual water-stress contribution to Assignment 3. Built using the official WRI Aqueduct 4.0 country rankings workbook; no synthetic observations.

## Run locally

From this folder:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The processed data is included, so opening the app needs no data download. `Launch dashboard.cmd` starts the app using the current Python installation. Open the local URL printed by Streamlit. For a new environment, install requirements first.

## Question and audience

Group question: Should data-centre expansion supporting AI be assessed against local electricity and water constraints rather than global averages?

Dashboard question: Which countries face greater baseline water stress?

Persona: an infrastructure policy adviser deciding whether expansion guidelines should vary by location. National water indicators provide screening context; this dashboard cannot approve sites or attribute water consumption to AI.

## Three user stories

1. As an infrastructure policy adviser, I want to rank national baseline water-stress scores so that I can identify countries needing closer water assessment.
2. As an infrastructure policy adviser, I want to filter countries, regions and risk categories so that I can compare the locations used by the electricity dashboards.
3. As an infrastructure policy adviser, I want to trace a displayed number to the source workbook so that I can judge the evidence and its transformations.

## Contents

- `app.py`: standalone entry point.
- `water_dashboard.py`: reusable renderer and filtering function.
- `data/raw/aqueduct-4-0-country-rankings.zip`: unchanged official archive, CC BY 4.0.
- `data/raw/country_baseline_bws_tot.csv`: source sample with original spreadsheet fields and source Excel row.
- `data/processed/water_stress.csv`: app input.
- `data/metadata.json`: retrieval date, baseline, source URL and archive checksum.
- `scripts/prepare_data.py`: reproducible extraction/transform.
- `scripts/verify.py`: data and app interaction checks.
- `docs/`: dictionary, disclosure, AI provenance and recording guide.

## Regenerate and verify

```powershell
python scripts/prepare_data.py
python scripts/verify.py
```

The script reads the archive directly. It does not request current data, rescale scores or fill missing data. See the dictionary for exact transformations.

## Part 2 integration

Copy this folder into the shared repository as a module. Import `render_water_dashboard` and call it after the electricity sections:

```python
from water_dashboard import render_water_dashboard
render_water_dashboard(countries=selected_iso3_codes, key_prefix='water_story')
```

The optional country list removes the local country picker and uses the parent's shared selection. Files resolve relative to the module, not the current working directory. The standalone wrapper alone sets the Streamlit page configuration. If the group wants a shorter chapter, edit the renderer to move supporting verification panels to the shared methodology section.

The four-dashboard portfolio must still satisfy the final chart-family requirement. This contribution alone is one ranking chart, not the entire final portfolio.

## Deploy

Push this folder's contents to the group GitHub repository and deploy `app.py` with Streamlit Community Cloud, using the included requirements and data files. No secrets or live APIs are required. Deployment/publication has not been performed. Confirm public loading speed and record the assessed commit hash after deployment.

## Sources and interpretation

[WRI dataset](https://www.wri.org/data/aqueduct-40-country-rankings), [original archive](https://files.wri.org/aqueduct/aqueduct-4-0-country-rankings.zip), [country dictionary](https://github.com/wri/Aqueduct40/blob/master/data_dictionary_country-rankings.md), [technical note](https://doi.org/10.46830/writn.23.00061).

Citation: Kuzma et al. (2023), Aqueduct 4.0: Updated Decision-Relevant Global Water Risk Indicators, World Resources Institute. CC BY 4.0. Local source retrieval: 18 October 2026. Baseline: 1979–2019. This download contains 189 total-demand country/territory records, 164 with a valid baseline water-stress score and category; the remainder are preserved and excluded explicitly.

Important for the team: this country-baseline workbook contains water stress, drought and flood indicators, not a ready-made seasonal-variability column. The other water member must confirm an appropriate Aqueduct export before building the separate variability dashboard.

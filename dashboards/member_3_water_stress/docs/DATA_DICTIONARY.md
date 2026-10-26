# Data dictionary

## Official source

Organisation: World Resources Institute. Dataset: Aqueduct 4.0 Current and Future Country Rankings. Edition: 2023. [Source](https://www.wri.org/data/aqueduct-40-country-rankings). [Direct archive](https://files.wri.org/aqueduct/aqueduct-4-0-country-rankings.zip). Licence: CC BY 4.0. Retrieved: 2026-10-18. SHA-256 and exact workbook name are in `data/metadata.json`.

Coverage: country/political entities defined by the source's GADM borders; 1979–2019 baseline reference period. Latest year in baseline inputs: 2019, not an annual observation for every row. WRI release date: 2023-08-16. Local refresh means file retrieval only. Country score is a weighted aggregation of basin-level scores, not a direct national withdrawal percentage.

## Source archive and extracted sample

`data/raw/aqueduct-4-0-country-rankings.zip` retains the full workbook, including other sheets; only `country_baseline` is used. The full sheet's logical key is (gid_0, indicator_name, weight). Sample `data/raw/country_baseline_bws_tot.csv` selects indicator_name=bws, weight=Tot; its key is gid_0. Both are regenerated/read by `scripts/prepare_data.py`.

| Original column | Meaning / units |
|---|---|
| gid_0 | Source ISO A3 / political-entity identifier; string |
| name_0 | Source country/political-entity name |
| indicator_name | Indicator code; bws = baseline water stress |
| weight | Tot = total gross water demand weighting |
| score | Demand-weighted indicator score; dimensionless 0–5 when valid |
| score_ranked | WRI ranking within indicator and weight; 1 is highest risk; ties may have fractional ranks |
| cat | Source category code 0–4; negative/special/missing codes are not ordinary scores |
| label | Source category description; preserve verbatim |
| un_region | UN region grouping |
| wb_region | World Bank region grouping |
| source_excel_row | Added provenance locator: Excel row in country_baseline, header is row 1 |

## Processed app dataset

File: `data/processed/water_stress.csv`. Primary key: iso3. One row per country/political entity in the total-demand baseline water-stress selection. Same time coverage as source. No future data or time-series interpolation.

| Column | Source / transformation |
|---|---|
| iso3 | gid_0 renamed; used for group-app joins, subject to matching code definitions |
| country | name_0 renamed |
| indicator_name, weight | Source codes retained |
| stress_score | score renamed and parsed as numeric; no scaling |
| source_rank | score_ranked renamed, not recalculated after filters |
| category_code | cat renamed |
| risk_category | label renamed; no category thresholds inferred |
| region | un_region renamed |
| wb_region | Unchanged |
| source_excel_row | Preserved source locator |
| has_score | True only if score is in [0,5] and category code in [0,4]; missing/special values retained but not plotted |

The transform preserves source values (including missing/special codes) and sorts by country. Display rounds chart scores to two decimals; table and verification use four decimals. KPI counts include only has_score=True. High/extremely-high count uses category_code >=3 among valid rows. Filtered min/max use valid selected rows. Chart row limit affects only the plot; the table and download include the full filtered selection.

Regeneration: run `python scripts/prepare_data.py` from the dashboard folder. pandas and openpyxl are required. Archive is the reproducible input; source sample and processed CSVs are derived outputs. The retrieval date is recorded for the included archive and must be updated honestly if replacing that source file.

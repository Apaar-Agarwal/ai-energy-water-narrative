# Data dictionary – Member 4 (water stress vs drought / flood risk)

## D4.1 Source: WRI Aqueduct 4.0 Country Rankings – `country_baseline` sheet

| Field | Entry |
|---|---|
| Files | `data/source/Aqueduct40_rankings_download_Y2023M07D05.xlsx` (original download, unchanged)<br>`data/source/aqueduct40_country_baseline.csv` (source sample: sheet `country_baseline` exported unchanged by `scripts/m4_extract_source_sample.py`) |
| Publisher | World Resources Institute (WRI) |
| URL | https://www.wri.org/data/aqueduct-40-country-rankings |
| Citation | Kuzma, S. et al. 2023. *Aqueduct 4.0: Updated decision-relevant global water risk indicators.* Technical Note. WRI. doi.org/10.46830/writn.23.00061 |
| Licence | Creative Commons, as listed on the WRI page. **Confirm the exact version (WRI open data is usually CC BY 4.0) before submission.** |
| Release / version | File dated 5 July 2023 (`Y2023M07D05`); WRI page published 16 Aug 2023 |
| Downloaded | 22 Oct 2026 (confirm) |
| Time coverage | Hydrological baseline 1979–2019, one value per country (no time series) |
| Latest observation | 2019 (end of the baseline period) |
| Grain / primary key | `gid_0` + `indicator_name` + `weight` (checked unique: 2,456 rows, 0 duplicates) |
| Coverage | 192 countries (GADM 3.6 codes) |
| Missing values | Sentinel `-9999` in `score` and `cat`, `label` = `NoData` |

| Column | Type | Unit / values | Description |
|---|---|---|---|
| gid_0 | text | ISO 3166-1 alpha-3 | Country code (GADM) |
| name_0 | text | – | Country name. Some names are mis-encoded in the source (e.g. `CÃ´te d'Ivoire`); 3 are blank (KIR, MCO, MHL) |
| indicator_name | text | `bws`, `drr`, `rfr` | Baseline water stress, drought risk, riverine flood risk |
| weight | text | `Tot`, `Dom`, `Ind`, `Irr`, `Liv`, `One`, `Pop` | Weighting used to aggregate to country: total / domestic / industrial / irrigation / livestock demand, one-weight (unweighted), population (rfr only) |
| score | number | 0–5 score (unitless) | Indicator score; `-9999` = NoData |
| score_ranked | number | rank | Country rank for that indicator/weight (ties shared) |
| cat | integer | 0–4; `-9999` | Risk category; checked equal to min(floor(score), 4) |
| label | text | e.g. `Low (<10%)` | Category label with raw thresholds |
| un_region | text | – | UN region |
| wb_region | text | – | World Bank region |

Category thresholds (taken from the `label` column):

| cat | bws (withdrawals ÷ renewable supply) | drr (raw index 0–1) | rfr (population affected per year) |
|---|---|---|---|
| 0 | Low (<10 %) | Low (0.0–0.2) | Low (0 to 2 in 1,000) |
| 1 | Low-Medium (10–20 %) | Low-Medium (0.2–0.4) | Low-Medium (2 to 4 in 1,000) |
| 2 | Medium-High (20–40 %) | Medium (0.4–0.6) | Medium-High (4 to 8 in 1,000) |
| 3 | High (40–80 %) | Medium-High (0.6–0.8) | High (8 in 1,000 to 1 in 100) |
| 4 | Extremely High (>80 %) | High (0.8–1.0) | Extremely High (>1 in 100) |

## D4.2 Processed: `data/processed/m4_water_stress_drought.csv`

| Field | Entry |
|---|---|
| Produced by | `python scripts/m4_process.py` (reads D4.1 CSV only) |
| Grain / primary key | `iso3` (one row per country, 192 rows, checked unique) |
| Time coverage / latest obs. | As D4.1: 1979–2019 baseline |
| Read by | `dashboards/m4_stress_vs_drought.py` |

| Column | Type | Unit | Description |
|---|---|---|---|
| iso3 | text | ISO3 | From `gid_0` |
| country | text | – | From `name_0`, encoding repaired; blank → ISO3 |
| un_region, wb_region | text | – | Unchanged |
| bws_score | number | 0–5 score | Baseline water stress, weight `Tot`; missing if NoData (28 countries) |
| bws_cat, bws_label | int / text | 0–4 | Category and label |
| drr_score | number | 0–5 score | Drought risk, weight `Tot`; missing if NoData (54 countries) |
| drr_cat, drr_label | int / text | 0–4 | Category and label |
| rfr_score | number | 0–5 score | Riverine flood risk, weight `Pop`; missing if NoData (28 countries) |
| rfr_cat, rfr_label | int / text | 0–4 | Category and label |
| low_stress_elevated_drought | boolean | – | `bws_score < 2` AND `drr_score >= 2`; missing if either score missing |

**Transform (T1–T5, with checks C1–C3 that stop the script on failure):**

1. T1: keep rows `bws/Tot`, `drr/Tot`, `rfr/Pop`; drop other weights.
2. T2: replace `-9999` with missing. It is never replaced with 0, because a 0 score means Low risk.
3. T3: pivot to one row per country.
4. T4: add the `low_stress_elevated_drought` flag (thresholds are the source's own category boundaries at score 2).
5. T5: repair mis-encoded names (UTF-8 read as Latin-1); blank names fall back to ISO3.
6. Scores are kept at full source precision; the app rounds to 2 d.p. for display only.
7. C1: the source key is unique. C2: `cat == min(floor(score), 4)` for every non-missing row. C3: scores lie in 0–5.

Result: 138 countries have both bws and drr; 164 have both bws and rfr.

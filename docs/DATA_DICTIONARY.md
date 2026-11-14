# Integrated data dictionary

## 1. OWID electricity source

- File: `data/raw/data-centers-share-electricity-demand.csv`. Key: (Entity, Year).
- Source: https://ourworldindata.org/grapher/data-centers-share-electricity-demand. Original providers IEA / Ember. Snapshot supplied by Brighty; source log retrieval 18 October 2026. Sanjai separately reports checking metadata on 21 October.
- Licence: OWID-authored work CC BY 4.0; underlying provider conditions apply. The linked IEA Energy and AI data product is explicitly Non-CC even though the separate reports are CC BY 4.0. See THIRD_PARTY_NOTICES.md for the source-specific distinction and public-release limitation.
- Coverage: ten entities, only two individual countries (CHN/USA), six regions, World and World excluding US/China. Observation years 2020, 2023–2025; latest observation 2025. No 2021/2022 observations and no future projections in the snapshot.
- Columns: Entity (source name), Code (country/OWID code, missing for regions), Year (calendar year), final indicator column (data-centre share of total electricity demand, percent; already multiplied by 100).

## 2. WRI Aqueduct country workbook

- File: `data/raw/Aqueduct40_rankings_download_Y2023M07D05.xlsx`; app uses only `country_baseline` sheet. Key: (gid_0, indicator_name, weight).
- Source: https://www.wri.org/data/aqueduct-40-country-rankings. Dictionary: https://github.com/wri/Aqueduct40/blob/master/data_dictionary_country-rankings.md. CC BY 4.0. Harsh note says downloaded 22 October 2026; this is a member-reported date, not an independently logged download. Archive filename date 5 July 2023; WRI page publication 16 August 2023.
- Coverage: 192 country/political entities in source sheet. Water-stress reference period 1979–2019, Aqueduct 4.0 edition. Drought/flood indicators are inherited Aqueduct 3.0. The Aqueduct 4.0 technical note identifies drought risk as 2000–2014 (p.23), and riverine flood risk as a 2010 baseline with FLOPROS protection input dated 2016 (p.19). These are model/reference vintages, not annual observations. There is no single latest observation year for all three indicators. None is live/current drought data.
- Columns: gid_0 (ISO A3/political key), name_0 (source name), indicator_name (bws water stress / drr drought / rfr riverine flood), weight (Tot, Dom, Ind, Irr, Liv, Pop, One), score (dimensionless score, usually 0–5, -9999 NoData), score_ranked (source rank, possible ties), cat (source category code, -9999 NoData), label (source category text), un_region (UN region), wb_region (World Bank region).
- Selected pairs: bws/Tot and drr/Tot (total water-demand weighting), rfr/Pop (population weighting). Equal scores across indicators are not equal physical impacts; national weighted scores cannot be read as measured national withdrawal percentages.
- Citation: Kuzma et al. (2023), Aqueduct 4.0: Updated Decision-Relevant Global Water Risk Indicators, WRI, https://doi.org/10.46830/writn.23.00061.

## Regenerated app inputs

Source checksums are recorded in `story_metadata.json`. No network requests.

### story_electricity.csv

Key: (entity, year); same coverage/units as OWID. source_csv_row added (1-based file row including header), Entity→entity, Code→iso3, Year→year, sole numeric indicator→share_pct. name strips trailing '(IEA)' for display. entity_type: Aggregate if source entity starts World; otherwise Country for three-character codes; Region otherwise. Sort entity/year. No interpolation, scaling, imputation or source-value edits.

### story_water.csv

Key: iso3; same national coverage as workbook. iso3←gid_0, country←name_0 (repair UTF8-as-Latin1 display encoding; blank falls back to ISO3), region←un_region, wb_region unchanged. Each prefix bws/drr/rfr has score, cat, label and source_excel_row columns. Prefix score/category -9999→missing, label retained. Select weight pairs above; left-join to national ID list, validate one-to-one. source_excel_row is 1-based sheet row including header. Sort country. No score rescaling. Missing pairs remain missing.

### story_country_baseline_sample.csv

Under `data/raw`, derived sample from unchanged workbook sheet with added source_excel_row. Every other column preserved. Logical key identical to source sheet. Regenerated with app datasets to permit on-screen source inspection; original workbook remains authoritative.

### grid_share.csv

Compatibility output for Sanjai's shared grid-share data: location←entity, code←iso3, year, share_pct. Same key, units, coverage and values as story_electricity. No Australia rows added.

### story_metadata.json

Build description, local integration refresh 26 October 2026, teammate-supplied source-retrieval notes, reference-period caveat, source SHA-256 checksums and row counts. Integration refresh is not a new source retrieval or observation date.

## On-screen calculations

- Opening world share: latest-year Entity=World row. Country coverage: count unique valid Country ISO3 codes.
- Electricity change: share(selected year) − share(2020), in percentage points; not relative growth. Both values from same source snapshot. Year 2020 compares to itself and yields zero.
- Comparison maximum and world reference are calculated from selected view and full-year World row respectively; regional/country values never summed.
- User threshold compares share >= chosen percent; no claim of official limit.
- Water min/max: valid selected bws scores only.
- Whole-file low-stress extra-risk count: valid paired scores; bws<2 and other score>=2. Denominator is valid paired records with bws<2. These are score thresholds, not asserted national raw-indicator thresholds.
- Scatter background uses all paired countries when context enabled; selected diamonds carry shared/expanded selections. Every plotted pair appears in a table.
- Synthesis is a left join by iso3; missing country electricity remains blank, not a regional substitute. Selected electricity year appears in header. Different reference periods remain explicit.
- Display values rounded; source and processed CSVs retain precision. No AI-generated numerical observations.

## Retained individual datasets

Brighty's tidy OWID CSV and script remain under contributors/Brighty plus their original shared paths; documentation in docs/source_log.md. Harsh's one-row-per-country CSV/source sample/scripts remain under contributors/Harsh and shared data/docs paths; fields documented in docs/m4_data_dictionary.md. Apaar's archive/sample/processed data and detailed dictionary remain under contributors/Apaar. These are preserved contribution evidence; the narrative reads only story files generated above. Sanjai's manually compiled AEMO file and source notes are archived under contributors/Sanjai, not read by the narrative; do not treat their inclusion as verification of their claims or an additional comparable app dataset.

## Preserved electricity member output

`data/processed/owid_data_centres_share_clean.csv` and `contributors/Brighty/data/processed/owid_data_centres_share_clean.csv` are identical derived OWID data. Source, source URL, licence, 2020/2023-2025 coverage and latest observation 2025 are as section 1. Primary key: (entity, year). `scripts/process_owid.py` renames Entity->entity, Code->code, Year->year, the numeric percentage column->share_pct, strips the display suffix into entity_clean and classifies entity_type. All text/code fields are dimensionless; year is calendar year and share_pct is percent. No interpolation or numerical rescaling.

`contributors/Sanjai/submission_materials/us_raw_row.csv` is a full 40-row copy of the OWID source, despite its filename. Its schema, key, units, coverage, licence and source URL are section 1; it is not a one-row independent US dataset.

## Preserved water member outputs

Harsh's processed files in root data/processed and contributors/Harsh/data/processed contain the same 192 country records. Source, licence and indicator-specific time coverage are section 2; primary key iso3. Columns and transforms are in m4_data_dictionary.md (corrected 14 November 2026). Latest reference inputs differ by indicator: stress ends 2019, drought ends 2014, riverine flood baseline 2010 plus 2016 protection input. No time series is implied.

Apaar's `contributors/Apaar/data/raw/country_baseline_bws_tot.csv` has 189 source selection rows, key gid_0. It selects bws/Tot from the same WRI country_baseline sheet and adds source_excel_row. Its `data/processed/water_stress.csv` has key iso3 and 189 rows, including 164 valid scores; it renames source columns and adds has_score, with no score rescaling. All columns, units and transforms: ../contributors/Apaar/docs/DATA_DICTIONARY.md. Source URL/licence are section 2; period 1979-2019, latest baseline input 2019. The saved ZIP is the original WRI archive, not a separate numerical source.

Unconsumed sheets embedded in the WRI workbook/archive remain source material, not inputs to the narrative. Their baseline/future and country/provincial schemas are defined in the linked WRI country-rankings dictionary; no projections or provincial observations are read, transformed or displayed by this app.

## Archived Australia/AEMO supporting dataset

File: `contributors/Sanjai/submission_materials/australia_aemo.csv` (8 rows). This is a member-supplied manual transcription kept as historical contribution evidence; it is NOT read by the integrated app and is not added to the OWID comparison. Source URLs are recorded per row in url, with details in australia_sources.md beside the file.

- Publisher/source: AEMO 2025 Inputs, Assumptions and Scenarios Report; AEMO 2026 ESOO; 2026 Digital demand surge news update; 2026 ISP. These are different editions/scopes/denominators, not one comparable time series.
- Source URLs: https://www.aemo.com.au/newsroom/news-updates/digital-demand-surge ; https://www.aemo.com.au/newsroom/media-release/2026-esoo ; https://aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp/2026-integrated-system-plan-isp ; the full IASR PDF URL is retained in each relevant row.
- Licence/conditions: AEMO copyright with its general permission for accurately attributed AEMO Material, subject to the stated exclusions. This is not described as CC BY. Policy: https://www.aemo.com.au/privacy-and-legal-notices/copyright-permissions (reviewed 14 November 2026).
- Primary key: (label, publication, scope, scenario), unique within the saved eight-row table. sort_key alone is NOT unique.
- Time coverage: mixed financial-year estimates from 2024-25 and 2025-26, a mid-2026 present-day estimate, and forecasts to 2050. Latest non-forecast reference: mid-2026/2025-26, not the end of the forecast horizon. Publication editions span 2025-2026.
- Transform: hand-entered/transcribed by the contributor from cited publications; numeric sorting helper added, scope/scenario and chart-inclusion flags recorded. No shared regeneration script creates these manually compiled observations. They are excluded from the reproducible app pipeline; no verification of all archived numerical claims is asserted by this release review.

| Column | Type / units | Definition |
|---|---|---|
| label | text | Financial year, calendar year or dated snapshot label; includes scenario qualifiers |
| sort_key | number / year ordering helper | Approximate display order; not an observation date or unique key |
| consumption_twh | number / TWh | Reported electricity use or forecast; blank means not supplied |
| share_pct | number / percent | Reported share using the row-specific denominator; blank is not zero |
| status | text | estimate or forecast |
| scenario | text | Reported scenario or n/a |
| publication | text | Source publication/edition |
| evidence | text | Contributor's primary/secondary attribution flag |
| scope | text | Geographic/system scope, e.g. NEM; not interchangeable with all Australia |
| denominator | text | Electricity basis used for the reported share |
| url | text / URL | Row-specific source link |
| in_chart | text / yes-no | Original standalone dashboard choice; not an inclusion flag for the integrated app |
| note | text | Contributor's source/interpretation caveat |

## Complete packaged CSV inventory

Every numerical CSV is listed below. Duplicate member snapshots inherit the corresponding source definitions above; they are not counted as independent sources. AI_PROVENANCE.csv files are administrative declarations (their seven-column schema is the assignment's matrix), not numerical datasets. JSON metadata supplies hashes/refresh notes and does not introduce numerical observations.

| File | Rows | Source/schema family |
|---|---:|---|
| `contributors/Apaar/data/processed/water_stress.csv` | 189 | Apaar processed stress above |
| `contributors/Apaar/data/raw/country_baseline_bws_tot.csv` | 189 | WRI country_baseline, section 2; added row locator where present |
| `contributors/Brighty/data/processed/owid_data_centres_share_clean.csv` | 40 | OWID member output above |
| `contributors/Brighty/data/raw/data-centers-share-electricity-demand.csv` | 40 | OWID original, section 1 |
| `contributors/Harsh/data/processed/m4_water_stress_drought.csv` | 192 | Harsh processed water; m4_data_dictionary.md |
| `contributors/Harsh/data/raw/aqueduct40_country_baseline.csv` | 2456 | WRI country_baseline, section 2; added row locator where present |
| `contributors/Sanjai/submission_materials/australia_aemo.csv` | 8 | Archived AEMO table above |
| `contributors/Sanjai/submission_materials/us_raw_row.csv` | 40 | OWID original, section 1 |
| `data/processed/grid_share.csv` | 40 | grid_share.csv above |
| `data/processed/m4_water_stress_drought.csv` | 192 | Harsh processed water; m4_data_dictionary.md |
| `data/processed/owid_data_centres_share_clean.csv` | 40 | OWID member output above |
| `data/processed/story_electricity.csv` | 40 | story_electricity.csv above |
| `data/processed/story_water.csv` | 192 | story_water.csv above |
| `data/raw/aqueduct40_country_baseline.csv` | 2456 | WRI country_baseline, section 2; added row locator where present |
| `data/raw/data-centers-share-electricity-demand.csv` | 40 | OWID original, section 1 |
| `data/raw/story_country_baseline_sample.csv` | 2456 | WRI country_baseline, section 2; added row locator where present |

The OWID original numeric column is named `Share of total electricity demand coming from data centers`; its unit is percent. No source values or archived member CSVs were changed by this documentation review.

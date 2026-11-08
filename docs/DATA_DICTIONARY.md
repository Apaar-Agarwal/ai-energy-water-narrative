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

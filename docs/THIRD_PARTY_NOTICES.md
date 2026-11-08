# Third-party sources and reuse notes

Source review: 6 November 2026. Source snapshots were supplied earlier by members and have not been replaced by live downloads.

## Water

Source: WRI Aqueduct, Aqueduct 4.0 Country Rankings (2023), CC BY 4.0.
https://www.wri.org/data/aqueduct-40-country-rankings
https://github.com/wri/Aqueduct40/blob/master/data_dictionary_country-rankings.md
Citation: Kuzma et al. (2023), doi:10.46830/writn.23.00061.
Changes: indicator/weight selection, national pivot, sentinel-to-missing conversion, display-name repair, derived counts and team visualisations. No endorsement implied.
Technical note: https://files.wri.org/d8/s3fs-public/2023-08/aqueduct-40-technical-note.pdf
Water stress baseline 1979–2019; drought risk 2000–2014 (p.23); riverine flood risk 2010 baseline, protection input 2016 (p.19). These indicators have different reference vintages. Neither annual electricity-year matching nor causal timing is implied.

## Electricity

Source: International Energy Agency (2025, 2026) and Ember (2026), with major processing by Our World in Data.
https://ourworldindata.org/grapher/data-centers-share-electricity-demand
Ember: https://ember-energy.org/creative-commons/ (CC BY 4.0).
IEA 2025 report: https://www.iea.org/reports/energy-and-ai (CC BY 4.0).
IEA 2026 report: https://www.iea.org/reports/key-questions-on-energy-and-ai (CC BY 4.0, subject to exclusions).
IMPORTANT: OWID also links the IEA data product https://www.iea.org/data-and-statistics/data-product/energy-and-ai, which is explicitly licensed under Non-CC terms. A report's CC licence does not establish the separate data product's licence.
https://www.iea.org/terms/terms-of-use-for-non-cc-material

The source/licence review is complete as a factual review; unrestricted public redistribution is NOT established. Keep this full source-data package local to the authorised review workflow until the team establishes permission or replaces the affected series with demonstrably open equivalents. The IEA terms distinguish graphic use from downloadable/manipulable data. The current app offers downloadable tables and the project includes source CSVs, so citation alone does not settle this issue. Do not label the complete project or electricity data CC BY. No legal conclusion or permission is claimed here.

Team changes: renamed columns, classified geography, added row locators, calculated percentage-point change and produced charts. Original values are preserved. No underlying IEA dataset has been newly downloaded in this review. The app is an educational screening narrative, not an IEA-endorsed decision tool.

## Archived contributions

Original member snapshots and AEMO supporting material are historical evidence. They are not additional verified app sources or independently relicensed works. Public release must account for these files as well. Source rights are not overridden by packaging or a repository licence.

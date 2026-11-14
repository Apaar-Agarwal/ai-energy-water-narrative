> Deployed Part 2 portfolio, 14 November 2026. All four individual contributions are included.

# Powering AI: why location matters

**Question:** Should data-centre expansion supporting AI be assessed against local electricity and water constraints rather than global averages?

**Persona:** an infrastructure policy adviser deciding whether expansion guidelines should vary by location. The app supports national/regional screening, not approval of individual sites.

## Run the local integration

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.port 8511
```

The app opens at http://localhost:8511. It reads packaged local CSVs and needs no live data API. Original individual water app remains on port 8510 if running. The shared app is deployed from the repository's `main` branch.

## Guided investigation frontend

The active frontend is `frontend.py`, entered from `app.py`. Follow one US/China profile in a persistent sidebar. Country-bar clicks update that profile and its downstream evidence; the year slider updates the electricity views. Compare share or percentage-point change, state an optional working hypothesis, then follow the water evidence. All four charts render on initial load; no click is needed to reveal them. Water-stress comparison defaults to Ireland as an explicitly water-only counterexample; the additional-risk scatter can be filtered to the blind-spot zone and switched to riverine flood risk. The final country brief offers a choice of evidence to request next, not an approval verdict.

Tables are in expanders to keep the narrative readable. Palette, typography, narrative transitions and a sidebar evidence rail unify the four contributions. Exact values are available without hover. `story.py` retains common loading/evidence functions and previous chapter renderers for reference; the current frontend does not use the old four-section layout.

## Three user stories

1. As an infrastructure policy adviser, I want to compare data-centre electricity-demand shares across places so that I can identify where demand is relatively significant. Walkthrough: sidebar country/year → clickable country bars or regional context.
2. As an infrastructure policy adviser, I want to examine change, water stress and drought risk so that I can identify additional resource constraints. Walkthrough: trajectory toggle → working hypothesis → water evidence → water-only comparison and extra-risk filter; the persistent matched country remains selected.
3. As an infrastructure policy adviser, I want to inspect sources, transformations and limitations so that I can judge whether the evidence supports location-specific guidelines. Walkthrough: conclusion → source-record inspector → methods/disclosure.

## One story, four contributions

| Chapter | Contribution | Integration |
|---|---|---|
| 1 | Brighty, electricity comparison | Ranked bars, world reference, year controls; geographic levels kept separate; claims computed from selected data |
| 2 | Sanjai, grid pressure/change | Change-from-2020 logic and illustrative threshold, adapted to a time-series chart with table; no fabricated annual observations |
| 3 | Apaar, baseline water stress | National stress-score ranking, source trace, dimensionless units and missing-value handling |
| 4 | Harsh, stress versus drought / riverine flood | Scatter, contextual countries, paired-data denominator and extra-risk indicator toggle |

No four-tab wrapper: chapters appear in one vertical narrative, with transitions and a combined answer. Sources are contextual rather than a synchronized causal model.

## Coverage decisions

- OWID snapshot has 40 rows: 10 entities at 2020, 2023, 2024 and 2025. Only US and China are individual countries; six IEA regions and two aggregates are not additional countries. Shared country comparison therefore uses US/China. Other water countries are available under an explicitly separate exploration mode.
- The water package has 192 entities, including 164 valid baseline water-stress scores. Drought and flood have separate missingness. All paired statistics use records with both indicators present.
- Water stress: Aqueduct 4.0, 1979–2019 baseline. Drought/flood are inherited Aqueduct 3.0 indicators with their own reference periods; the app does not call them current drought or assign 1979–2019 to every measure.
- Scores are weighted national aggregates, not literal national withdrawal ratios. Thresholds classify scores rather than asserting a physical national percentage. No combined sustainability score or site approval verdict.
- Sanjai's AEMO material is retained under `contributors/Sanjai/submission_materials/`. It mixes reporting editions, scopes and years, expands the agreed two-dataset scope, and is not merged into the OWID comparison. Its source claims require primary-source verification before adding a separate chapter.

## Source and processing

The packaged source data and processed outputs are retained in the project folders. Source definitions, field mappings and reference-period caveats are described in `docs/DATA_DICTIONARY.md` and `docs/INTEGRATION_REPORT.md`.

Individual teammate snapshots are retained under `contributors/{Apaar,Brighty,Harsh,Sanjai}/`, including scripts, individual documentation and submitted archives. Apaar's standalone contribution is under `contributors/Apaar/`. These originals document contribution history; they are not imported as side-effectful standalone apps in the final narrative. The integration source map is in `docs/BRANCH_SOURCES.json`.

## Deployment and submission

Live app: https://powering-ai-energy-water.streamlit.app/
Repository: https://github.com/Apaar-Agarwal/ai-energy-water-narrative
Entry point: root app.py. Cloud Python: 3.14. Requirements: requirements.txt.

Submit one PDF per group by Friday 20 November 2026, 11:59 pm. It must contain the live app URL, repository URL and full assessed commit or release tag. All supporting files are in this repository at that revision. The PDF is supplied separately for Canvas; do not submit a ZIP in its place.

Peer contribution factors: Apaar 1.0, Brighty 1.0, Sanjai 1.0, Harsh 1.0, declared as equal contribution by Apaar on behalf of the group on 14 November 2026. See docs/PEER_CONTRIBUTIONS.md.

Use the revision in the final PDF as the assessed version. Any subsequent code change requires updating that revision and checking the deployment. Source notices remain in docs/THIRD_PARTY_NOTICES.md. Sanjai's existing personal verification entry is preserved unchanged at Apaar's request; it has not been strengthened by inventing a check.

## Reproduce and verify

```text
python scripts/verify_integration.py
```

This runs source-equality checks, member-water comparisons, repeated builds, cross-platform newline checks and app interactions. Source data is packaged locally; no live API is required. `--shared-only` is retained for checking an intentionally partial copy, but the full assessed repository uses the strict default command.

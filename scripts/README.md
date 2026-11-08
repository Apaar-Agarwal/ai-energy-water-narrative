# Preparation and verification

- build_story_data.py: offline integrated build, original-source validation, sample/processed outputs and metadata.
- verify_integration.py: source equality, member comparisons, deterministic rebuild and initial four-chart/interaction tests.
- process_owid.py: Brighty's original tidy preparation; run from project root.
- m4_extract_source_sample.py and m4_process.py: Harsh's scripts with working paths corrected to data/raw. Originals retained under contributors/Harsh.

Run python scripts/verify_integration.py after installing root requirements. It invokes the build itself. See docs/VERIFICATION.md.

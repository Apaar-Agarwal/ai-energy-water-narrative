# Verification

The project includes packaged raw sources and processed outputs. Review notes and historical timings are in REVIEW_NOTES_NOV03.md and INTEGRATION_REPORT.md.

## Run locally

After installing requirements.txt with your project Python:

```text
python scripts/verify_integration.py
```

The suite rebuilds packaged processed files. Keep raw snapshots unchanged. It compares exact parsed table values across LF/CRLF line endings, then checks byte stability for a second build on the same platform. This detects source/value drift without treating Windows/macOS newline differences as changed observations.

## Checks

1. Source keys are unique and values within documented ranges.
2. Every electricity observation matches its original CSV row and value.
3. Every water score/missing value matches the workbook using bws/Tot, drr/Tot and rfr/Pop.
4. All 164 valid Apaar scores and all Harsh indicator scores match the integration.
5. The drought finding is recomputed using paired data: 65 of 86 records with bws<2 have drr>=2. Missing pairs are excluded.
6. A fresh app render contains FOUR chart elements before any interaction and no reveal button.
7. Country/year, measure, geography, comparator and risk controls raise no app exception.
8. Missing Canadian drought, same-country comparison, empty threshold filter, no-context view and earliest year are handled.
9. Source inspection and next-evidence interaction work.

## Source trace

The evidence inspector matches Entity/Year to the original electricity percentage and CSV row. Water matches country code, indicator/weight and workbook sheet/row. Sentinel -9999 becomes missing, never zero; scores are not converted to percentages.

Australia's original Apaar trace: country_baseline row 634, AUS / bws / Tot, score 2.906718433 (2.91 displayed). Confirm identifiers, not only a row number in a separately sorted spreadsheet.

## Limits

These checks do not certify unknown teaching-team scripts, a grade, deployed cold-start speed, colour-vision accessibility, personal AI declarations or licences. A script no longer needs to click to find four charts. Explicitly choosing an empty filter may still remove marks and show a message, as intended. Browser and public deployment checks remain.

Restricted Windows tests can emit a temporary-directory cleanup permission warning after assertions finish. Distinguish that from app exceptions, failed assertions or timeouts; do not ignore failed checks.

## Release review, 6 November 2026

The LF/CRLF regression, repeated-build test, source checks and full AppTest suite passed. The test machine used the required openpyxl from an existing local dependency directory; the portable package declares it in requirements.txt. This is not a claim of a clean dependency installation on every supported operating system. See RELEASE_REVIEW_NOV06.md and ACCESSIBILITY_REVIEW.md for the exact limits.

## Shared main upload, 8 November 2026

Until individual member folders have been uploaded, run `python scripts/verify_integration.py --shared-only`. This explicitly reports the member-snapshot comparison as NOT RUN; it does not skip any shared raw-source, reproducibility or app interaction checks. The default command remains strict and requires the member snapshots.

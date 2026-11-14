> Historical review. Current deployment and final status: FINAL_REVIEW_NOV14.md.

# Local release preparation — 6 November 2026

Input: the user-supplied AI_Energy_Water_Part2.zip. Its original archive was left unchanged. Output is a separate clean source package; no GitHub push or deployment was performed.

## Changes

- Removed .venv, __pycache__, __MACOSX, compiled files and OS metadata from the deliverable.
- Replaced cross-platform CSV byte comparison with exact parsed-table comparison; retained a repeated-build byte-stability check and added explicit LF/CRLF regression coverage.
- Removed an author-machine sibling dependency-path shortcut. Dependencies are declared in requirements.txt.
- Preserved Brighty's supplied provenance/disclosure, retained Sanjai's honest visual-review scope, added a clearly attributed Apaar water-stress row and distinguished automated integration checks from personal student checks.
- Reconciled current member-confirmation notes, disclosure, documentation index and release checklist. Historical integration reports remain history.
- Verified reference vintages against WRI's Aqueduct 4.0 technical note: drought 2000–2014; riverine flood 2010 baseline with 2016 protection input. Added explicit app/docs wording.
- Added third-party notices. Confirmed that the separate IEA Energy and AI data product is Non-CC; did not confuse the CC-licensed reports with dataset permission. Public redistribution is unresolved.
- Strengthened selected scatter-case size/opacity and smallprint contrast. Kept all four charts unconditional.
- Prepared publication procedure and release metadata file with null public identifiers rather than fabricated URLs/hashes.

## Verification evidence

Source checks: 40 electricity rows, 192 water records, 164 Apaar scores matching, all supplied Harsh scores matching; drought finding 65/86 reproduced. Repeated build and LF/CRLF regression passed. Four charts rendered initially. Country/year, trajectory measure, geography, risk toggle, missing Canadian drought, empty filter, same-country comparison, source inspection and decision interactions passed with no app exceptions.

Local test run after the portability fix: opening render 3.92 seconds, country update 1.02 seconds; these are local observations and not public-host performance guarantees. Final rerun after frontend wording/symbol refinements: opening 2.92 seconds; country update 0.62 seconds; source and guided-interaction checks passed, exit code 0. Restricted Windows cleanup warnings occurred after successful test assertions and exit code 0; no app exception was ignored.

Browser: 1366x768 default and expanded-value tables had page width 1366; all four chart elements were present. At 390x844 the page width was 390 and four chart elements remained present. See ACCESSIBILITY_REVIEW.md for simulation scope.

## What is not complete

The source package is locally prepared. It is not yet an assessed public release. The IEA reuse limitation, actual public deployment/revision, deployed performance check and final URL/revision PDF cannot be certified by local packaging. Member accounts are present; only the actual members can confirm personal actions. See ../submission/RELEASE_STEPS.md.

## Contributor-folder correction

Apaar's complete original water-stress contribution is now under contributors/Apaar, alongside Brighty, Harsh and Sanjai. It was relocated from dashboards/member_3_water_stress without changing its files. Root documentation, provenance paths and verification references were updated. The integrated app still runs from root app.py.

## Contributor-only organisation

Removed the redundant top-level dashboards folder. The path-corrected Brighty and Harsh standalone modules are now in their respective contributors folders. No contribution or source data was dropped. Their data paths were checked against the actual member-local files. Root app.py, frontend.py and story.py remain the active group app. contributors/README.md maps all four standalone entry points.

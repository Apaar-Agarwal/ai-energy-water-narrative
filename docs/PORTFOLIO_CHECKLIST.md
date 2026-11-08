# Part 2 release checklist

Current status: 6 November 2026. This is a local release candidate; public release is not certified. Historical notes do not override this file.

## Local implementation and data

- [x] One arguable question and persona in README and opening screen.
- [x] Three user stories and a coherent four-chapter narrative.
- [x] Answer and reasonable counterinterpretation on screen.
- [x] Four charts on initial render: two electricity and two water.
- [x] Three visual families: ranking/magnitude, change over time, correlation.
- [x] Chart tasks, forms, alternatives, titles, units and limitations documented.
- [x] Values labelled or available in tables without hover.
- [x] Shared country/year and additional water interactions; missing and empty states tested.
- [x] Every packaged electricity observation and water score traced to original sources.
- [x] Cross-platform newline regression and repeated local build passed.
- [x] Source coverage, transformations, indicator-specific periods and source credits documented.
- [x] Named AI rows for all four members and matching disclosures; supplied personal checks distinguished from assistant checks.
- [x] Clean source package excludes environments, caches, OS metadata and secrets.
- [x] Desktop 1366x768 default and expanded-table checks: no page-level horizontal overflow.
- [x] Colour-vision simulation reviewed by the assistant; shapes, patterns and labels supplement colours.

## Final external/human steps

- [ ] Each member confirms their own supplied account is accurate; do not invent a sign-off.
- [ ] Team/human accessibility acceptance. Simulation is supporting evidence, not a user study.
- [ ] Resolve public redistribution of the IEA-derived electricity snapshot (THIRD_PARTY_NOTICES.md).
- [ ] Publish the approved source revision to GitHub; record actual assessed commit/tag.
- [ ] Deploy the approved app; verify public URL signed out and public timing/interactions.
- [ ] Generate the submission PDF with real app URL, repository URL and assessed revision.

Follow ../submission/RELEASE_STEPS.md. Never substitute this checklist, a localhost URL or a ZIP hash for the required final release.

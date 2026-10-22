# Powering AI: Why Location Matters

Assignment 3 — Data Narrative Studio. Shared workspace for four individual dashboards (Part 1) and one integrated Streamlit narrative (Part 2).

## Question
Should data-centre expansion supporting AI be assessed against local electricity and water constraints rather than global averages?

## Persona
An infrastructure policy adviser deciding whether expansion guidelines should vary by location. Country-level comparisons provide screening evidence, not site approval decisions.

## Three user stories
- As an infrastructure policy adviser, I want to compare data-centre electricity-demand shares across countries so that I can identify where demand is relatively significant.
- As an infrastructure policy adviser, I want to examine water stress and drought risk for the same countries so that I can identify additional resource constraints.
- As an infrastructure policy adviser, I want to inspect sources, transformations and limitations so that I can judge whether the evidence supports location-specific guidelines.

## Contributions
| Member | Standalone dashboard | Final story role |
|---|---|---|
| 1 | Electricity comparison | Where demand is significant |
| 2 | Electricity change, subject to available comparable years | How pressure changes |
| 3 | Baseline water stress | Where water constraints differ |
| 4 | Water stress versus drought risk; optional riverine-flood toggle | What water stress alone misses |

## Repository structure
- dashboards/ — each member's standalone dashboard and reusable components.
- data/raw/ — original source samples and source metadata.
- data/processed/ — reproducible files read by the app.
- scripts/ — documented data preparation and verification.
- docs/ — data dictionary, AI provenance, disclosure, design notes and checks.
- submission/ — final submission PDF with public app URL, repo URL and assessed commit hash/tag.

Add the shared app.py and requirements.txt during integration. No dashboard code or datasets have been uploaded in this initial structure.

## Sources and interpretation
- [OWID electricity dataset](https://ourworldindata.org/grapher/data-centers-share-electricity-demand)
- [WRI Aqueduct country rankings](https://www.wri.org/data/aqueduct-40-country-rankings)
- [Aqueduct country dictionary](https://github.com/wri/Aqueduct40/blob/master/data_dictionary_country-rankings.md)

Electricity figures cover data centres generally, not AI alone. Aqueduct describes water conditions, not AI water consumption. Use compatible country codes and geography; document indicator vintage and weighting (Tot for the water-stress comparison). Preserve missing values, never replace missing risk scores with zero. Verify quantitative claims against source files before publishing.

## Team workflow
Each member adds their own work in a separate branch and opens a pull request. Keep standalone dashboards runnable; agree shared country scope before integration. Do not commit credentials, virtual environments, local logs or recordings. Record substantive AI assistance and a verification check that could fail. Each member must own a provenance row.

## Part 2 narrative
Opening decision → electricity comparison → electricity change → water stress → drought risk → qualified shared answer and limitations. Use a shared country selector and transitions, rather than four unrelated tabs.

## Required portfolio evidence
At least four charts across three Visual Vocabulary families; readable values and labelled units; two responsive interactions; clear empty states; accessible colours; sources and last refresh visible. Include reproducible data, complete dictionary, Data and AI disclosure and member provenance. Test at 1366×768 with vertical scrolling only, deployment under five seconds and interactions around one second. Check all 30 rubric items before submission.

## Deadlines
- Part 1 recording: 23 October 2026, 11:59 pm; maximum five minutes.
- Peer feedback: 6 November 2026.
- Part 2 portfolio: 20 November 2026, 11:59 pm.

## Status
Starter structure only. Team uploads, analysis, verification, deployment and assessed release remain to be completed. Repository visibility does not grant write access; invite teammates as collaborators.

# Data and AI disclosure

The narrative uses OWID data-centre electricity estimates and WRI Aqueduct national water indicators. Electricity covers all data centres, not AI alone. Water scores describe contextual environmental risk, not AI/facility consumption. Units, geography, absent years and missingness remain explicit. There is no causal model, combined sustainability score or site-approval classifier.

Source definitions and transformations are in DATA_DICTIONARY.md; reference vintages and reuse conditions are in THIRD_PARTY_NOTICES.md. Source download dates are attributed member reports. The separate IEA data-product licence has not been replaced by the reports' CC licences; public redistribution requires resolution before release.

Brighty used Claude (Anthropic) for the electricity comparison dashboard code, the OWID processing script and debugging, and verified the output against the raw OWID file as recorded in AI_PROVENANCE.csv.

Sanjai used Claude (Anthropic) to support Grid Pressure visualisations, regional comparisons, change since 2020, ranked charts and the illustrative threshold. His supplied verification was a visual review, not an independent numerical audit. Team source-value checks are recorded separately.

Harsh's supplied record reports Claude/Cowork assistance with processing, indicator choice and the stress/drought scatter. It describes a failed row-count check and fix, missing-value checks, source comparisons and interface checks; see m4_ai_provenance_rows.md. Those personal actions remain attributed to Harsh.

Apaar used OpenAI Codex for the water-stress dashboard, source processing, group integration, frontend, documentation and release preparation. Executed verification compared raw and processed values, joins, missingness, every member water score, regeneration, LF/CRLF portability and app interactions. These are assistant-executed checks, not a claim of an additional student manual review. AI is not the numerical source.

The consolidated matrix records tools, requests, outputs, verification and outcomes. All four named members have entries. Members should correct any inaccurate account before submission. No tool version or personal check has been invented.

Original member files are preserved as contribution evidence. AEMO material remains archived and excluded from the two-source narrative. All four charts render on initial load. The shared integration is being published to main on 8 November 2026 with Apaar's approval. Individual folders are uploaded separately by their members. This source upload is not a deployment; final submission identifiers must be real and verified.

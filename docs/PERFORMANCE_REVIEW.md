# Performance observations - 14 November 2026

Local full verification after the final code edits: opening render 2.08 seconds; linked country change 0.41 seconds. Four charts render initially. The complete source, regeneration, member-comparison and guided-interaction suite passed.

The evidence inspector now caches unchanged raw CSV snapshots between reruns. This avoids repeated source parsing; it does not replace or change any displayed source values.

Live browser automation of the existing public deployment measured 6.544 seconds from a full outer-page reload to the opening heading becoming attached. This includes browser automation/Cloud wrapper overhead, so it is not a precise human paint benchmark. It does NOT establish the rubric's under-five-second public-load check. Local measurements must not be represented as public measurements. Updated deployment observations are retained in the final delivery's Deployment_Record.json.

Network latency, browser state and Streamlit cold starts vary. Test from the assessor-facing URL again on the due date. No always-under-five-second or always-one-second claim is made. Country/year and water-risk changes are functional; live response observations are reported separately when measured.

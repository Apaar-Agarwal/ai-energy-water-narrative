# Design notes

## Audience and story

The persona is an infrastructure policy adviser considering location-specific expansion guidelines. One persistent US/China profile links electricity share, change, baseline water stress and additional drought/flood risk. A water-only comparison demonstrates what the first indicator may miss. The final brief asks what local evidence is needed; it does not approve a site or invent a sustainability score.

All four charts render on initial load. The dark water transition and optional hypothesis retain the narrative pause without hiding required charts or the conclusion. Sidebar anchors permit free navigation. Detailed values remain readable in expandable tables without hovering.

## Chart decisions

| Chart | Visual task / family | Chosen form and reason | Alternative rejected and reason |
|---|---|---|---|
| Electricity share | Compare/rank magnitudes | Labelled horizontal bars with a world reference; precise values and readable country names | Pie: separate denominators, not parts of a whole. Map: sparse coverage and geographic size distract from precise comparisons |
| Electricity trajectory | Change over time | Lines with points and labels, actual year spacing, share/change toggle | Grouped bars repeat marks and make the trajectory harder to follow; missing years are never filled |
| Water stress | Compare/rank magnitudes | Labelled bars on a common 0-5 score scale | Choropleth map: country area dominates a precise two-case comparison |
| Stress versus drought/flood | Association | Scatter with threshold zone, case labels, context and blind-spot filter | Separate rankings conceal paired observations; a combined score would impose unsupported weights |

Families: ranking/magnitude, change over time and correlation; confirm the course Visual Vocabulary terminology. Equal scores across water indicators do not mean equal physical impacts.

## Interactions

Country-bar clicks update the profile, with a sidebar control as an alternative. Year changes update electricity views and the brief. Regional context stays separate from overlapping countries. A water-only comparator does not gain a fabricated electricity value. Drought/flood, context and threshold-zone controls expose missingness and different readings. The optional hypothesis and next-evidence choice encourage reasoning, not a scored quiz.

## Presentation and accessibility

Cream, dark teal and serif headings unify the editorial layout. US/China colours remain consistent; line patterns and scatter shapes supplement colour. Values are labelled or tabulated. Missing and empty selections receive messages, not zeros. The revised four-chart default and expanded tables were reviewed at 1366x768; assistant colour-vision simulation checks are recorded in ACCESSIBILITY_REVIEW.md. This is not a human user study. Do not claim public timing from local tests.

Brighty owns the original comparison, Sanjai grid share/change, Apaar water stress and Harsh additional water risk. Originals are preserved. Codex assisted integration/frontend/documentation; personal declarations remain governed by the provenance matrix.

# Local accessibility and presentation review

6 November 2026. Reviewer: OpenAI Codex (assistant visual review). No human participant, disability user study or formal accessibility certification is claimed.

## Observed checks

- At 1366x768, four chart elements were present. The page width was 1366 pixels, matching the viewport.
- Expanding the electricity values and all scatter values still produced a page width of 1366 pixels. Data tables can have their own contained scrolling.
- At 390x844 the page width matched the 390-pixel viewport; all four chart elements remained present and the side panel collapsed.
- Bars have country labels and numeric labels. Trajectories use line patterns, labels and a values table. Scatter uses diamonds/squares/circles, case labels and paired values.
- Simulated protanopia, deuteranopia and tritanopia views were inspected for all four chart forms; see review/colour_vision_review.png. The simulation uses severity-100 linear-RGB matrices, sRGB conversion and clipping; it is an approximation, not a diagnosis or accessibility guarantee.
- In the reviewed simulations, bar values, line trajectories and named scatter cases remain identifiable without relying solely on hue. Highlighted scatter cases were subsequently enlarged and set to full opacity, strengthening their distinction from context. Source data and thresholds are unchanged.
- Supporting smallprint was darkened. Empty and missing states are textual.

## Limits

The default desktop layout, expanded tables and narrow-screen rendering were spot checked locally. Hosting cold starts, every possible country/indicator combination, keyboard/screen-reader usability and team/human acceptance must not be inferred from these checks. Personal member sign-off remains a human action.

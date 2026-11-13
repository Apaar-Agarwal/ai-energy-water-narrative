# Part 1 recording – Member 4 talk track (target 4:40, hard limit 5:00)

**Before you record:** run `streamlit run dashboards/m4_stress_vs_drought.py`. Open three things: the app in the browser, the original `Aqueduct40_rankings_download_Y2023M07D05.xlsx` in Excel, and `data/processed/m4_water_stress_drought.csv`. Zoom the browser to 110–125 % so text is legible. Speak at about 140 words a minute.

---

### 0:00–0:30 · Question and persona  ✔ items 3, 4
*(Screen: app header)*

> "Our group asks: **should data-centre expansion supporting AI be assessed against local electricity and water constraints rather than global averages?** Our persona is **an infrastructure policy adviser** deciding whether expansion guidelines should vary by location. My dashboard asks a narrower question: does drought risk reveal water concerns that baseline water stress alone misses?"

### 0:30–1:45 · My dashboard  ✔ item 5
*(Screen: metrics row, then the chart)*

> "This is my module in our shared repo, `dashboards/m4_stress_vs_drought.py`. It opens on the whole dataset: 138 of 192 countries have both a water-stress score and a drought-risk score from WRI's Aqueduct 4.0. Of the 86 countries with low or low-medium water stress, below 20 per cent, **65, or 76 per cent, still score medium or higher for drought risk**. The two scores correlate at only 0.26."

*(Point to the shaded zone.)*

> "Each point is a country. The dashed lines are Aqueduct's own category boundaries. The shaded top-left zone is low stress but elevated drought risk. Ireland, the UK, the Netherlands, France and Japan, all major data-centre markets, sit there."

*(Interaction 1: untick regions down to Europe.)*
> "Filtering to Europe updates the chart, the takeaway and the table."

*(Interaction 2: switch to Riverine flood risk.)*
> "I can also switch the second indicator to flood risk, a siting risk rather than a supply one."

*(Clear all regions.)*
> "With nothing selected, it shows a message instead of an error."

*(Restore all regions and switch back to Drought risk.)*

### 1:45–2:35 · Design decision  ✔ item 6
*(Screen: the chart)*

> "The visual task is **relationship**: finding countries where two measures disagree. I chose a **scatter plot**. The alternative I rejected was **two ranked bar charts side by side**, which is how our water-stress dashboard ranks countries. I rejected it because the reader would have to find each of 138 countries in two separate lists to spot a mismatch. In the scatter, each country is one point, so the mismatch is a visible zone. I also rejected a combined risk index, because averaging the two scores would hide exactly the disagreement the question is about. I labelled the focus countries directly and added a table, so no value depends on hovering. Labelled versus other countries differ in fill as well as colour, so the encoding works for colour-blind viewers."

### 2:35–4:05 · Trace a number live  ✔ item 7
*(Screen: app table, Ireland row)*

> "I'll trace Ireland's drought score: **2.62** in the table."

1. *(Excel, sheet `country_baseline`. Filter `gid_0` = IRL, `indicator_name` = drr, `weight` = Tot.)*
   > "In WRI's original file: score 2.617392, category 2, label 'Medium, 0.4 to 0.6'. I use the `Tot` weight, which weights by total water demand, the same weighting as the water-stress score."
2. *(Processed CSV, row IRL.)*
   > "My script `m4_process.py` keeps that row, converts the minus-9999 NoData code to blank, not zero, and pivots to one row per country. Here `drr_score` is 2.617392."
3. *(App, open **Trace a number to the source file**, select Ireland.)*
   > "The app shows both rows side by side. On screen it's rounded to 2.62. That is above 2, the Medium boundary, and the water-stress score of 0.36 is below 2, so Ireland is flagged as low stress, elevated drought risk."

### 4:05–4:40 · AI use and its check  ✔ item 8
*(Screen: `docs/m4_ai_provenance_rows.md`)*

> "I used Claude to inspect the workbook and draft the processing script and the Streamlit app. Claude found that the file has no seasonal-variability indicator, so I confirmed that myself by listing the indicators, then switched to drought risk. For the script, my check was that the output must have one row per country, 192. **The first version failed that check**: it produced over a million rows because of a pivot setting. I fixed it, re-ran it, and also checked by hand that Canada's missing drought score stayed blank and wasn't turned into zero."

### 4:40 · Stop.

---
**Checklist before upload:** under 5:00 ✔ · mic audible, browser zoomed ✔ · question ✔ · persona ✔ · own module on screen ✔ · scatter vs two bar charts, with reason ✔ · Ireland 2.62 traced to xlsx ✔ · AI use and the failed check ✔

*Only say the AI lines you can stand behind. If you didn't do a step yourself (e.g. the Canada check), do it before recording; it takes 30 seconds.*

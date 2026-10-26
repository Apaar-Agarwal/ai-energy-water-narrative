# Member 2 - Grid pressure: full guide

## 0. Get the data (2 minutes)
1. Open https://ourworldindata.org/grapher/data-centers-share-electricity-demand
2. Click **Download > Download full data** (ZIP with CSV + metadata JSON + README).
3. Run: `python prepare_data.py --file ~/Downloads/data-centers-share-electricity-demand.zip`
   (or just `python prepare_data.py` to download automatically).
4. Run: `streamlit run grid_pressure.py`
Keep the ZIP's metadata JSON and README in `data/raw/` too: they are your evidence.

## 1. What the dataset really contains (checked against OWID metadata, version 2026-06-30)
- Unit: percent. Years: 2020, 2023, 2024, 2025 only (2021-22 absent - never interpolate).
- 10 entities: Africa (IEA), Asia Pacific (IEA), Central and South America (IEA), China, Europe (IEA),
  Middle East (IEA), North America (IEA), United States, World, World excl. United States and China.
- They OVERLAP (US is inside North America; China inside Asia Pacific; World contains all).
  Ranking them in one chart would double count, so the app offers two non-overlapping views.
- Numerator: IEA data-centre electricity use (incl. cooling), AI and non-AI. Denominator: Ember total demand.
- IEA publishes no Eurasia aggregate, so the six regions do not cover the whole world.

## 2. Source register entry (copy into repo)
| Field | Entry |
|---|---|
| Source | Our World in Data, "Share of total electricity demand coming from data centers"; originals: IEA "Energy and AI"; Ember "Yearly Electricity Data" |
| Original file | data-centers-share-electricity-demand.csv (full), accessed [DATE], OWID dataset version 2026-06-30 |
| Coverage | 10 entities, years 2020, 2023-2025 |
| Meaning | % of a region's total electricity demand used by ALL data centres; IEA estimates / Ember statistics |
| Licence | OWID: CC BY 4.0; underlying IEA terms (c) OECD/IEA still apply; Ember CC BY 4.0 |
| Processing | prepare_data.py: renamed columns, dropped rows with missing share (count printed), no interpolation |
| Verification | One bar recomputed from IEA TWh / Ember TWh (section 5) |

## 3. Data dictionary entries
| Column | Meaning | Unit | Type |
|---|---|---|---|
| location | Country or IEA region | text | label |
| code | ISO / OWID code, blank for IEA regions | text | label |
| year | Calendar year | year | int |
| share_pct | Data-centre electricity / total electricity demand x 100 | % | estimate |
| value (app only) | share_pct, or share_pct(year) - share_pct(2020) | % or pp | derived |

## 4. Design decision (task - form - rejected - reason)
- **Visual task:** rank places by how large a share of their grid data centres use, with precise differences.
- **Chosen:** ranked horizontal bars with value labels and a dashed world-average line.
- **Rejected:** (a) pie chart - the shares are not parts of one whole and sit at 0.5-6%, so slices would be tiny and unreadable;
  (b) choropleth map - only 3 countries/6 regions exist, regions are huge, and colour hides the 1-point differences planners need.
- **Extra defensible choices:** two non-overlapping views to avoid double counting; no interpolation of 2021-22;
  a "change since 2020" measure so the story is about speed, not only level.

## 5. Verification (could fail)
1. In the app pick United States, 2024 (or any bar). Note the value.
2. Open raw CSV row: same location/year (the app's "Trace the numbers" expander shows it too).
3. Recompute: IEA Energy and AI file (https://www.iea.org/data-and-statistics/data-product/energy-and-ai) gives US data-centre TWh;
   Ember (https://files.ember-energy.org/public-downloads/yearly_full_release_long_format.csv) gives US total demand TWh.
   share = TWh_dc / TWh_total x 100. Show the division on screen. A mismatch beyond rounding = FAIL (report it honestly).
Do not commit the IEA file to GitHub (non-CC terms); cite its URL.

## 6. Recording script (target 4:40)
- 0:00-0:30 "Our question: should electricity and water limits constrain AI data-centre expansion? Persona: a regional infrastructure planner. My section answers: where is the grid already most exposed?"
- 0:30-1:50 Demo: toggle the two views, move the year slider, switch to change-since-2020. State ONE finding with a real number and say "all data centres, not only AI".
- 1:50-2:40 Design decision (section 4): task, ranked bars, rejected pie AND map, the reasons.
- 2:40-4:10 Trace: app bar -> raw CSV row -> IEA TWh / Ember TWh -> division on screen.
- 4:10-4:40 AI disclosure (section 7).
Rehearse with a timer; stop at 4:40. Check mic and zoom the browser to 125%.

## 7. AI disclosure (fill in truthfully)
"I used [tool] to draft the Streamlit code and data-prep script and to suggest dataset sources. I checked it by (1) opening the raw CSV and
confirming the columns and years, (2) noticing the entities overlap and confirming the app never ranks them together, and (3) recomputing
[location, year] from IEA and Ember figures. [State anything the AI got wrong or you changed.]"
Provenance row: | Member 2 | [tool] | code + source suggestions | prompts + what you changed | checks above |

## 8. Eight-item checklist self-test
[ ] <=5:00 [ ] voice audible, screen legible [ ] question stated [ ] persona named [ ] own section on screen
[ ] design decision + named alternative + why it lost [ ] number traced to source on screen [ ] AI use + check disclosed

## 9. Part 2 duties (integration, deployment, speed, layout)
- Everyone exposes `render()`; app.py (provided) imports each section as a tab. Add teammates' modules to the SECTIONS list.
- requirements.txt is complete; push to GitHub; deploy on Streamlit Community Cloud (main file: app.py).
- Commit processed CSVs (not the IEA file). Use @st.cache_data. Test at phone width, check first-load time, tag a release and record the commit hash.

## 10. Interactions you can demo (5 controls)
View (non-overlapping sets), Measure (share vs change since 2020), Year slider, Location multiselect, and the planner threshold
slider (colours bars at/above your own line and writes a plain-language note). Say clearly: the threshold is a screening line YOU choose, not an official limit.

## 11. Australia spotlight (added 21 Oct 2026)
- Australia is not in the OWID file, so it has its own tab, fed by data/processed/australia_aemo.csv (hand-transcribed from AEMO and reports of AEMO).
- Not like-for-like with OWID: AEMO figures are NEM/grid-supplied, financial years, estimates and forecasts. Never put them in the OWID ranked bar.
- PRIMARY (read on AEMO's page): about 2% today; 12 TWh / about 6% by 2030; 34 TWh / 12% by 2050 (2025 IASR).
- SECONDARY (confirm in AEMO's ESOO 2026 / ISP 2026 before quoting on camera): 3.9 TWh 2024-25; about 5 TWh / 3% in 2025-26; 34 TWh / 13% by 2035-36; 52 TWh high growth.
- Source register: add AEMO news update (1 Jun 2026), accessed 21 Oct 2026; list each secondary URL from data/raw/australia_sources.md.
- Verification for Australia: 3.9 TWh / about 205 TWh NEM = 1.9%, vs AEMO "about 2%". Check the 205 TWh in AEMO's ISP.
- Data currency: OWID updated 30 Jun 2026, series ends 2025, next update expected 30 Jun 2027. AEMO's ESOO (Aug 2026) is the newest Australian source I found.

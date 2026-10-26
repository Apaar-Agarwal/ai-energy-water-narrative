"""Member 4 dashboard - Does drought risk reveal concerns that baseline water
stress alone misses?

Standalone Streamlit module. Run from the repo root:
    streamlit run dashboards/m4_stress_vs_drought.py

Reads only data/processed/m4_water_stress_drought.csv (built by
scripts/m4_process.py) and, for the trace panel, the unchanged source sample
data/source/aqueduct40_country_baseline.csv.
"""
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data/processed/m4_water_stress_drought.csv"
SOURCE = ROOT / "data/source/aqueduct40_country_baseline.csv"

SOURCE_FILE = "Aqueduct40_rankings_download_Y2023M07D05.xlsx (sheet country_baseline)"
SOURCE_URL = "https://www.wri.org/data/aqueduct-40-country-rankings"
SOURCE_RELEASE = "5 July 2023 (file date); WRI page published 16 Aug 2023"
BASELINE_PERIOD = "1979–2019 hydrological baseline"
DOWNLOADED = "22 Oct 2026"  # date the group downloaded the file - confirm

# Commonly cited data-centre markets. This list is the group's choice, not
# something the Aqueduct data says. Align with Member 1's country set.
DEFAULT_FOCUS = ["USA", "CHN", "IRL", "GBR", "DEU", "NLD", "FRA", "JPN", "AUS", "IND"]

# Colour: focus = blue filled circle, context = grey hollow circle. Shape and
# fill differ as well as hue, so identity never depends on colour alone.
FOCUS = "#2a78d6"
CONTEXT = "#8a8986"
BAND = "#eb6834"

Y_OPTIONS = {
    "Drought risk": {
        "prefix": "drr",
        "axis": "Drought risk score (0–5)",
        "scale": "Score bands 0–1 … 4–5 = raw drought-risk index 0.0–0.2 … 0.8–1.0",
        "elevated": "Medium or higher (raw index ≥ 0.4)",
        "weight": "weighted by total water demand",
    },
    "Riverine flood risk": {
        "prefix": "rfr",
        "axis": "Riverine flood risk score (0–5)",
        "scale": "Score bands = expected share of population affected per year: "
                 "<2 in 1,000 … >1 in 100",
        "elevated": "Medium-High or higher (≥ 4 in 1,000 people per year)",
        "weight": "weighted by population",
    },
}

st.set_page_config(page_title="Water stress vs drought risk", layout="wide")


def _full_width(fn, *args, **kwargs):
    """Call a Streamlit element at full width on old and new Streamlit versions."""
    try:
        return fn(*args, width="stretch", **kwargs)
    except TypeError:
        return fn(*args, use_container_width=True, **kwargs)



@st.cache_data
def load():
    df = pd.read_csv(PROCESSED)
    src = pd.read_csv(SOURCE)
    return df, src


df, src = load()

# ---------------------------------------------------------------- header
st.caption("Powering AI: Why Location Matters · Member 4 dashboard")
st.title("Does drought risk reveal concerns that baseline water stress alone misses?")
st.markdown(
    "**Group question:** Should data-centre expansion supporting AI be assessed "
    "against local electricity and water constraints rather than global averages?  \n"
    "**Persona:** an infrastructure policy adviser deciding whether expansion "
    "guidelines should vary by location."
)

# ---------------------------------------------------------- whole dataset
pairs = df.dropna(subset=["bws_score", "drr_score"])
low = pairs[pairs.bws_score < 2]
low_flag = low[low.drr_score >= 2]
r = pairs.bws_score.corr(pairs.drr_score)

st.subheader("Across all countries with both scores")
c1, c2, c3 = st.columns(3)
c1.metric("Countries with both a water-stress and a drought score",
          f"{len(pairs)} of {len(df)}")
c2.metric("Low or Low-Medium stress countries (<20 %) with Medium+ drought risk",
          f"{len(low_flag)} of {len(low)}  ({len(low_flag) / len(low):.0%})")
c3.metric("Correlation between the two scores (Pearson r)", f"{r:.2f}")
st.markdown(
    f"**Finding:** in the Aqueduct 4.0 baseline, a low water-stress score is a poor "
    f"guide to drought risk. {len(low_flag)} of the {len(low)} countries whose "
    f"average withdrawals use less than 20 % of renewable supply still score "
    f"Medium or higher for drought risk, and across {len(pairs)} countries the two "
    f"scores are only weakly related (r = {r:.2f}). Screening on average water "
    f"stress alone would miss these countries."
)

# --------------------------------------------------------------- controls
st.subheader("Explore")
k1, k2, k3 = st.columns([1.1, 1.4, 2.5])
y_name = k1.radio("Compare water stress with", list(Y_OPTIONS), horizontal=False)
regions = sorted(df.un_region.dropna().unique())
pick_regions = k2.multiselect("UN region", regions, default=regions)
name_by_iso = df.set_index("iso3").country.to_dict()
focus = k3.multiselect(
    "Countries to label (default: commonly cited data-centre markets)",
    options=sorted(df.iso3, key=lambda c: name_by_iso[c]),
    default=DEFAULT_FOCUS,
    format_func=lambda c: name_by_iso[c],
)

cfg = Y_OPTIONS[y_name]
p = cfg["prefix"]
ys, yl = f"{p}_score", f"{p}_label"

view = df[df.un_region.isin(pick_regions)].copy()
plot = view.dropna(subset=["bws_score", ys]).copy()
plot["group"] = plot.iso3.isin(focus).map({True: "Labelled country", False: "Other country"})
plot["flag"] = (plot.bws_score < 2) & (plot[ys] >= 2)

# ------------------------------------------------------------------ chart
st.markdown(f"#### Baseline water stress vs {y_name.lower()}, by country "
            f"(Aqueduct 4.0, {BASELINE_PERIOD})")

if not pick_regions:
    st.info("No region selected. Choose at least one UN region to show countries.")
elif plot.empty:
    st.info(f"No country in the selected region(s) has both a water-stress and a "
            f"{y_name.lower()} score. Aqueduct reports these as NoData.")
else:
    band = pd.DataFrame({"x": [0], "x2": [2], "y": [2], "y2": [5]})
    band_layer = alt.Chart(band).mark_rect(color=BAND, opacity=0.08).encode(
        x="x:Q", x2="x2:Q", y="y:Q", y2="y2:Q")
    band_text = alt.Chart(pd.DataFrame({"x": [0.08], "y": [4.85],
                                        "t": [f"Low stress, {y_name.lower()} elevated"]})
                          ).mark_text(align="left", baseline="top", fontSize=12,
                                      color="#9a3c12").encode(x="x:Q", y="y:Q", text="t:N")
    rules = alt.Chart(pd.DataFrame({"v": [2]})).mark_rule(
        color="#52514e", strokeDash=[4, 3], strokeWidth=1)
    vrule = rules.encode(x="v:Q")
    hrule = rules.encode(y="v:Q")

    x_enc = alt.X("bws_score:Q", scale=alt.Scale(domain=[-0.15, 5.15], nice=False),
                  title="Baseline water stress score (0–5; 2 = 20 % of renewable supply withdrawn)",
                  axis=alt.Axis(values=[0, 1, 2, 3, 4, 5], grid=False))
    y_enc = alt.Y(f"{ys}:Q", scale=alt.Scale(domain=[-0.15, 5.15], nice=False), title=cfg["axis"],
                  axis=alt.Axis(values=[0, 1, 2, 3, 4, 5], grid=False))
    tip = [alt.Tooltip("country:N", title="Country"),
           alt.Tooltip("bws_score:Q", title="Water stress score", format=".2f"),
           alt.Tooltip("bws_label:N", title="Water stress category"),
           alt.Tooltip(f"{ys}:Q", title=f"{y_name} score", format=".2f"),
           alt.Tooltip(f"{yl}:N", title=f"{y_name} category")]

    points = alt.Chart(plot).mark_point(size=70, strokeWidth=1.5).encode(
        x=x_enc, y=y_enc,
        shape=alt.Shape("group:N", title="Point", scale=alt.Scale(
            domain=["Labelled country", "Other country"], range=["circle", "circle"])),
        color=alt.Color("group:N", title="Point", scale=alt.Scale(
            domain=["Labelled country", "Other country"], range=[FOCUS, CONTEXT])),
        fill=alt.Fill("group:N", legend=None, scale=alt.Scale(
            domain=["Labelled country", "Other country"], range=[FOCUS, "transparent"])),
        size=alt.Size("group:N", legend=None, scale=alt.Scale(
            domain=["Labelled country", "Other country"], range=[110, 45])),
        order=alt.Order("group:N", sort="descending"),
        opacity=alt.value(1),
        tooltip=tip,
    )
    labels = alt.Chart(plot[plot.group == "Labelled country"]).mark_text(
        align="left", dx=8, dy=-6, fontSize=12, color="#0b0b0b").encode(
        x="bws_score:Q", y=f"{ys}:Q", text="country:N")

    chart = (band_layer + band_text + vrule + hrule + points + labels).properties(
        height=430).configure_legend(orient="top", title=None, labelFontSize=12
    ).configure_axis(labelFontSize=12, titleFontSize=13)
    st.markdown(f"<span style='color:{FOCUS}'>●</span> filled blue = labelled country "
                f"&nbsp;&nbsp; <span style='color:{CONTEXT}'>○</span> hollow grey = other "
                f"country &nbsp;&nbsp; <span style='color:{BAND}'>■</span> shaded zone = "
                f"low stress but {y_name.lower()} elevated", unsafe_allow_html=True)
    _full_width(st.altair_chart, chart)
    st.caption(
        f"Each point is a country. Dashed lines mark score 2 on each axis: left of "
        f"the vertical line is Low or Low-Medium water stress (<20 %); above the "
        f"horizontal line is {cfg['elevated']}. {cfg['scale']}. "
        f"Water stress weighted by total water demand; {y_name.lower()} {cfg['weight']}. "
        f"Showing {len(plot)} countries with both scores in the selected region(s)."
    )

    n_low = int((plot.bws_score < 2).sum())
    n_flag = int(plot.flag.sum())
    flagged_focus = plot[plot.flag & (plot.group == "Labelled country")].country.tolist()
    msg = (f"**Takeaway for this selection:** {n_flag} of {n_low} low-stress countries "
           f"shown score {cfg['elevated'].split(' (')[0]} for {y_name.lower()}.")
    if flagged_focus:
        msg += " Labelled countries in the shaded zone: " + ", ".join(flagged_focus) + "."
    st.markdown(msg)

# ------------------------------------------------------------------ table
st.markdown(f"#### Values for labelled countries ({BASELINE_PERIOD})")
if not focus:
    st.info("No countries selected to label. Pick countries above to see their values.")
else:
    t = view[view.iso3.isin(focus)].copy()
    missing_region = [name_by_iso[c] for c in focus if c not in set(t.iso3)]
    if t.empty:
        st.info("None of the labelled countries is in the selected region(s).")
    else:
        t = t.sort_values(ys, ascending=False, na_position="last")
        table = pd.DataFrame({
            "Country": t.country,
            "Water stress score (0–5)": t.bws_score.round(2),
            "Water stress category": t.bws_label,
            f"{y_name} score (0–5)": t[ys].round(2),
            f"{y_name} category": t[yl],
            "Low stress, elevated risk?": ((t.bws_score < 2) & (t[ys] >= 2)).where(
                t.bws_score.notna() & t[ys].notna()).map(
                {True: "Yes", False: "No"}).fillna("No data"),
        })
        _full_width(st.dataframe, table, hide_index=True)
        nodata = t[t[ys].isna() | t.bws_score.isna()].country.tolist()
        if nodata:
            st.caption("Not plotted (Aqueduct NoData): " + ", ".join(nodata) + ".")
    if missing_region:
        st.caption("Outside the selected region(s): " + ", ".join(missing_region) + ".")

# ---------------------------------------------------------- definitions etc.
d1, d2 = st.columns(2)
with d1:
    st.markdown("#### Definitions")
    st.markdown(
        "- **Baseline water stress:** total water withdrawals as a share of available "
        "renewable surface and groundwater supply, averaged over 1979–2019 and scored "
        "0–5. Categories: Low (<10 %), Low-Medium (10–20 %), Medium-High (20–40 %), "
        "High (40–80 %), Extremely High (>80 %).\n"
        "- **Drought risk:** Aqueduct's index of drought hazard, exposure and "
        "vulnerability, 0–1 raw, scored 0–5 in five equal 0.2 bands.\n"
        "- **Riverine flood risk:** expected share of the population affected by "
        "riverine floods per year, scored 0–5.\n"
        "- A score is a ranked band, not a physical unit; the axes cannot be read as "
        "'twice as stressed'."
    )
with d2:
    st.markdown("#### What this data cannot show")
    st.markdown(
        "- How much water any data centre or AI workload uses. Aqueduct measures "
        "catchment conditions, not data-centre consumption.\n"
        "- Conditions at a specific site. National scores average over regions "
        "that differ widely (e.g. within the USA or India).\n"
        "- Current drought. The baseline is a 1979–2019 average, not live data.\n"
        "- Causation. A country's position on both axes doesn't explain why.\n"
        "- 54 of 192 countries, including Canada, Saudi Arabia, the UAE and "
        "Singapore, have no drought score, so they can't appear on the drought view."
    )

# ------------------------------------------------------------- trace panel
with st.expander("Trace a number to the source file"):
    plotted = df.dropna(subset=["bws_score", "drr_score"])
    iso = st.selectbox("Country", sorted(plotted.iso3, key=lambda c: name_by_iso[c]),
                       index=sorted(plotted.iso3, key=lambda c: name_by_iso[c]).index("IRL"),
                       format_func=lambda c: name_by_iso[c])
    raw = src[(src.gid_0 == iso) & (
        ((src.indicator_name.isin(["bws", "drr"])) & (src.weight == "Tot")) |
        ((src.indicator_name == "rfr") & (src.weight == "Pop")))]
    st.markdown(f"**1. Source rows** in `{SOURCE.relative_to(ROOT)}` (unchanged export "
                f"of {SOURCE_FILE}), filtered to gid_0 = {iso}:")
    _full_width(st.dataframe, raw, hide_index=True)
    st.markdown(f"**2. Processed row** in `{PROCESSED.relative_to(ROOT)}` "
                f"(made by `scripts/m4_process.py`: keep bws/Tot, drr/Tot, rfr/Pop; "
                f"-9999 → missing; pivot to one row per country):")
    _full_width(st.dataframe, df[df.iso3 == iso], hide_index=True)
    st.markdown("**3. On screen:** score rounded to 2 decimal places; the point sits "
                "at (water stress score, drought score).")

# ------------------------------------------------------------------ footer
st.divider()
st.caption(
    f"**Source:** World Resources Institute, Aqueduct 4.0 Country Rankings, "
    f"{SOURCE_FILE}. {SOURCE_URL}. Released {SOURCE_RELEASE}. {BASELINE_PERIOD}. "
    f"Downloaded {DOWNLOADED}. Licence: Creative Commons (per WRI). Citation: Kuzma "
    f"et al. 2023, Aqueduct 4.0 Technical Note, doi.org/10.46830/writn.23.00061. "
    f"WRI cautions that Aqueduct indicators can't be measured directly and haven't "
    f"been validated."
)

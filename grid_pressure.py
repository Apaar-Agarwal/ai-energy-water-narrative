"""Grid Pressure dashboard.

Research question:
Where do data centres already take a large share of the electricity grid, and
how fast is that share rising?

The dashboard keeps the original data model and processing logic while improving
its presentation, narrative and evidence framing for a professional university
assignment.
"""
import io
import altair as alt
import pandas as pd
import streamlit as st
PROCESSED = "data/processed/grid_share.csv"
AUS = "data/processed/australia_aemo.csv"
NAVY = "#1F3A5F"
TEAL = "#2B8A8A"
AMBER = "#F59E0B"
GREY = "#75849A"
TEXT = "#102A43"
SURFACE = "#F7F9FC"
BORDER = "#DDE6F0"
# Entities overlap (US is inside North America, China inside Asia Pacific, World
# contains all), so the app only ever ranks non-overlapping groups.
VIEWS = {
    "IEA world regions": [
        "Africa (IEA)",
        "Asia Pacific (IEA)",
        "Central and South America (IEA)",
        "Europe (IEA)",
        "Middle East (IEA)",
        "North America (IEA)",
    ],
    "US and China vs the rest": [
        "United States",
        "China",
        "World excl. United States and China",
    ],
}

SHARE, CHANGE = "Share of electricity demand", "Change since 2020"
SOURCE = (
    "Source: Our World in Data, 'Share of total electricity demand coming from data centers' "
    "(IEA data-centre consumption divided by Ember total electricity demand), accessed 21 Oct 2026. "
    "Covers all data centres, not only AI."
)
CSS = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: #eef4f7;
    color: #102a43;
}
[data-testid="stHeader"] {
    background: rgba(255,255,255,0);
}
.main .block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}
.hero {
    background: linear-gradient(135deg, #f7fbfd 0%, #edf5f8 42%, #f4f6fa 100%);
    border: 1px solid #dfeaf2;
    border-radius: 18px;
    padding: 1.6rem 1.7rem 1.3rem 1.7rem;
    margin-bottom: 1rem;
    box-shadow: 0 12px 28px rgba(16, 42, 67, 0.04);
}

.hero-tag {
    display: inline-block;
    margin-bottom: 0.7rem;
    padding: 0.28rem 0.7rem;
    border-radius: 999px;
    background: rgba(43, 138, 138, 0.1);
    color: #0f6d6d;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.hero h2 {
    margin: 0;
    color: #102a43;
    font-size: 2.4rem;
    line-height: 1.12;
    font-weight: 800;
    letter-spacing: -0.04em;
}
.hero p {
    margin: 0.8rem 0 0 0;
    color: #42586f;
    font-size: 1.05rem;
    line-height: 1.65;
    max-width: 980px;
}
.editorial-note {
    margin: 0.3rem 0 1rem 0;
    padding: 0.8rem 0.9rem;
    border-left: 4px solid #2b8a8a;
    border-radius: 10px;
    background: rgba(43, 138, 138, 0.05);
    color: #22516f;
    font-size: 0.92rem;
    line-height: 1.6;
}
.kpis {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 0.6rem 0 1rem 0;
}
.kpi {
    flex: 1 1 180px;
    min-width: 180px;
    background: rgba(255,255,255,0.9);
    border: 1px solid #dfeaf2;
    border-left: 5px solid #1f3a5f;
    border-radius: 14px;
    padding: 0.8rem 0.95rem 0.9rem 0.95rem;
    box-shadow: 0 6px 16px rgba(16, 42, 67, 0.025);
}

.kpi.alert {
    border-left-color: #e4572e;
    background: rgba(255, 248, 244, 0.92);
}

.kpi .lab {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5a7085;
    opacity: 0.9;
}

.kpi .val {
    margin-top: 0.38rem;
    color: #102a43;
    font-size: 1.7rem;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -0.03em;
}

.kpi .sub {
    margin-top: 0.2rem;
    color: #536b82;
    font-size: 0.82rem;
    line-height: 1.5;
}

.panel {
    background: rgba(255,255,255,0.88);
    border: 1px solid #dfeaf2;
    border-radius: 16px;
    padding: 1rem 1rem 0.9rem 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 10px 18px rgba(16, 42, 67, 0.02);
}

.note {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.22);
    border-left: 4px solid #e3a11d;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    color: #1f2b3a;
    line-height: 1.6;
}

.note strong {
    color: #102a43;
}

.stTabs [role="tablist"] {
    background: rgba(255,255,255,0.75);
    border: 1px solid #dfeaf2;
    border-radius: 12px;
    padding: 0.2rem 0.25rem;
}

.stTabs [role="tab"] {
    color: #39526a;
    font-weight: 600;
}

.stTabs [role="tab"][aria-selected="true"] {
    background: rgba(43, 138, 138, 0.09);
    border-radius: 10px;
    color: #0f4f4e;
}

[data-testid="stDataFrame"] {
    border: 1px solid #dfeaf2;
    border-radius: 12px;
    overflow: hidden;
}

section[data-testid="stSidebar"] {
    background: #f3f7fa;
}

.stRadio > label,
.stMultiSelect > label,
.stSlider > label,
.stSelectbox > label {
    color: #1d3557;
    font-weight: 700;
}

div[role="radiogroup"] label {
    color: #1e3550;
}

svg text {
    font-family: "Segoe UI", sans-serif;
}
</style>
"""


@st.cache_data
def load_processed():
    return pd.read_csv(PROCESSED)


def clean_upload(file):
    if file is None:
        return None
    df = pd.read_csv(io.BytesIO(file.getvalue()))
    df = df.rename(columns={"Entity": "location", "Code": "code", "Year": "year", df.columns[-1]: "share_pct"})
    return df.dropna(subset=["share_pct"])[["location", "code", "year", "share_pct"]]


def get_data():
    try:
        return load_processed()
    except FileNotFoundError:
        st.info("Processed file missing. Run `python prepare_data.py` or upload the raw OWID CSV.")
        up = st.file_uploader("Raw OWID CSV", type="csv")
        return clean_upload(up) if up else None


def kpi(label, value, sub="", alert=False):
    return (
        '<div class="kpi' + (' alert' if alert else '') + '">'
        f'<div class="lab">{label}</div>'
        f'<div class="val">{value}</div>'
        f'<div class="sub">{sub}</div>'
        '</div>'
    )


def render_global(df):
    years = sorted(df["year"].dropna().unique().tolist())
    c1, c2, c3 = st.columns([1.2, 1.1, 1.4])
    view = c1.radio(
        "Compare",
        list(VIEWS),
        help="Both views are non-overlapping, so nothing is double counted.",
    )
    metric = c2.radio("Measure", [SHARE, CHANGE])

    if metric == CHANGE:
        year = c3.select_slider(
            "Compare 2020 with",
            options=[y for y in years if y > 2020],
            value=max([y for y in years if y > 2020]),
        )
    else:
        year = c3.select_slider(
            "Year",
            options=years,
            value=max(years),
            help="Only years in the source are offered; 2021-2022 are not estimated.",
        )

    names = [name for name in VIEWS[view] if name in set(df["location"])]
    d1, d2 = st.columns([3, 2])
    chosen = d1.multiselect("Locations shown", names, default=names)
    threshold = d2.slider(
        "Your attention threshold (% of demand)",
        min_value=0.5,
        max_value=6.0,
        value=3.0,
        step=0.5,
        disabled=(metric == CHANGE),
        help="Your own screening line, not an official limit. Places at or above it are flagged for closer review.",
    )

    wide = df.pivot_table(index="location", columns="year", values="share_pct", aggfunc="first")

    def get_value(loc):
        if loc not in wide.index or pd.isna(wide.loc[loc].get(year)):
            return None
        if metric == CHANGE:
            base = wide.loc[loc].get(2020)
            if pd.isna(base):
                return None
            return float(wide.loc[loc, year] - base)
        return float(wide.loc[loc, year])

    data = pd.DataFrame(
        [{"location": loc, "value": get_value(loc)} for loc in chosen if get_value(loc) is not None]
    )
    if data.empty:
        st.warning("No data for this selection.")
        return

    data = data.sort_values("value", ascending=False).reset_index(drop=True)
    world = get_value("World")
    unit = "percentage points" if metric == CHANGE else "%"
    top = data.iloc[0]
    low = data.iloc[-1]

    flagged = data[data["value"] >= threshold] if metric == SHARE else pd.DataFrame()
    cards = [
        kpi(
            "Highest" if metric == SHARE else "Fastest rise",
            f"{top['value']:.2f}{'' if metric == CHANGE else '%'}",
            f"{top['location']}, {year}",
        ),
        kpi(
            "World reference",
            f"{world:.2f}{'' if metric == CHANGE else '%'}" if world is not None else "n/a",
            "all data centres, global",
        ),
    ]
    if metric == SHARE:
        cards.append(
            kpi(
                "At or above threshold",
                f"{len(flagged)} of {len(data)}",
                f"threshold {threshold:.1f}%",
                alert=True,
            )
        )
    else:
        cards.append(kpi("Slowest rise", f"{low['value']:.2f}", low["location"]))

    st.markdown('<div class="kpis">' + "".join(cards) + "</div>", unsafe_allow_html=True)

    data["flag"] = [
        "At or above threshold" if (metric == SHARE and value >= threshold) else "Below threshold / n.a."
        for value in data["value"]
    ]
    x_title = (
        "Data-centre share of electricity demand (%)"
        if metric == SHARE
        else f"Change in share, 2020 to {year} (percentage points)"
    )

    plot_data = data.sort_values("value", ascending=False).reset_index(drop=True)
    plot_data["location"] = plot_data["location"].astype(str)

    chart = alt.Chart(plot_data).mark_bar(cornerRadiusTopRight=7, cornerRadiusBottomRight=7).encode(
        x=alt.X("value:Q", title=x_title, axis=alt.Axis(format=".1f")),
        y=alt.Y(
            "location:N",
            sort=alt.EncodingSortField(field="value", op="max", order="descending"),
            title=None,
            axis=alt.Axis(labelLimit=260),
        ),
        color=alt.Color(
            "flag:N",
            scale=alt.Scale(
                domain=["At or above threshold", "Below threshold / n.a."],
                range=["#E4572E", "#1F3A5F"],
            ),
            legend=alt.Legend(title=None, orient="bottom", labelLimit=300)
            if metric == SHARE
            else None,
        ),
        tooltip=[
            alt.Tooltip("location:N", title="Location"),
            alt.Tooltip("value:Q", title=unit, format=".2f"),
        ],
    )

    label_layer = alt.Chart(plot_data).mark_text(align="left", dx=6, color="#1c2f43", fontSize=11).encode(
        x=alt.X("value:Q", title=x_title),
        y=alt.Y(
            "location:N",
            sort=alt.EncodingSortField(field="value", op="max", order="descending"),
            title=None,
        ),
        text=alt.Text("value:Q", format=".2f"),
    )

    layers = chart + label_layer
    if metric == SHARE:
        layers += alt.Chart(pd.DataFrame({"v": [threshold]})).mark_rule(
            color=AMBER,
            strokeDash=[5, 4],
            size=2,
        ).encode(x="v:Q")
    if world is not None:
        layers += alt.Chart(pd.DataFrame({"v": [world]})).mark_rule(
            color=GREY,
            strokeDash=[2, 3],
            size=1.5,
        ).encode(x="v:Q")

    st.altair_chart(
        layers.properties(height=max(260, 40 * len(plot_data)), width="container"),
        use_container_width=True,
        theme=None,
    )
    st.caption(
        "Grey dotted line = world reference; amber dashed line = illustrative planner threshold."
        if metric == SHARE
        else "Grey dotted line = world reference."
    )

    if metric == SHARE:
        if not flagged.empty:
            names_txt = ", ".join(f"<b>{row.location}</b> ({row.value:.1f}%)" for row in flagged.itertuples())
            if len(flagged) == 1:
                msg = (
                    f"In {year}, {names_txt} is the only region at or above the {threshold:.1f}% threshold. "
                    "This makes it a candidate for closer assessment, although regional shares alone cannot establish local grid constraints."
                )
            else:
                msg = (
                    f"In {year}, {names_txt} are at or above the {threshold:.1f}% threshold. These are candidates for closer "
                    "assessment, although regional shares alone cannot establish local grid constraints."
                )
        else:
            msg = (
                f"No selected place reaches {threshold:.1f}% in {year}. That does not clear any local grid: "
                "averages can hide hotspots, and local network conditions still matter."
            )
        st.markdown(f'<div class="note"><strong>What this means for the planner.</strong> {msg}</div>', unsafe_allow_html=True)

    with st.expander("Trace the numbers (raw source rows)"):
        trace = df[df["location"].isin(chosen + ["World"]) & df["year"].isin([2020, year])].copy()
        st.dataframe(trace.sort_values(["location", "year"]), hide_index=True, width="stretch")
        st.caption("Share = IEA data-centre electricity / Ember total demand x 100. Change = share(year) - share(2020).")

    with st.expander("Sources, assumptions and limits"):
        st.markdown(
            f"{SOURCE}\n\n- Overlapping entities are never ranked together.\n"
            "- Only 2020 and 2023-2025 exist; gaps are not filled.\n"
            "- IEA regions exclude Eurasia.\n"
            "- Shares describe whole regions, not individual grids or sites.\n"
            "- Underlying IEA terms apply; see OWID for reuse conditions."
        )


def render_australia():
    a = pd.read_csv(AUS)
    st.markdown("### Australia spotlight")
    st.markdown(
        "Australia is **not a separate row in the global OWID file**, so this tab uses AEMO, Australia's independent energy market operator. "
        "AEMO figures cover the grid (mostly the National Electricity Market, NEM) over financial years, so they are **not like-for-like** "
        "with the OWID bars. Treat comparisons as indicative only."
    )
    st.markdown(
        '<div class="editorial-note"><strong>Australia reading:</strong> the financial-year NEM figures below are best read as indicative planning signals, not directly comparable to the global calendar-year estimates shown in the first tab.</div>',
        unsafe_allow_html=True,
    )
    only_primary = st.checkbox(
        "Only values read directly from AEMO's own page",
        value=False,
        help="Other values come from news or NGO reports of AEMO figures and should be confirmed in AEMO's documents.",
    )

    d = a[a["in_chart"] == "yes"].copy()
    if only_primary:
        d = d[d["evidence"] == "primary"]
    d = d.dropna(subset=["share_pct"]).sort_values("sort_key").reset_index(drop=True)

    now = a[a["label"].str.startswith("Mid-2026")].iloc[0]
    esoo26 = a[a["label"] == "2025-26"].iloc[0]
    esoo36 = a[a["label"] == "2035-36"].iloc[0]

    st.markdown(
        '<div class="kpis">'
        + kpi("AEMO, June 2026", f"~{now['share_pct']:.0f}%", "of grid-supplied electricity today")
        + kpi(
            "AEMO ESOO, Aug 2026",
            f"~{esoo26['share_pct']:.0f}% to ~{esoo36['share_pct']:.0f}%",
            "2025-26 to 2035-36 (Step Change)",
            alert=True,
        )
        + kpi("Operational data centres", "162", "Australia, per AEMO (Jun 2026)")
        + "</div>",
        unsafe_allow_html=True,
    )

    if d.empty:
        st.warning("No values match this filter.")
    else:
        order = d["label"].tolist()
        # Graph removed per request; the Australia spotlight now keeps the evidence in a table and summary cards only.

    st.markdown(
        '<div class="note"><strong>Why the two publications differ.</strong> AEMO\'s 2025 IASR and 2026 ESOO use different bases '
        '(grid-supplied vs operational demand) and report different dates for about 34 TWh (2050 vs 2035-36). '
        'Reports of the 2026 ISP also give almost 10% by 2050. Quote the report, year and denominator with every figure.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("Check it yourself: a simple consistency test"):
        base_twh, nem_twh = 3.9, 205
        st.markdown(
            f"{base_twh} TWh / about {nem_twh} TWh NEM consumption = **{base_twh / nem_twh * 100:.1f}%**, "
            "consistent with AEMO's 'about 2%'. The 205 TWh denominator comes from a news report of the 2026 ISP "
            "(secondary): confirm it in AEMO's ISP before using it on camera."
        )

    with st.expander("Australia data table and sources"):
        st.dataframe(a.drop(columns=["in_chart"]), hide_index=True, width="stretch")
        st.caption(
            "Evidence 'primary' = read on AEMO's own page; 'secondary' = reported by others. See data/raw/australia_sources.md."
        )
def render():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="hero"><div class="hero-tag">Energy analytics</div>'
        '<h2>Grid pressure</h2>'
        '<p>Where do data centres already take a large share of the electricity grid, and how fast is that share rising? '
        'Built for a regional infrastructure planner deciding where further investigation is warranted.</p></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="editorial-note"><strong>Planner lens:</strong> this dashboard measures all data-centre electricity demand across a region or country, not AI-only infrastructure. It is a screening tool for where further network analysis may be needed.</div>',
        unsafe_allow_html=True,
    )

    df = get_data()
    if df is None:
        return

    t1, t2 = st.tabs(["Global comparison (OWID/IEA)", "Australia spotlight (AEMO)"])
    with t1:
        render_global(df)
        st.caption(
            "Dataset last updated by OWID on 30 Jun 2026; series ends 2025; next update expected 30 Jun 2027. Checked 21 Oct 2026."
        )
    with t2:
        render_australia()
if __name__ == "__main__":
    st.set_page_config(page_title="Grid pressure", page_icon="⚡", layout="wide")
    render()
"""Member 1: Electricity comparison dashboard.

Run on its own from the project root:
    streamlit run dashboards/electricity_comparison.py
"""
from pathlib import Path
import altair as alt
import pandas as pd
import streamlit as st

DATA = Path("data/processed/owid_data_centres_share_clean.csv")
RAW = Path("data/raw/data-centers-share-electricity-demand.csv")
TYPE_COLOURS = {"Country": "#0072B2", "Region": "#E69F00", "Aggregate": "#7F7F7F"}


MY_TAKEAWAY = "In 2025, data centres account for about 4.9% of electricity demand in the United States, roughly 3.2 times the world figure of 1.5%. North America (4.1%) and Europe (1.9%) also sit above the world figure, while China (1.1%), Asia Pacific (1.1%) and the remaining regions fall below it. The highest share is over 40 times the lowest, so a single global figure hides large differences between places. This supports looking at location, but these are estimated shares of demand for data centres in general, not AI alone, and they say nothing about any single facility."


def stretch(fn, *args, **kwargs):
    """Full-width display that works on both newer and older Streamlit versions."""
    try:
        return fn(*args, width="stretch", **kwargs)
    except Exception:
        return fn(*args, use_container_width=True, **kwargs)


@st.cache_data
def load() -> pd.DataFrame:
    return pd.read_csv(DATA)


@st.cache_data
def load_raw() -> pd.DataFrame | None:
    return pd.read_csv(RAW) if RAW.exists() else None


def build_chart(d: pd.DataFrame, year: int, world: float | None) -> alt.Chart:
    d = d.copy()
    d["value_label"] = d["share_pct"].map(lambda v: f"{v:.1f}%")
    # Explicit order: automatic sorting breaks once the reference line is layered on.
    order = list(d.sort_values("share_pct", ascending=False)["label"])
    base = alt.Chart(d).encode(
        y=alt.Y("label:N", sort=order, title=None,
                axis=alt.Axis(labelLimit=400)),
        x=alt.X("share_pct:Q", title="Share of total electricity demand",
                scale=alt.Scale(domain=[0, float(d["share_pct"].max()) * 1.15]),
                axis=alt.Axis(values=list(range(0, int(d["share_pct"].max() * 1.15) + 1)),
                              labelExpr="datum.label + '%'")),
    )
    bars = base.mark_bar().encode(
        color=alt.Color("entity_type:N", title="Type",
                        scale=alt.Scale(domain=list(TYPE_COLOURS),
                                        range=list(TYPE_COLOURS.values()))))
    text = base.mark_text(align="left", dx=4, fontSize=13).encode(text="value_label:N")
    layers = bars + text
    subtitle = ""
    if world is not None:
        ref = pd.DataFrame({"x": [world]})
        rule = alt.Chart(ref).mark_rule(color="#222222", strokeDash=[5, 4],
                                        strokeWidth=2).encode(x="x:Q")
        layers = layers + rule
        subtitle = f"Dashed line = World figure ({world:.1f}%)"
    title = alt.TitleParams(
        text=f"Data-centre share of electricity demand, {year} (IEA estimates)",
        subtitle=subtitle)
    # One fixed-size band per entity, so labels never get skipped or squashed.
    chart = layers.properties(title=title, height=alt.Step(36))
    return (chart.configure_axis(labelFontSize=13, titleFontSize=14)
                 .configure_legend(labelFontSize=13, titleFontSize=13)
                 .configure_title(fontSize=16, subtitleFontSize=13))


def render() -> None:
    df = load()
    st.header("Where do data centres take the largest share of electricity demand?")

    years = sorted(df["year"].unique())
    c1, c2 = st.columns([1, 3])
    year = c1.selectbox("Year", years, index=len(years) - 1,
                        help="The source reports only these years.")
    types = c2.multiselect("Entity types", ["Country", "Region", "Aggregate"],
                           default=["Country", "Region"])

    # World figure always comes from the full file, not from the filtered selection.
    w = df[(df["year"] == year) & (df["entity"] == "World")]["share_pct"]
    world = float(w.iloc[0]) if len(w) else None

    pool = df[(df["year"] == year) & (df["entity_type"].isin(types))].copy()
    pool["label"] = pool["entity_clean"] + " (" + pool["entity_type"].str.lower() + ")"
    chosen = st.multiselect("Entities", sorted(pool["label"]),
                            default=sorted(pool["label"]))
    d = pool[pool["label"].isin(chosen)].sort_values("share_pct", ascending=False)

    if d.empty:
        st.info("No data for this selection. Choose at least one entity.")
        return

    if world:
        d["times_world"] = d["share_pct"] / world

    
    if MY_TAKEAWAY.strip():
        st.markdown(f"**Takeaway:** {MY_TAKEAWAY}")
    else:
        hi, lo = d.iloc[0], d.iloc[-1]
        ratio = (f", {hi['times_world']:.1f} times the world figure of {world:.1f}%"
                 if world else "")
        st.markdown(f"**Draft takeaway (replace with your own):** in {year}, "
                    f"{hi['label']} is highest at {hi['share_pct']:.1f}%{ratio}; "
                    f"{lo['label']} is lowest at {lo['share_pct']:.1f}%.")

    stretch(st.altair_chart, build_chart(d, year, world))
    st.caption(f"Estimates by the IEA, processed by Our World in Data. Covers data "
               f"centres generally, not AI workloads alone. Observation year: {year}. "
               f"Source reports only {', '.join(str(y) for y in years)}.")
    if {"Country", "Region"} <= set(d["entity_type"]):
        st.caption("Regions contain countries shown here (North America includes the "
                   "United States; Asia Pacific includes China). Do not add bars together.")

    st.subheader("Values shown")
    cols = ["entity_clean", "entity_type", "year", "share_pct"]
    names = {"entity_clean": "Entity", "entity_type": "Type", "year": "Year",
             "share_pct": "Share (%)", "times_world": "Times world figure"}
    if world:
        cols.append("times_world")
    shown = d[cols].rename(columns=names)
    shown["Year"] = shown["Year"].astype(str)  # avoids "2,025" formatting
    stretch(st.dataframe, shown, hide_index=True,
            column_config={"Share (%)": st.column_config.NumberColumn(format="%.2f"),
                           "Times world figure": st.column_config.NumberColumn(format="%.1f")})
    st.caption("Times world figure = entity share divided by the World share for the "
               "same year. It is a ratio, not a percentage-point difference.")

    with st.expander("Check a value against the original file"):
        raw = load_raw()
        pick = st.selectbox("Entity", list(d["label"]), key="verify")
        row = d[d["label"] == pick].iloc[0]
        if raw is None:
            st.warning(f"Original file not found at {RAW}.")
        else:
            match = raw[(raw["Entity"] == row["entity"]) & (raw["Year"] == row["year"])]
            st.write("Row in the original download:")
            stretch(st.dataframe, match.astype(str), hide_index=True)
            st.write(f"Shown on chart: {row['share_pct']:.1f}% "
                     f"(full value {row['share_pct']})")

    with st.expander("Source, units and limitations"):
        st.markdown(
            "- **Source:** IEA (2025) and Ember (2026), processed by Our World in Data.\n"
            "- **Unit:** percent of total electricity demand. Values are estimates.\n"
            "- **Years available:** 2020, 2023, 2024, 2025 (no 2021-2022).\n"
            "- **Limit:** covers data centres generally, not AI workloads alone, and "
            "national or regional shares do not describe any single facility.\n"
            "- **Downloaded:** 18 October 2026.")


if __name__ == "__main__":
    st.set_page_config(page_title="Electricity comparison", layout="wide")
    render()
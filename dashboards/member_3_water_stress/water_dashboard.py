"""Standalone dashboard; call render_water_dashboard(countries=[ISO3, ...]) in Part 2."""
from pathlib import Path
import json
import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
SOURCE = 'https://www.wri.org/data/aqueduct-40-country-rankings'

@st.cache_data
def load_data():
    return pd.read_csv(ROOT / 'data/processed/water_stress.csv')

def filter_data(df, countries, regions, categories):
    return df.loc[df.iso3.isin(countries) & df.region.isin(regions) & df.risk_category.isin(categories) & df.has_score].copy()

def render_water_dashboard(countries=None, key_prefix='water'):
    df = load_data()
    meta = json.loads((ROOT / 'data/metadata.json').read_text(encoding='utf-8'))
    valid = df.loc[df.has_score].copy()
    st.markdown('''<style>
    .stApp {background:#f5f8fa;color:#152e3a;}
    .block-container {max-width:1180px;padding-top:4rem;}
    h1,h2,h3 {letter-spacing:-.035em;}
    [data-testid="stMetric"] {background:white;border:1px solid #dbe5e9;border-radius:12px;padding:16px;}
    [data-testid="stMetricValue"] {color:#087f8c;}
    </style>''', unsafe_allow_html=True)
    st.caption('POWERING AI  /  WATER EVIDENCE  /  AQUEDUCT 4.0')
    st.title('Water, before expansion')
    st.markdown('### Which countries face greater baseline water stress?')
    st.write('Compare national water conditions before drawing conclusions about where infrastructure should grow.')
    st.caption('Group question: Should data-centre expansion supporting AI be assessed against local electricity and water constraints rather than global averages?')
    st.caption('Audience: an infrastructure policy adviser considering location-specific expansion guidelines.')

    a,b,c = st.columns(3)
    a.metric('Countries / territories with scores', len(valid))
    b.metric('High or extremely high stress', int((valid.category_code >= 3).sum()))
    c.metric('Baseline reference period', '1979–2019')
    st.caption(f'Whole-dataset overview · total-demand weighting · {len(df)-len(valid)} records without a valid stress score excluded from counts and charts.')
    st.info('Water conditions vary across the dataset. This supports screening by location, but national scores cannot determine whether a particular data-centre site is suitable.')

    with st.expander('Understand the measure', expanded=False):
        st.write('Baseline water stress describes demand relative to available renewable water supply. The country score is a demand-weighted aggregation of basin-level indicator scores, on a dimensionless 0–5 scale. It is not a percentage and should not be multiplied by 20 to create one.')
        st.write('WRI’s category labels include underlying stress bands (<10%, 10–20%, 20–40%, 40–80%, >80%). These labels describe the indicator framework; the national score is not a directly measured national withdrawal percentage.')
        st.write('Total gross water demand weighting is used throughout. Baseline conditions use 1979–2019 data, released in Aqueduct 4.0 in 2023; this is not a 2026 observation or a live drought reading.')

    st.divider()
    st.subheader('Compare water stress')
    st.caption('Start with all scored countries; select the countries used by your electricity teammates when the shared scope is agreed.')
    options = df.sort_values('country').iso3.tolist()
    names = dict(zip(df.iso3, df.country))
    if countries is None:
        show_all = st.checkbox('Include all countries / territories', value=True, key=f'{key_prefix}_all')
        if show_all:
            chosen = options
        else:
            chosen = st.multiselect('Countries / territories', options, default=[x for x in ['AUS','IND','USA','CHN','IRL'] if x in options], format_func=lambda x:names[x], key=f'{key_prefix}_countries')
    else:
        chosen = [x for x in countries if x in options]
        st.caption('Country selection supplied by the group narrative app.')
    left,right = st.columns(2)
    regions = sorted(valid.region.dropna().unique())
    categories = valid.sort_values('category_code').risk_category.drop_duplicates().tolist()
    picked_regions = left.multiselect('Regions', regions, default=regions, key=f'{key_prefix}_regions')
    picked_categories = right.multiselect('Risk categories', categories, default=categories, key=f'{key_prefix}_categories')
    controls = st.columns([2,1])
    order = controls[0].radio('Order countries', ['Highest stress first','Lowest stress first','Alphabetical'], horizontal=True, key=f'{key_prefix}_order')
    limit = controls[1].selectbox('Chart rows', [15,30,'All'], key=f'{key_prefix}_limit')
    result = filter_data(df, chosen, picked_regions, picked_categories)
    missing = df.loc[df.iso3.isin(chosen) & ~df.has_score, 'country'].tolist()
    if missing:
        with st.expander(f'{len(missing)} selected records have no valid score'):
            st.write('No valid baseline score for: ' + ', '.join(missing) + '. These records are retained in the source package, not plotted as zero.')
    if result.empty:
        st.warning('No countries match these filters. Select at least one country, region and risk category.')
    else:
        result = result.sort_values('country' if order == 'Alphabetical' else 'stress_score', ascending=order != 'Highest stress first')
        plot = result if limit == 'All' else result.head(limit)
        high = result.sort_values('stress_score',ascending=False).iloc[0]
        low = result.sort_values('stress_score').iloc[0]
        st.markdown(f'**In this selection:** {len(result)} countries / territories; scores range from **{low.stress_score:.2f}** ({low.country}) to **{high.stress_score:.2f}** ({high.country}). Equal scores may be tied.')
        st.caption(f'Chart shows {len(plot)} of {len(result)} matching records, ordered as selected. Full matching values are in the table below.')
        chart = alt.Chart(plot).encode(y=alt.Y('country:N',sort=plot.country.tolist(),title=None),x=alt.X('stress_score:Q',scale=alt.Scale(domain=[0,5.45],nice=False),title='Baseline water-stress score (dimensionless, 0–5)',axis=alt.Axis(values=[0,1,2,3,4,5])))
        bars = chart.mark_bar(color='#087f8c',cornerRadiusEnd=3,size=15)
        labels = chart.mark_text(align='left',dx=7,color='#152e3a',fontSize=12).encode(text=alt.Text('stress_score:Q',format='.2f'))
        st.altair_chart((bars+labels).properties(height=max(180,len(plot)*29),title='Baseline water stress by country / territory · total-demand weighting').configure_view(stroke=None),width='stretch')
        st.caption('Longer bars indicate greater baseline stress. A single colour avoids relying on colour perception to distinguish risk; the table states every category.')
        view = result[['country','iso3','stress_score','risk_category','region']].rename(columns={'country':'Country / territory','iso3':'ISO3','stress_score':'Score (0–5)','risk_category':'WRI risk category','region':'UN region'})
        st.dataframe(view,hide_index=True,width='stretch',column_config={'Score (0–5)':st.column_config.NumberColumn(format='%.4f')})
        st.download_button('Download matching data (CSV)',result.to_csv(index=False),'water_stress_selection.csv','text/csv',key=f'{key_prefix}_download')

    st.divider()
    st.subheader('Trace a number to its source')
    st.write('Use this panel during your recording: displayed score → processed record → source spreadsheet row.')
    verify_options = result.iso3.tolist() if not result.empty else valid.iso3.tolist()
    selected = st.selectbox('Country to verify',verify_options,format_func=lambda x:names[x],key=f'{key_prefix}_verify')
    row = df.loc[df.iso3 == selected].iloc[0]
    raw = pd.read_csv(ROOT / 'data/raw/country_baseline_bws_tot.csv')
    original = raw.loc[raw.gid_0 == selected].iloc[0]
    st.markdown(f'**{row.country}: {row.stress_score:.4f} / 5** · {row.risk_category}')
    st.caption(f'Original workbook: {meta["workbook_member"]} · sheet: country_baseline · Excel row {int(row.source_excel_row)}')
    evidence = pd.DataFrame({'Original field':original.index,'Source value':[str(v) for v in original.values]})
    st.dataframe(evidence,hide_index=True,width='stretch',height=425)
    st.code(f'Filter indicator_name == "bws" and weight == "Tot"\nMatch gid_0 == "{selected}"\nRead score = {float(original.score)}\nRename score → stress_score; no rescaling or imputation\nDisplay rounded to 2 decimals: {row.stress_score:.2f}')
    if abs(float(original.score)-float(row.stress_score)) < 1e-12:
        st.success('Verification passed: the processed score matches the saved source record.')
    else:
        st.error('Verification failed: source and processed scores differ.')
    with st.expander('Download original evidence and processing instructions'):
        st.download_button('Official WRI workbook archive (ZIP)',(ROOT/'data/raw/aqueduct-4-0-country-rankings.zip').read_bytes(),'aqueduct-4-0-country-rankings.zip',key=f'{key_prefix}_zip')
        st.download_button('Source sample (CSV)',(ROOT/'data/raw/country_baseline_bws_tot.csv').read_bytes(),'country_baseline_bws_tot.csv',key=f'{key_prefix}_sample')
        st.code('python scripts/prepare_data.py')
        st.caption('The source sample is extracted from the unchanged workbook archive; regenerate it and the processed file with the command above.')

    st.subheader('What this means for the group story')
    st.write('Water stress is an additional screening consideration alongside electricity demand. Compare the same countries in the electricity chapters, then investigate drought risk and local conditions before proposing site-level decisions.')
    st.warning('These data do not measure AI water consumption, identify data-centre locations, or show that AI caused water stress. National aggregates hide basin differences. Water stress alone is not a complete assessment of cooling technology, water supply, permits or infrastructure suitability.')
    with st.expander('Design decision and AI disclosure'):
        st.markdown('**Visual task:** compare and rank country scores. **Chosen form:** horizontal bars with a fixed 0–5 scale and direct labels. **Alternative rejected:** a choropleth map, because area and location would compete with the precise comparisons this dashboard serves.')
        st.write('AI assistance: Codex generated the dashboard, transformation script and documentation. Checks applied: source/processed score equality, valid score range, country-key uniqueness, deterministic regeneration, and interaction checks. See docs/AI_PROVENANCE.csv for recorded results. The student must review the work, add their name and record any further substantive AI uses before submission.')
    st.divider()
    st.caption(f'Source: WRI Aqueduct 4.0 · baseline 1979–2019 · source retrieved / last local data refresh: {meta["retrieved"]} · CC BY 4.0. Retrieval date is not the observation year.')
    st.markdown(f'[Official dataset]({SOURCE}) · [WRI country data dictionary](https://github.com/wri/Aqueduct40/blob/master/data_dictionary_country-rankings.md) · [Methodology](https://doi.org/10.46830/writn.23.00061)')

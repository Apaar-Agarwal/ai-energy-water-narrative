"""Four member contributions adapted into one evidence-led scrolling story."""
from pathlib import Path
import json
import altair as alt
import pandas as pd
import streamlit as st

ROOT=Path(__file__).resolve().parent
COLOURS=['#0072B2','#D55E00','#009E73','#CC79A7','#332288','#8C564B']

@st.cache_data
def load_data():
    return (pd.read_csv(ROOT/'data/processed/story_electricity.csv'),
            pd.read_csv(ROOT/'data/processed/story_water.csv'),
            json.loads((ROOT/'data/processed/story_metadata.json').read_text(encoding='utf-8')))

@st.cache_data
def load_source_csv(relative_path):
    return pd.read_csv(ROOT/relative_path)

def table(data,key):
    st.dataframe(data,hide_index=True,width='stretch')
    st.download_button('Download these values',data.to_csv(index=False),f'{key}.csv','text/csv',key=key)

def style(chart):
    return chart.configure_view(stroke=None).configure_axis(labelFontSize=12,titleFontSize=12).configure_legend(orient='top',labelFontSize=12)

def chapter_one(e,year,countries):
    st.caption('01 / ELECTRICITY COMPARISON · BRIGHTY')
    st.header('A world average hides different electricity burdens')
    st.write('First compare the share of electricity demand attributed to data centres. A high share is a reason to investigate network conditions; it is not proof of grid congestion.')
    scope=st.radio('Compare at one geographic level',['Countries','IEA regions'],horizontal=True,key='comparison_scope')
    d=e.loc[(e.year==year)&(e.entity_type==('Country' if scope=='Countries' else 'Region'))].copy()
    if scope=='Countries':
        d=d.loc[d.iso3.isin(countries)]
    if d.empty:
        st.info('No electricity observations match this selection. Select a country in the shared controls.')
        return
    d=d.sort_values('share_pct',ascending=False)
    world=float(e.loc[(e.entity=='World')&(e.year==year),'share_pct'].iloc[0])
    d['label']=d.share_pct.map(lambda x:f'{x:.2f}%')
    base=alt.Chart(d).encode(y=alt.Y('name:N',sort=d.name.tolist(),title=None),x=alt.X('share_pct:Q',title='Data-centre share of total electricity demand (%)',scale=alt.Scale(domain=[0,max(d.share_pct.max(),world)*1.22],nice=False)))
    bars=base.mark_bar(color=COLOURS[0],size=23)
    labels=base.mark_text(align='left',dx=6).encode(text='label:N')
    rule=alt.Chart(pd.DataFrame({'reference':[world]})).mark_rule(color='#555555',strokeDash=[5,4]).encode(x='reference:Q')
    st.altair_chart(style((bars+labels+rule).properties(height=max(180,len(d)*43),title=f'Electricity-demand share, {year} · IEA estimates via OWID')),width='stretch')
    st.caption(f'Dashed line: world reference {world:.2f}%. Year {year}; percentages are already in source units. Regions and countries overlap, so they are shown separately and must not be added.')
    leader=d.iloc[0]
    st.markdown(f'**What to notice:** {leader["name"]} has the highest share in this view at **{leader.share_pct:.2f}%**, compared with **{world:.2f}%** worldwide. This is a share of each location’s demand, not a share of global data-centre electricity.')
    table(d[['name','year','share_pct']].rename(columns={'name':'Location','year':'Year','share_pct':'Electricity share (%)'}),'electricity_comparison')

def chapter_two(e,year,countries):
    st.caption('02 / CHANGE IN GRID SHARE · SANJAI')
    st.header('The starting point and the trajectory both matter')
    st.write('The previous chart is a snapshot. Now examine how the share has changed since the earliest available observation: places with the largest shares need not have the fastest increases.')
    scope=st.radio('Trend geography',['Shared countries','IEA regions'],horizontal=True,key='trend_scope')
    if scope=='Shared countries':
        names=e.loc[(e.entity_type=='Country')&e.iso3.isin(countries),'entity'].unique().tolist()
    else:
        names=e.loc[e.entity_type=='Region','entity'].unique().tolist()
    d=e.loc[e.entity.isin(names)&(e.year<=year)].copy()
    if d.empty:
        st.info('No trend data for this selection.')
        return
    d=d.sort_values(['entity','year'])
    d['label']=d.share_pct.map(lambda x:f'{x:.2f}')
    colour=alt.Color('name:N',title='Location',scale=alt.Scale(range=COLOURS))
    base=alt.Chart(d).encode(x=alt.X('year:Q',title='Observation year (2021–2022 absent)',scale=alt.Scale(zero=False),axis=alt.Axis(values=sorted(d.year.unique().tolist()),format='d')),y=alt.Y('share_pct:Q',title='Data-centre share of electricity demand (%)',scale=alt.Scale(zero=True)),color=colour)
    line=base.mark_line(point=True,strokeWidth=2).encode(strokeDash=alt.StrokeDash('name:N',legend=None))
    text=base.mark_text(dy=-12,fontSize=11).encode(text='label:N')
    st.altair_chart(style((line+text).properties(height=320,title=f'Observed years in the source snapshot · through {year}')),width='stretch')
    st.caption('Lines connect available estimates to aid comparison; they do not supply missing annual values. Point positions preserve elapsed-time spacing. No projections are included.')
    baseline=e.loc[(e.year==2020)&e.entity.isin(names),['entity','share_pct']].rename(columns={'share_pct':'baseline'})
    changes=d.loc[d.year==year].merge(baseline,on='entity',validate='one_to_one')
    changes['change_pp']=changes.share_pct-changes.baseline
    if len(changes):
        high=changes.sort_values('change_pp',ascending=False).iloc[0]
        st.markdown(f'**What changed:** {high["name"]} shows the largest increase in this selection: **{high.change_pp:+.2f} percentage points** from 2020 to {year}. A percentage-point difference subtracts shares; it is not percentage growth.')
    threshold=st.slider('Illustrative attention threshold (% of electricity demand)',0.5,6.0,3.0,0.5,key='attention_threshold')
    flagged=changes.loc[changes.share_pct>=threshold,'name'].tolist()
    st.caption(f'At or above your {threshold:.1f}% screening line in {year}: '+(', '.join(flagged) if flagged else 'none of the selected locations')+'. This user-selected line is not a regulatory or scientific limit.')
    table(d[['name','year','share_pct']].rename(columns={'name':'Location','year':'Year','share_pct':'Electricity share (%)'}),'electricity_trends')
    table(changes[['name','baseline','share_pct','change_pp']].rename(columns={'name':'Location','baseline':'Baseline 2020 (%)','share_pct':f'Selected {year} (%)','change_pp':'Change (percentage points)'}),'electricity_change')
    with st.expander('Why the Australia spotlight is not in this comparison'):
        st.write('Sanjai also supplied an AEMO Australia spotlight. Its material is preserved in contributors/Sanjai/submission_materials. It combines financial years, national and NEM scopes, report editions and projection horizons. It is not merged with OWID’s calendar-year shares. Adding it as an evidence chapter would expand the agreed two-dataset scope and requires source-by-source verification. The grid-share/change contribution is integrated above.')

def water_selection(w,countries):
    st.info('The electricity source has country figures for the US and China only. Shared mode compares those same countries; additional water countries have no matching country-level electricity figure in this snapshot.')
    mode=st.radio('Water-country scope',['Shared electricity countries','Explore more water countries'],horizontal=True,key='water_scope')
    if mode=='Shared electricity countries':
        selected=countries
    else:
        mapping=dict(zip(w.iso3,w.country))
        defaults=[x for x in ['USA','CHN','IRL','GBR','DEU','NLD','FRA','JPN','AUS','IND'] if x in mapping]
        selected=st.multiselect('Additional water comparison',w.iso3.tolist(),default=defaults,format_func=lambda x:mapping[x],key='water_countries')
    return w.loc[w.iso3.isin(selected)].copy()

def chapter_three(selected):
    st.caption('03 / BASELINE WATER STRESS · APAAR')
    st.header('Electricity alone does not describe water constraints')
    st.write('Water stress adds a different consideration: demand relative to renewable supply, expressed here as a weighted national score. The baseline is 1979–2019, not the electricity observation year.')
    valid=selected.dropna(subset=['bws_score']).sort_values('bws_score',ascending=False)
    missing=selected.loc[selected.bws_score.isna(),'country'].tolist()
    if missing:
        st.warning('No water-stress score: '+', '.join(missing)+'. Missing is not zero.')
    if valid.empty:
        st.info('No water-stress scores match this selection.')
        return
    valid=valid.copy();valid['label']=valid.bws_score.map(lambda x:f'{x:.2f}')
    base=alt.Chart(valid).encode(y=alt.Y('country:N',sort=valid.country.tolist(),title=None),x=alt.X('bws_score:Q',title='Baseline water-stress score (dimensionless, 0–5)',scale=alt.Scale(domain=[0,5.45],nice=False),axis=alt.Axis(values=[0,1,2,3,4,5])))
    st.altair_chart(style((base.mark_bar(color='#009E73',size=21)+base.mark_text(align='left',dx=6).encode(text='label:N')).properties(height=max(180,len(valid)*35),title='National baseline water stress · total-demand weighting')),width='stretch')
    st.caption('Aqueduct 4.0 water-stress indicator. Country scores aggregate basin-level scores weighted by total gross demand. Scores are not percentages or measured AI water consumption.')
    st.markdown(f'**What this adds:** selected scores range from **{valid.bws_score.min():.2f} to {valid.bws_score.max():.2f}**. National differences support further assessment; they do not locate vulnerable facilities or establish suitable cooling technology.')
    table(selected[['country','bws_score','bws_label']].rename(columns={'country':'Country','bws_score':'Water-stress score (0–5)','bws_label':'WRI category'}),'water_stress')

def chapter_four(w,selected):
    st.caption('04 / DROUGHT AND FLOOD RISK · HARSH')
    st.header('Low water stress can still leave another risk')
    st.write('Baseline stress and drought risk describe different things. Could a stress-only screen miss other concerns? Compare the indicators as an exploratory association, not a prediction of data-centre impacts.')
    choice=st.radio('Additional water indicator',['Drought risk','Riverine flood risk'],horizontal=True,key='water_indicator')
    prefix='drr' if choice=='Drought risk' else 'rfr'
    ys=f'{prefix}_score'
    all_pairs=w.dropna(subset=['bws_score',ys])
    low=all_pairs.loc[all_pairs.bws_score<2]
    elevated=low.loc[low[ys]>=2]
    st.markdown(f'**Whole-file check:** among **{len(all_pairs)}** countries/territories with both scores, **{len(elevated)} of {len(low)}** have a water-stress score below 2 and a {choice.lower()} score of at least 2.')
    st.caption('Denominator excludes countries missing either indicator. These thresholds group weighted scores; they do not assert that a national withdrawal ratio is below 20%.')
    context=st.checkbox('Show other countries as context',True,key='scatter_context')
    plot=(w if context else selected).dropna(subset=['bws_score',ys]).copy()
    if selected.empty:
        st.info('Select at least one country to explore the water relationship.')
        return
    if plot.empty:
        st.info('No paired scores match this selection.')
        return
    plot['group']=plot.iso3.isin(selected.iso3).map({True:'Selected country',False:'Context country'})
    base=alt.Chart(plot).encode(x=alt.X('bws_score:Q',title='Baseline water-stress score (0–5)',scale=alt.Scale(domain=[0,5.35],nice=False)),y=alt.Y(f'{ys}:Q',title=f'{choice} score (0–5)',scale=alt.Scale(domain=[0,5.35],nice=False)))
    points=base.mark_point(size=85,strokeWidth=1.5).encode(color=alt.Color('group:N',title='Country set',scale=alt.Scale(domain=['Selected country','Context country'],range=['#0072B2','#888888'])),shape=alt.Shape('group:N',title='Country set',scale=alt.Scale(domain=['Selected country','Context country'],range=['diamond','circle'])))
    labels=alt.Chart(plot.loc[plot.iso3.isin(selected.iso3)]).mark_text(dx=7,dy=-8,align='left',fontSize=11,color='#173342').encode(x='bws_score:Q',y=f'{ys}:Q',text='country:N')
    zone=alt.Chart(pd.DataFrame({'x':[0],'x2':[2],'y':[2],'y2':[5]})).mark_rect(color='#D55E00',opacity=.07).encode(x='x:Q',x2='x2:Q',y='y:Q',y2='y2:Q')
    st.altair_chart(style((zone+points+labels).properties(height=360,title=f'National stress versus {choice.lower()} · different indicator vintages')),width='stretch')
    st.caption('Shaded zone: water-stress score <2 and additional-risk score ≥2. Diamonds identify selected countries; hollow circles supply optional context. Full scores are readable in the table below without hovering.')
    st.caption('Water stress: Aqueduct 4.0, 1979–2019 baseline; drought and riverine flood: inherited Aqueduct 3.0 indicators with their own model/reference periods. Drought uses total-demand weighting; riverine flood uses population weighting. Scores are dimensionless; equal numbers do not mean equal physical impacts.')
    missing=selected.loc[selected.bws_score.isna()|selected[ys].isna(),'country'].tolist()
    if missing:
        st.warning('Selected countries not plotted because one or both scores are missing: '+', '.join(missing))
    scored=selected.dropna(subset=['bws_score',ys])
    n=int(((scored.bws_score<2)&(scored[ys]>=2)).sum())
    st.markdown(f'**Within your selection:** {n} of {len(scored)} countries with paired scores fall in the shaded zone. A low stress score alone is insufficient to describe all water risks.')
    table(plot[['country','bws_score',ys]].rename(columns={'country':'Country','bws_score':'Water-stress score (0–5)',ys:f'{choice} score (0–5)'}),'water_relationship')

def evidence(e,w):
    st.header('Follow a number back to its source')
    with st.expander('Inspect source records and transformations'):
        kind=st.radio('Evidence source',['Electricity','Water'],horizontal=True,key='evidence_kind')
        if kind=='Electricity':
            entity=st.selectbox('Source entity',e.entity.unique().tolist(),key='trace_entity')
            year=st.selectbox('Source observation year',sorted(e.year.unique().tolist()),key='trace_year')
            row=e.loc[(e.entity==entity)&(e.year==year)]
            raw=load_source_csv('data/raw/data-centers-share-electricity-demand.csv')
            match=raw.loc[(raw.Entity==entity)&(raw.Year==year)]
            st.dataframe(match.T.astype(str).rename(columns={match.index[0]:'Original value'}),width='stretch')
            st.caption(f'Raw CSV row {int(row.source_csv_row.iloc[0])}, including header. Value is already a percentage; rename only, no interpolation. Source matches processed: {float(match.iloc[0,-1]) == float(row.share_pct.iloc[0])}.')
        else:
            mapping=dict(zip(w.iso3,w.country))
            country=st.selectbox('Source country',w.iso3.tolist(),format_func=lambda x:mapping[x],key='trace_country')
            raw=load_source_csv('data/raw/story_country_baseline_sample.csv')
            match=raw.loc[(raw.gid_0==country)&(((raw.indicator_name.isin(['bws','drr']))&(raw.weight=='Tot'))|((raw.indicator_name=='rfr')&(raw.weight=='Pop')))]
            for r in match.itertuples():
                st.markdown(f'**{r.indicator_name} / {r.weight}** · workbook sheet country_baseline · Excel row {r.source_excel_row}')
                st.write({'source score':r.score,'source category':r.label})
            st.caption('Filter bws/Tot, drr/Tot, rfr/Pop; replace -9999 with missing; join by country code. Repair display-name encoding only. Scores are not rescaled. The unchanged workbook is saved in data/raw.')

def conclusion(e,w,year,countries,selected):
    st.caption('SYNTHESIS / THE PLANNING DECISION')
    st.header('Use location-specific assessment, not a universal verdict')
    st.write('**Our answer: the evidence supports location-specific screening rather than relying on global averages.** Electricity-demand shares differ between places and over time, while water-stress and drought indicators add distinct concerns. The evidence does not establish a universal constraint threshold or justify approving or rejecting a particular site.')
    st.write('**A reasonable alternative interpretation:** national screening measures are too coarse to constrain expansion. Facility cooling choices, water sourcing, local grid capacity and mitigation could matter more than national averages. The same evidence can therefore support further investigation rather than limits.')
    lookup=e.loc[(e.year==year)&(e.entity_type=='Country'),['iso3','share_pct']]
    summary=selected[['iso3','country','bws_score','drr_score']].merge(lookup,on='iso3',how='left',validate='one_to_one')
    if len(summary):
        summary=summary.rename(columns={'iso3':'ISO3','country':'Country','bws_score':'Stress score (0–5)','drr_score':'Drought score (0–5)','share_pct':f'Electricity share {year} (%)'})
        st.dataframe(summary.drop(columns='ISO3'),hide_index=True,width='stretch')
    st.caption('Blank electricity values mean no country-level observation in this snapshot. Water indicators use different vintages; this is a contextual comparison, not a synchronized country-year model. No combined sustainability score is calculated.')
    st.warning('What the data cannot show: AI-only electricity or water use; facility-level consumption; current drought; grid congestion; causation; local catchment suitability; or whether mitigation would change a site decision. Missing observations are never replaced with zero.')

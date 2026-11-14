"""Editorial investigation with a persistent country, linked charts and evidence reveal."""
from html import escape
import altair as alt
import pandas as pd
import streamlit as st
from story import load_data,evidence

INK='#173B3F'; TEAL='#087F83'; ORANGE='#C66435'
CSS='''<style>
.stApp,[data-testid="stAppViewContainer"]{background:#faf8f3;color:#173b3f}
[data-testid="stHeader"]{background:rgba(250,248,243,.94)}
.block-container{max-width:1120px;padding:3rem 2.7rem 4rem}
h1,h2,h3{color:#173b3f;letter-spacing:-.035em;line-height:1.14!important}
h1{font-family:Georgia,serif!important;font-size:3.9rem!important;font-weight:500!important}
h2{font-family:Georgia,serif!important;font-size:2.35rem!important;font-weight:500!important;margin:.2rem 0 .6rem!important}
h3{font-size:1.2rem!important}p,li{line-height:1.65}
.eyebrow{font:700 .67rem/1.5 'Segoe UI',sans-serif;letter-spacing:.18em;text-transform:uppercase;color:#087f83;margin-bottom:1rem}
.masthead{border-top:2px solid #173b3f;padding-top:1rem;display:flex;justify-content:space-between;font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;margin-bottom:1.8rem}
.deck{font-size:1.1rem;color:#526b69;max-width:48rem;line-height:1.7}
.hero-number{font-family:Georgia,serif;font-size:5.7rem;line-height:1;color:#087f83;letter-spacing:-.07em}
.hero-label{font-size:.73rem;letter-spacing:.06em;text-transform:uppercase;color:#637573;margin-top:.55rem}
.lede{border-left:3px solid #087f83;padding:.3rem 0 .3rem 1.25rem;margin:1.4rem 0 2rem;font-size:1.12rem;line-height:1.6}
.chapter-marker{display:flex;gap:.8rem;align-items:center;margin:3rem 0 1rem;border-top:1px solid #dfe5df;padding-top:1.5rem;font-size:.7rem;letter-spacing:.17em;text-transform:uppercase;color:#637573}
.chapter-marker b{display:inline-grid;place-items:center;width:2.1rem;height:2.1rem;border:1px solid #bdceca;border-radius:50%;font-size:.77rem;color:#087f83}
.takeaway{background:#e9f1ed;border:1px solid #d5e4db;padding:1.1rem 1.3rem;border-radius:5px;margin:.8rem 0 1rem;line-height:1.65}.takeaway strong{color:#075d61}
.bridge{font-family:Georgia,serif;font-size:1.45rem;line-height:1.6;color:#607570;margin:2rem 0 .7rem;max-width:43rem}
.reveal{background:#173b3f;color:#f7f7ee;border-radius:8px;padding:1.7rem 1.8rem;margin:2rem 0 1rem}.reveal h3{color:#fff!important;font-family:Georgia,serif;font-size:1.8rem!important}.reveal p{color:#d8e6e0;margin-bottom:0}
.tag{display:inline-block;border:1px solid #cddbd4;border-radius:30px;padding:.25rem .65rem;font-size:.68rem;margin:.3rem .4rem .3rem 0;color:#55706b}
.smallprint{font-size:.75rem;color:#526b69;line-height:1.6}
.case-card{border:1px solid #cadbd4;background:white;border-radius:8px;padding:1.2rem 1.3rem;margin:1rem 0;min-height:210px}.case-value{font-family:Georgia,serif;font-size:2.8rem;letter-spacing:-.05em;color:#087f83}.case-label{font-size:.7rem;color:#647874;text-transform:uppercase;letter-spacing:.08em}
section[data-testid="stSidebar"]{background:#173b3f}
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"]{color:#eef5ef}
section[data-testid="stSidebar"] label p{color:#dce9e1!important;font-size:.8rem}
.side-eyebrow{font-size:.65rem;color:#a7ccc1;letter-spacing:.17em;margin:1.2rem 0 .4rem}.side-title{font-family:Georgia,serif;font-size:1.8rem;color:#fff;margin-bottom:.7rem}
.side-stat{padding:.8rem 0;border-top:1px solid #46615f}.side-stat span{display:block;font-size:.7rem;color:#abc7bd}.side-stat strong{font-family:Georgia,serif;font-size:1.55rem;font-weight:400;color:#fff}.side-note{font-size:.72rem;color:#b8d0c7;line-height:1.6}
.rail a{display:block;color:#d5e6dd!important;text-decoration:none;padding:.45rem 0;font-size:.8rem;border-bottom:1px solid #355451}
[data-testid="stMetric"]{padding:12px;background:#fff;border:1px solid #dbe4dc;border-radius:6px}
.stButton button[kind="primary"]{background:#087f83;border:0;border-radius:5px;padding:.6rem 1rem;font-weight:600}
[data-testid="stExpander"]{background:rgba(255,255,255,.45);border-radius:5px}[data-testid="stDataFrame"]{border:1px solid #dce5dd;border-radius:5px}
@media(max-width:800px){.block-container{padding:2rem 1rem}h1{font-size:2.9rem!important}h2{font-size:2rem!important}.hero-number{font-size:4rem}}
</style>'''

def html(s): st.markdown(s,unsafe_allow_html=True)
def finish(c):
    return c.configure_view(stroke=None).configure_axis(labelColor='#637774',titleColor=INK,labelFontSize=11,titleFontSize=12,gridColor='#e3e8e0',domain=False,tickColor='#c5d3ca').configure_legend(orient='top',labelColor=INK,titleColor=INK).configure_title(color=INK,fontSize=14,anchor='start',offset=17)
def stage(n,label,title,anchor):
    html(f'<div id="{anchor}" class="chapter-marker"><b>{n:02d}</b>{label}</div>');st.header(title,anchor=anchor+'-heading')
def note(s): html('<div class="takeaway">'+s+'</div>')
def values(df,label,key):
    with st.expander(label):
        st.dataframe(df,hide_index=True,width='stretch');st.download_button('Download values · CSV',df.to_csv(index=False),key+'.csv','text/csv',key=key)
def selection_country(event,current):
    selected=event.get('selection',{}).get('pick_country',[])
    return selected[0]['iso3'] if selected and selected[0].get('iso3') in ['USA','CHN'] else current
def country_click():
    st.session_state['case_country']=selection_country(st.session_state.get('electricity_pick',{}),st.session_state.get('case_country','USA'))
def render():
    html(CSS);e,w,meta=load_data()
    st.session_state.setdefault('case_country','USA')
    names={'USA':'United States','CHN':'China'}
    with st.sidebar:
        html('<div class="side-eyebrow">YOUR INVESTIGATION</div><div class="side-title">Follow one place.</div>')
        iso=st.selectbox('Country profile',['USA','CHN'],format_func=lambda x:names[x],key='case_country')
        year=st.select_slider('Electricity observation year',options=sorted(e.year.unique().tolist()),value=2025,key='case_year')
        country=names[iso];current=e.loc[(e.iso3==iso)&(e.year==year)].iloc[0];base=e.loc[(e.iso3==iso)&(e.year==2020)].iloc[0];water=w.loc[w.iso3==iso].iloc[0]
        world=float(e.loc[(e.entity=='World')&(e.year==year),'share_pct'].iloc[0]);delta=float(current.share_pct-base.share_pct)
        html(f'<div class="side-stat"><span>ELECTRICITY SHARE · {year}</span><strong>{current.share_pct:.2f}%</strong></div><div class="side-stat"><span>CHANGE SINCE 2020</span><strong>{delta:+.2f} pp</strong></div>')
        html(f'<div class="side-stat"><span>BASELINE WATER STRESS · 0–5</span><strong>{water.bws_score:.2f}</strong></div><div class="side-stat"><span>DROUGHT RISK · 0–5</span><strong>{water.drr_score:.2f}</strong></div>')
        html('<div class="side-eyebrow">THE EVIDENCE TRAIL</div><div class="rail"><a href="#scale">01 &nbsp; Beyond the average</a><a href="#momentum">02 &nbsp; The direction of travel</a><a href="#exposure">03 &nbsp; Water constraints</a><a href="#blind-spot">04 &nbsp; The risk a screen misses</a><a href="#decision">→ &nbsp; Your assessment</a><a href="#source-evidence">↗ &nbsp; Inspect the evidence</a></div>')
        st.caption('Only the US and China have individual electricity series. Other countries appear in water-only exploration.')
    latest=int(e.year.max());world_latest=float(e.loc[(e.entity=='World')&(e.year==latest),'share_pct'].iloc[0])
    pairs=w.dropna(subset=['bws_score','drr_score']);low=pairs.loc[pairs.bws_score<2];elevated=low.loc[low.drr_score>=2]
    html('<div class="masthead"><span>POWERING AI</span><span>Electricity · Water · Place</span></div><div class="eyebrow">AN INTERACTIVE POLICY INVESTIGATION</div>')
    html('<h1>One global average.<br>Different local questions.</h1>')
    st.markdown('**Should data-centre expansion supporting AI be assessed against local electricity and water constraints rather than global averages?**')
    html('<p class="deck">You are an infrastructure policy adviser. Follow a country through the electricity evidence, examine its water conditions, then decide how far the evidence can take you.</p>')
    st.caption(f'Following {country} · electricity {year}. Change the country and year in the side panel.')
    left,right=st.columns([1,2],vertical_alignment='center')
    with left: html(f'<div class="hero-number">{world_latest:.2f}<span style="font-size:2rem">%</span></div><div class="hero-label">World electricity demand used<br>by data centres · {latest}</div>')
    with right:
        html(f'<div class="lede">That figure describes the global share.<br>It does not tell you what to investigate in <strong>{country}</strong>.</div>')
        st.caption(f'The complete snapshot: {len(e)} electricity observations across 10 entities; {len(w)} national water records, {len(pairs)} with paired stress/drought scores. Only 2 electricity entities are individual countries.')
    html('<span class="tag">All data centres, not AI alone</span><span class="tag">National screening, not site approval</span>')
    st.caption('Sources: OWID / IEA / Ember + WRI Aqueduct · local data build '+meta['local_refresh']+' · snapshot dates and indicator periods in the evidence notes below.')
    electricity(e,iso,country,year,current,base,world,delta)
    html('<div id="water-reveal" class="reveal"><div class="eyebrow" style="color:#b9d4bd">PAUSE BEFORE THE NEXT PIECE OF EVIDENCE</div><h3>Would electricity alone be enough?</h3><p>Keep the same country. Follow the water evidence below and test what your first impression leaves out.</p></div>')
    hypothesis=st.radio('Your working hypothesis',['Electricity is the main signal','Water could change the picture','I need more evidence'],index=None,key='working_hypothesis',horizontal=True)
    st.caption('The next stages compare stress, drought and optional riverine-flood risk. Your country and electricity year remain unchanged.')
    render_water(w,water,country,iso,low,elevated)
    decision(country,year,current,base,water,world,hypothesis)
    html('<div id="source-evidence" class="chapter-marker"><b>↗</b>FOLLOW THE EVIDENCE</div>');evidence(e,w)
    with st.expander('Sources, definitions and reference periods'):
        st.markdown('[OWID electricity data](https://ourworldindata.org/grapher/data-centers-share-electricity-demand) · [WRI Aqueduct rankings](https://www.wri.org/data/aqueduct-40-country-rankings) · [WRI dictionary](https://github.com/wri/Aqueduct40/blob/master/data_dictionary_country-rankings.md)')
        st.write('Electricity: all-data-centre demand divided by total electricity demand, percent; observations 2020, 2023–2025. OWID snapshot source log: 18 October 2026. Water source note: 22 October 2026. Local integration data build: 26 October 2026.')
        st.write('Water stress: Aqueduct 4.0 demand-weighted national scores, 1979–2019 baseline. Drought: 2000–2014. Riverine flood: 2010 baseline, with 2016 flood-protection input. Both are inherited Aqueduct 3.0 indicators. They are not simultaneous observations for the chosen electricity year. Drought is total-demand weighted; flood is population weighted.')
        st.write('Scores are dimensionless, not national percentages, per-query consumption or proof that AI caused risk. NoData remains missing. Countries are matched by codes, not display names.')
    with st.expander('Design, team contributions and AI disclosure'):
        st.write('Brighty: electricity comparison. Sanjai: grid-share/change analysis. Apaar: baseline water stress. Harsh: stress versus drought/riverine flood. Original files and branch revisions are retained in the repository.')
        st.write('Ranking bars support precise comparison; a time series supports change; a scatter supports association. Values are labelled or available in expandable tables without hovering. Patterns and shapes supplement colour. Water-only comparisons remain separate from matched electricity coverage.')
        st.write('Codex assisted integration, frontend, narrative, processing and verification. It is not the numerical source. Checks compare source scores, joins, missingness, deterministic rebuilds, linked state and empty cases. Brighty and Sanjai used Claude for electricity work; Harsh used Claude/Cowork for the water-risk dashboard; Apaar used Codex for water stress and integration. Supplied accounts and verification scopes are recorded in docs/AI_PROVENANCE.csv.')
    st.caption('Sources: IEA (2025, 2026) and Ember (2026), processed by Our World in Data; WRI Aqueduct (2023). Team charts and transformations; no endorsement implied.')
    st.caption('POWERING AI · National screening evidence ·  Source and AI documentation in the project repository')

def electricity(e,iso,country,year,current,base,world,delta):
    stage(1,'THE SCALE','Start with the difference the average hides.','scale')
    st.write(f'Your case is **{country}** in **{year}**. Compare its share with the world reference. Click either country bar to switch the persistent profile, or use the country control.')
    geography=st.radio('Comparison lens',['Country pair','Regional context'],horizontal=True,key='comparison_lens',label_visibility='collapsed')
    d=e.loc[(e.entity_type==('Country' if geography=='Country pair' else 'Region'))&(e.year==year)].copy().sort_values('share_pct',ascending=False)
    d['focus']=d.iso3.eq(iso);d['label']=d.share_pct.map(lambda v:f'{v:.2f}%')
    c=alt.Chart(d).encode(x=alt.X('share_pct:Q',title='Data-centre share of electricity demand (%)',scale=alt.Scale(domain=[0,max(world,d.share_pct.max())*1.22],nice=False)),y=alt.Y('name:N',sort=d.name.tolist(),title='Country' if geography=='Country pair' else 'IEA region'))
    bars=c.mark_bar(size=26,cornerRadiusEnd=3)
    if geography=='Country pair':
        bars=bars.encode(color=alt.Color('name:N',scale=alt.Scale(domain=['United States','China'],range=[TEAL,ORANGE]),legend=None),opacity=alt.condition('datum.focus',alt.value(1),alt.value(.45))).add_params(alt.selection_point(name='pick_country',fields=['iso3'],on='click',clear='dblclick'))
    else:
        bars=bars.encode(color=alt.value('#afc5c0'))
    labels=c.mark_text(dx=7,align='left',color=INK,fontSize=13).encode(text='label:N')
    rule=alt.Chart(pd.DataFrame({'x':[world]})).mark_rule(color=ORANGE,strokeDash=[5,4],size=1.5).encode(x='x:Q')
    chart=finish((bars+labels+rule).properties(height=max(160,len(d)*42),title=f'Electricity share by place · {year}'))
    if geography=='Country pair': st.altair_chart(chart,width='stretch',theme=None,key='electricity_pick',on_select=country_click,selection_mode='pick_country')
    else: st.altair_chart(chart,width='stretch',theme=None,key='electricity_regions')
    st.caption(f'Amber dashed line = world share ({world:.2f}%). Regions contain countries and must not be added to them; no regional value substitutes for a national one.')
    relation='above' if current.share_pct>world else 'below' if current.share_pct<world else 'equal to'
    note(f'<strong>{country}: {current.share_pct:.2f}%</strong> — {abs(current.share_pct-world):.2f} percentage points {relation} the world share of {world:.2f}%. This is the share of its electricity demand attributed to all data centres, not proof of congestion.')
    values(d[['name','share_pct']].rename(columns={'name':'Location','share_pct':f'Electricity share {year} (%)'}),'See the exact comparison values','rank_values')
    stage(2,'THE MOMENTUM','A snapshot cannot show the direction of travel.','momentum')
    html(f'<p class="bridge">What changes when you follow {country} through time?</p>')
    mode=st.radio('Follow the trajectory',['Share of demand','Change since 2020'],horizontal=True,key='trajectory_measure')
    t=e.loc[(e.entity_type=='Country')&(e.year<=year)].copy()
    baseline=e.loc[(e.entity_type=='Country')&(e.year==2020),['iso3','share_pct']].rename(columns={'share_pct':'baseline'})
    t=t.merge(baseline,on='iso3',validate='many_to_one');t['value']=t.share_pct if mode=='Share of demand' else t.share_pct-t.baseline;t['label']=t.value.map(lambda v:f'{v:.2f}')
    unit='Electricity-demand share (%)' if mode=='Share of demand' else 'Change from 2020 (percentage points)'
    colour=alt.Color('name:N',title='Country',scale=alt.Scale(domain=['United States','China'],range=[TEAL,ORANGE]))
    line=alt.Chart(t).encode(x=alt.X('year:Q',title='Observation year',scale=alt.Scale(zero=False),axis=alt.Axis(values=sorted(t.year.unique().tolist()),format='d')),y=alt.Y('value:Q',title=unit,scale=alt.Scale(zero=True)),color=colour)
    lines=line.mark_line(point=True).encode(strokeWidth=alt.condition(alt.datum.iso3==iso,alt.value(3.5),alt.value(1.5)),strokeDash=alt.StrokeDash('name:N',legend=None))
    st.altair_chart(finish((lines+line.mark_text(dy=-13,fontSize=11).encode(text='label:N')).properties(height=280,title=f'The observed trajectory · through {year}')),width='stretch',theme=None)
    st.caption('Only 2020, 2023, 2024 and 2025 exist in the snapshot. Lines connect available points; they do not supply missing annual values or forecasts. Colour and pattern identify countries; your profile has the heavier line.')
    note(f'<strong>{country} changed by {delta:+.2f} percentage points</strong> between 2020 and {year}, from {base.share_pct:.2f}% to {current.share_pct:.2f}%. Percentage-point change subtracts shares; it is not percentage growth.')
    with st.expander('Try an electricity-only screening threshold'):
        threshold=st.slider('Your illustrative threshold (% of demand)',.5,6.,3.,.5,key='screen_threshold')
        st.write(f'{country} is **'+('at or above' if current.share_pct>=threshold else 'below')+f' your {threshold:.1f}% line** in {year}. This is your exploratory choice, not an official limit or approval rule.')
    values(t[['name','year','share_pct','value']].rename(columns={'name':'Country','year':'Year','share_pct':'Share (%)','value':unit}),'Inspect the trajectory and calculation','trend_values')

def render_water(w,water,country,iso,low,elevated):
    stage(3,'THE EXPOSURE','Same country. A different resource constraint.','exposure')
    st.write(f'For **{country}**, baseline water stress scores **{water.bws_score:.2f} / 5**, classified as **{water.bws_label}**. The period and measure differ from the electricity evidence above.')
    mapping=dict(zip(w.iso3,w.country))
    comparator=st.selectbox('Add a water-only comparison',w.iso3.tolist(),index=w.iso3.tolist().index('IRL'),format_func=lambda x:mapping[x],key='water_case')
    ids=list(dict.fromkeys([iso,comparator]));d=w.loc[w.iso3.isin(ids)].dropna(subset=['bws_score']).copy().sort_values('bws_score',ascending=False)
    d['label']=d.bws_score.map(lambda v:f'{v:.2f} / 5');d['focus']=d.iso3.eq(iso)
    if d.empty: st.info('No water-stress scores for these countries.')
    else:
        c=alt.Chart(d).encode(x=alt.X('bws_score:Q',title='Baseline water-stress score (dimensionless, 0–5)',scale=alt.Scale(domain=[0,5.7],nice=False),axis=alt.Axis(values=[0,1,2,3,4,5])),y=alt.Y('country:N',sort=d.country.tolist(),title='Country'))
        bars=c.mark_bar(size=24,cornerRadiusEnd=3).encode(color=alt.condition('datum.focus',alt.value(TEAL if iso=='USA' else ORANGE),alt.value('#5264A4')))
        st.altair_chart(finish((bars+c.mark_text(align='left',dx=7,fontSize=12,color=INK).encode(text='label:N')).properties(height=160,title='The water-stress contrast · national weighted scores')),width='stretch',theme=None)
    st.caption(f'{mapping[comparator]} is a water-only comparison here. No electricity value is invented. Stress uses the 1979–2019 baseline; this is not AI water use and cannot be converted to a national withdrawal percentage.')
    missing=w.loc[w.iso3.isin(ids)&w.bws_score.isna(),'country'].tolist()
    if missing: st.warning('No stress score for: '+', '.join(missing)+'. Missing is not zero.')
    values(w.loc[w.iso3.isin(ids),['country','bws_score','bws_label']].rename(columns={'country':'Country','bws_score':'Stress score (0–5)','bws_label':'WRI category'}),'Read the water-stress values','stress_values')
    stage(4,'THE BLIND SPOT','Low stress does not necessarily mean low risk.','blind-spot')
    html(f'<div class="lede"><strong>{len(elevated)} of {len(low)}</strong> countries with a stress score below 2 still have a drought-risk score of at least 2.<br><span class="smallprint">Whole-file finding; only countries with both scores enter this denominator.</span></div>')
    st.write('These indicators answer different questions. A stress-only screen may miss drought concerns; this does not establish the risk at a particular facility.')
    choice=st.radio('Reveal another water indicator',['Drought risk','Riverine flood risk'],horizontal=True,key='extra_risk')
    ys='drr_score' if choice=='Drought risk' else 'rfr_score';yl='drr_label' if choice=='Drought risk' else 'rfr_label'
    context=st.checkbox('Show global water context',True,key='global_water')
    scope=st.radio('Explore the evidence',['All paired records','Low stress, elevated additional risk'],horizontal=True,key='risk_filter')
    all_valid=w.dropna(subset=['bws_score',ys]);d=(all_valid if context else all_valid.loc[all_valid.iso3.isin(ids)]).copy()
    if scope!='All paired records': d=d.loc[(d.bws_score<2)&(d[ys]>=2)]
    if d.empty: st.info('No paired scores meet this filter. Show global context or choose a different water comparison.')
    else:
        d['group']=d.iso3.map(lambda x:'Your country' if x==iso else 'Water comparison' if x==comparator else 'Global context')
        x=alt.X('bws_score:Q',title='Baseline water-stress score (0–5)',scale=alt.Scale(domain=[0,5.4],nice=False),axis=alt.Axis(values=[0,1,2,3,4,5]));y=alt.Y(ys+':Q',title=choice+' score (0–5)',scale=alt.Scale(domain=[0,5.4],nice=False),axis=alt.Axis(values=[0,1,2,3,4,5]))
        point=alt.Chart(d).mark_point(strokeWidth=1.7).encode(x=x,y=y,size=alt.condition(alt.datum.group=='Global context',alt.value(60),alt.value(160)),opacity=alt.condition(alt.datum.group=='Global context',alt.value(.6),alt.value(1)),color=alt.Color('group:N',title='Country set',scale=alt.Scale(domain=['Your country','Water comparison','Global context'],range=[TEAL if iso=='USA' else ORANGE,'#5264A4','#71817a'])),shape=alt.Shape('group:N',title='Country set',scale=alt.Scale(domain=['Your country','Water comparison','Global context'],range=['diamond','square','circle'])))
        labels=alt.Chart(d.loc[d.iso3.isin(ids)]).mark_text(dx=8,dy=-12,align='left',fontSize=12,color=INK).encode(x='bws_score:Q',y=ys+':Q',text='country:N')
        zone=alt.Chart(pd.DataFrame({'x':[0],'x2':[2],'y':[2],'y2':[5]})).mark_rect(color=ORANGE,opacity=.08).encode(x='x:Q',x2='x2:Q',y='y:Q',y2='y2:Q');rule=alt.Chart(pd.DataFrame({'v':[2]})).mark_rule(color='#a1afa6',strokeDash=[3,4])
        st.altair_chart(finish((zone+rule.encode(x='v:Q')+rule.encode(y='v:Q')+point+labels).properties(height=330,title='Find the cases a stress-only screen could miss')),width='stretch',theme=None)
        st.caption(f'Shaded zone: stress score <2, {choice.lower()} score ≥2. {len(d)} countries shown. Shapes distinguish cases from context; exact scores below. Weighted score thresholds are not literal national physical ratios.')
        values(d[['country','bws_score',ys]].rename(columns={'country':'Country','bws_score':'Stress score (0–5)',ys:choice+' score (0–5)'}),'Inspect every plotted country','scatter_values')
    cases=w.loc[w.iso3.isin(ids),['country','bws_score',ys,yl]]
    st.dataframe(cases.rename(columns={'country':'Your two cases','bws_score':'Stress (0–5)',ys:choice+' (0–5)',yl:'WRI category'}),hide_index=True,width='stretch')
    for row in cases.itertuples(index=False,name=None):
        if pd.isna(row[1]) or pd.isna(row[2]): st.warning(row[0]+' has no paired score for this indicator; it is absent from the scatter, not assigned zero.')
    comparison=w.loc[w.iso3==comparator].iloc[0]
    if pd.notna(comparison.bws_score) and pd.notna(comparison[ys]):
        flag=comparison.bws_score<2 and comparison[ys]>=2
        note(f'<strong>{escape(mapping[comparator])}</strong> has a stress score of {comparison.bws_score:.2f} and {choice.lower()} score of {comparison[ys]:.2f}. '+('It falls in the shaded zone: stress alone would not describe this additional concern.' if flag else 'It is outside the shaded zone. That is not a site-level safety verdict.'))
    st.caption('Water stress: Aqueduct 4.0 (1979–2019). Drought: 2000–2014 (demand weighted). Riverine flood: 2010 baseline with 2016 flood-protection input (population weighted). Neither is a current hazard alert.')

def decision(country,year,current,base,water,world,hypothesis):
    html('<div id="decision" class="chapter-marker"><b>→</b>RETURN TO THE DECISION</div>');st.header('A stronger question than “is it safe?”')
    st.write(f'For **{country}**, ask: **what local electricity and water evidence would an expansion proposal need to provide?**')
    cards=[(f'Electricity · {year}',f'{current.share_pct:.2f}%',f'{current.share_pct-base.share_pct:+.2f} pp since 2020<br>World reference: {world:.2f}%'),('Baseline water stress',f'{water.bws_score:.2f} / 5',escape(str(water.bws_label))+'<br>1979–2019 baseline'),('Additional drought risk',f'{water.drr_score:.2f} / 5',escape(str(water.drr_label))+'<br>2000–2014 · Aqueduct 3.0')]
    for col,(label,val,detail) in zip(st.columns(3),cards):
        with col: html(f'<div class="case-card"><div class="case-label">{label}</div><div class="case-value">{val}</div><p>{detail}</p></div>')
    if hypothesis: st.caption('Your starting hypothesis: '+hypothesis+'. Evidence adds distinct signals; it does not produce a sustainability score.')
    note('<strong>Our answer: location-specific assessment is better supported than a global-average rule.</strong> Electricity shares differ across places and time. Water stress and drought add different constraints. Together they support targeted investigation, not an automatic limit on expansion.')
    next_step=st.selectbox('What would you request next?',['Local grid capacity and connection study','Catchment-level water supply and cooling plan','Both, with facility demand and mitigation evidence'],key='next_evidence')
    responses=['Electricity share does not measure spare network capacity or congestion. A local connection study addresses a gap these data cannot fill.','National scores hide catchment differences. Site demand, water source, cooling technology and seasonal conditions are needed to assess a proposal.','This links the resources at the decision scale. Facility demand and credible mitigation evidence could change the conclusion that national screening alone suggests.']
    st.write(responses[['Local grid capacity and connection study','Catchment-level water supply and cooling plan','Both, with facility demand and mitigation evidence'].index(next_step)])
    with st.expander('Could someone reasonably interpret this evidence differently?'):
        st.write('Yes. National indicators may be too coarse to justify constraints, and facility design or mitigation could matter more. The same data can support further investigation rather than restrictions. We cannot measure AI-only demand, infer causation, approve a site or predict local impacts from this comparison.')
    st.caption('Different units and reference periods stay separate. This is an evidence brief, not a synchronized causal model or approval calculator.')

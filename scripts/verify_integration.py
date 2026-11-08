from pathlib import Path
import hashlib
import io
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build_story_data import build
import pandas as pd
from streamlit.testing.v1 import AppTest

paths=[ROOT/'data/processed'/p for p in ['story_electricity.csv','story_water.csv','grid_share.csv']]
before={p:pd.read_csv(p) for p in paths}
e,w=build()
for path in paths:
    # Compare parsed tables, so CRLF/LF differences cannot cause false failures.
    pd.testing.assert_frame_equal(before[path],pd.read_csv(path),check_exact=True)
first_build={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
build()
assert all(first_build[p]==hashlib.sha256(p.read_bytes()).hexdigest() for p in paths), 'Repeated local build changed output bytes'
# Explicit regression: both operating-system newline conventions preserve values.
for path in paths:
    lf=path.read_bytes().replace(b'\r\n',b'\n')
    pd.testing.assert_frame_equal(pd.read_csv(io.BytesIO(lf)),pd.read_csv(io.BytesIO(lf.replace(b'\n',b'\r\n'))),check_exact=True)
raw=pd.read_csv(ROOT/'data/raw/data-centers-share-electricity-demand.csv')
for row in e.itertuples():
    source=raw.iloc[row.source_csv_row-2]
    assert source.Entity==row.entity and source.Year==row.year
    assert float(source.iloc[-1])==row.share_pct
sample=pd.read_csv(ROOT/'data/raw/story_country_baseline_sample.csv')
for ind,weight in [('bws','Tot'),('drr','Tot'),('rfr','Pop')]:
    source=sample.loc[(sample.indicator_name==ind)&(sample.weight==weight)].set_index('gid_0')
    for row in w.itertuples():
        value=getattr(row,ind+'_score')
        if row.iso3 not in source.index:
            assert pd.isna(value)
            continue
        original=source.loc[row.iso3,'score']
        if pd.isna(original) or original==-9999:
            assert pd.isna(value)
        else:
            assert abs(value-original)<1e-12
if '--shared-only' in sys.argv:
    print('Member snapshot comparison NOT RUN: --shared-only selected; individual contributor uploads are pending.')
else:
    apaar=pd.read_csv(ROOT/'contributors/Apaar/data/processed/water_stress.csv')
    joined=apaar.loc[apaar.has_score].merge(w,on='iso3',validate='one_to_one')
    assert (abs(joined.stress_score-joined.bws_score)<1e-12).all()
    harsh=pd.read_csv(ROOT/'contributors/Harsh/data/processed/m4_water_stress_drought.csv')
    j=harsh.merge(w,on='iso3',suffixes=('_member','_story'),validate='one_to_one')
    for indicator in ['bws','drr','rfr']:
        a=j[indicator+'_score_member'];b=j[indicator+'_score_story']
        assert ((a.isna()&b.isna())|(abs(a-b)<1e-12)).all()
if '--shared-only' not in sys.argv:
    print(f'Member comparison PASS: {len(joined)} Apaar scores match; all Harsh scores match.')
pairs=w.dropna(subset=['bws_score','drr_score'])
low=pairs.loc[pairs.bws_score<2]
print(f'Source checks PASS: {len(e)} electricity rows; {len(w)} water records; drought check {int((low.drr_score>=2).sum())}/{len(low)}.')

from frontend import selection_country
assert selection_country({'selection':{'pick_country':[{'iso3':'CHN'}]}},'USA') == 'CHN'
assert selection_country({'selection':{'pick_country':[{'iso3':'IRL'}]}},'USA') == 'USA'
assert selection_country({'selection':{'pick_country':[]}},'USA') == 'USA'
start=time.perf_counter()
app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=30).run(timeout=45)
assert not app.exception,[x.message for x in app.exception]
assert len(app.get('vega_lite_chart'))==4, 'All four charts must render before any interaction'
assert not any(button.key=='reveal_water' for button in app.button)
print(f'Opening render: {time.perf_counter()-start:.2f}s; all four charts present without interaction')
app.radio(key='working_hypothesis').set_value('Electricity is the main signal').run()
assert not app.exception,[x.message for x in app.exception]
assert len(app.get('vega_lite_chart'))==4
start=time.perf_counter()
app.selectbox(key='case_country').set_value('CHN').run()
assert not app.exception
assert 'China' in '\n'.join(x.value for x in app.markdown)
print(f'Persistent country change: {time.perf_counter()-start:.2f}s')
app.select_slider(key='case_year').set_value(2023).run()
app.radio(key='trajectory_measure').set_value('Change since 2020').run()
app.radio(key='comparison_lens').set_value('Regional context').run()
assert not app.exception
app.selectbox(key='water_case').set_value('CAN').run()
assert not app.exception
assert any('no paired score' in x.value for x in app.warning)
app.radio(key='extra_risk').set_value('Riverine flood risk').run()
app.checkbox(key='global_water').uncheck().run()
assert not app.exception
app.selectbox(key='water_case').set_value('CHN').run()
app.radio(key='risk_filter').set_value('Low stress, elevated additional risk').run()
assert not app.exception
assert any('No paired scores meet' in x.value for x in app.info)
app.radio(key='risk_filter').set_value('All paired records').run()
app.select_slider(key='case_year').set_value(2020).run()
app.radio(key='evidence_kind').set_value('Water').run()
assert not app.exception
app.radio(key='comparison_lens').set_value('Country pair').run()
app.radio(key='extra_risk').set_value('Drought risk').run()
app.selectbox(key='water_case').set_value('IRL').run()
app.checkbox(key='global_water').check().run()
app.selectbox(key='next_evidence').set_value('Both, with facility demand and mitigation evidence').run()
assert not app.exception
assert len(app.get('vega_lite_chart'))==4
print('Guided interaction checks PASS: four charts on initial render; no reveal gate; country selection mapping; persistent country/year; hypothesis; region lens; trajectory toggle; missing drought; flood; no-context empty state; same-country comparator; earliest year; evidence inspection; decision follow-up.')

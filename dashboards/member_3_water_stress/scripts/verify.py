"""Meaningful data-integrity, regeneration and Streamlit interaction checks."""
from pathlib import Path
import sys
import hashlib
import io
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'.vendor'))
import pandas as pd
from prepare_data import build
from streamlit.testing.v1 import AppTest

path=ROOT/'data/processed/water_stress.csv'
before=hashlib.sha256(path.read_bytes()).hexdigest()
df=build()
assert before == hashlib.sha256(path.read_bytes()).hexdigest(), 'Regeneration changed processed data'
assert df.iso3.is_unique
with zipfile.ZipFile(ROOT/'data/raw/aqueduct-4-0-country-rankings.zip') as z:
    raw=pd.read_excel(io.BytesIO(z.read(z.namelist()[0])),sheet_name='country_baseline')
for row in df.itertuples():
    source=raw.iloc[row.source_excel_row-2]
    assert source.gid_0 == row.iso3 and source.weight == 'Tot' and source.indicator_name == 'bws'
    assert pd.isna(source.score) and pd.isna(row.stress_score) or source.score == row.stress_score
print('PASS: all country scores and spreadsheet locators match original workbook; regeneration identical')

app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=40)
assert not app.exception, [x.message for x in app.exception]
app.checkbox(key='water_all').uncheck().run()
app.multiselect(key='water_countries').set_value(['AUS','IND','USA']).run()
assert not app.exception
assert len(app.dataframe[0].value)==3
app.multiselect(key='water_regions').set_value([]).run()
assert not app.exception
assert any('No countries match' in x.value for x in app.warning)
app.multiselect(key='water_regions').set_value(sorted(df.loc[df.has_score,'region'].dropna().unique())).run()
app.radio(key='water_order').set_value('Lowest stress first').run()
assert not app.exception
table=app.dataframe[0].value
assert table['Score (0–5)'].is_monotonic_increasing
app.selectbox(key='water_verify').set_value('AUS').run()
assert not app.exception
assert any('Verification passed' in x.value for x in app.success)
app.multiselect(key='water_countries').set_value([]).run()
assert not app.exception
assert any('No countries match' in x.value for x in app.warning)
print('PASS: app startup, country and region filters, empty states, ordering and source verification')

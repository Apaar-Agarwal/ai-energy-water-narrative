"""Offline, deterministic Part 2 build from the teammates' saved source files."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
import numpy as np
import pandas as pd

RAW=ROOT/'data/raw'
OUT=ROOT/'data/processed'

def fix_name(value):
    if not isinstance(value,str):
        return value
    try:
        return value.encode('latin1').decode('utf8')
    except (UnicodeError,ValueError):
        return value

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    csv=RAW/'data-centers-share-electricity-demand.csv'
    xlsx=RAW/'Aqueduct40_rankings_download_Y2023M07D05.xlsx'
    e=pd.read_csv(csv)
    value=[c for c in e if c not in ['Entity','Code','Year']]
    assert len(value)==1
    e.insert(0,'source_csv_row',range(2,len(e)+2))
    e=e.rename(columns={'Entity':'entity','Code':'iso3','Year':'year',value[0]:'share_pct'})
    assert not e.duplicated(['entity','year']).any()
    assert e.share_pct.dropna().between(0,100).all()
    e['name']=e.entity.str.replace(r'\s*\(IEA\)$','',regex=True)
    e['entity_type']=np.where(e.entity.str.startswith('World'),'Aggregate',np.where(e.iso3.fillna('').str.len()==3,'Country','Region'))
    e=e.sort_values(['entity','year']).reset_index(drop=True)
    e.to_csv(OUT/'story_electricity.csv',index=False)

    raw=pd.read_excel(xlsx,sheet_name='country_baseline')
    raw.insert(0,'source_excel_row',range(2,len(raw)+2))
    assert not raw.duplicated(['gid_0','indicator_name','weight']).any()
    raw.to_csv(RAW/'story_country_baseline_sample.csv',index=False)
    ids=raw[['gid_0','name_0','un_region','wb_region']].drop_duplicates('gid_0').rename(columns={'gid_0':'iso3','name_0':'country','un_region':'region'})
    ids['country']=ids.country.map(fix_name).fillna(ids.iso3)
    w=ids.copy()
    for ind,weight in [('bws','Tot'),('drr','Tot'),('rfr','Pop')]:
        part=raw.loc[(raw.indicator_name==ind)&(raw.weight==weight),['gid_0','score','cat','label','source_excel_row']].copy()
        part[['score','cat']]=part[['score','cat']].replace(-9999,np.nan)
        assert part.score.dropna().between(0,5).all()
        part=part.rename(columns={'gid_0':'iso3',**{c:f'{ind}_{c}' for c in ['score','cat','label','source_excel_row']}})
        w=w.merge(part,on='iso3',how='left',validate='one_to_one')
    assert w.iso3.is_unique
    w=w.sort_values('country').reset_index(drop=True)
    w.to_csv(OUT/'story_water.csv',index=False)
    # Member 2's change metric, regenerated from the shared OWID snapshot.
    g=e[['entity','iso3','year','share_pct']].rename(columns={'entity':'location','iso3':'code'})
    g.to_csv(OUT/'grid_share.csv',index=False)
    metadata={'build':'offline from committed source snapshots','local_refresh':'2026-10-26',
              'electricity_retrieved':'2026-10-18 (Brighty source log)',
              'water_retrieved':'2026-10-22 (Harsh source note; member confirmation pending)',
              'electricity_years':sorted(int(x) for x in e.year.unique()),
              'water_stress_baseline':'1979â€“2019',
              'water_vintages':'bws: Aqueduct 4.0; drought and riverine flood: inherited Aqueduct 3.0 indicators; do not assign one observation period to all indicators',
              'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [csv,xlsx]},
              'electricity_rows':len(e),'water_rows':len(w)}
    (OUT/'story_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(f'Built {len(e)} electricity rows and {len(w)} water records.')
    return e,w

if __name__=='__main__':
    build()

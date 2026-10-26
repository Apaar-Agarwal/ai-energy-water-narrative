"""Rebuild the app dataset from the unchanged official WRI archive."""
from pathlib import Path
import hashlib
import io
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.vendor'))
import pandas as pd

def build():
    archive = ROOT / 'data/raw/aqueduct-4-0-country-rankings.zip'
    with zipfile.ZipFile(archive) as z:
        member = next(n for n in z.namelist() if n.endswith('.xlsx'))
        df = pd.read_excel(io.BytesIO(z.read(member)), sheet_name='country_baseline')
    df.insert(0, 'source_excel_row', range(2, len(df) + 2))
    sample = df.loc[(df.indicator_name == 'bws') & (df.weight == 'Tot')].copy()
    assert not sample.gid_0.duplicated().any(), 'Duplicate country keys'
    sample.to_csv(ROOT / 'data/raw/country_baseline_bws_tot.csv', index=False)
    out = sample.rename(columns={'gid_0':'iso3','name_0':'country','score':'stress_score',
                                'score_ranked':'source_rank','cat':'category_code',
                                'label':'risk_category','un_region':'region'})
    out['stress_score'] = pd.to_numeric(out.stress_score, errors='coerce')
    out['has_score'] = out.stress_score.between(0, 5) & out.category_code.between(0, 4)
    out = out.sort_values('country').reset_index(drop=True)
    out.to_csv(ROOT / 'data/processed/water_stress.csv', index=False)
    metadata = {'source_url':'https://files.wri.org/aqueduct/aqueduct-4-0-country-rankings.zip',
                'landing_page':'https://www.wri.org/data/aqueduct-40-country-rankings',
                'retrieved':'2026-10-18','edition':'Aqueduct 4.0 (2023)',
                'baseline':'1979–2019','sheet':'country_baseline','workbook_member':member,
                'licence':'CC BY 4.0','archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
                'rows':len(out),'valid_scores':int(out.has_score.sum())}
    (ROOT / 'data/metadata.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    print(json.dumps(metadata, indent=2))
    return out

if __name__ == '__main__':
    build()

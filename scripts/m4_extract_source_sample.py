"""Member 4 - Step 0: extract the source sample.

Copies the `country_baseline` sheet of the WRI Aqueduct 4.0 country rankings
workbook to CSV *unchanged* (no filtering, no recoding), so the repository holds
a small, diff-able source sample the processing step can read.

Run from the repo root:  python scripts/m4_extract_source_sample.py
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / "data/source/Aqueduct40_rankings_download_Y2023M07D05.xlsx"
OUT = ROOT / "data/source/aqueduct40_country_baseline.csv"

df = pd.read_excel(XLSX, sheet_name="country_baseline")
df.to_csv(OUT, index=False)
print(f"Wrote {OUT.relative_to(ROOT)}: {len(df)} rows x {df.shape[1]} cols")

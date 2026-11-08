"""Step 1 - get the raw OWID file and produce the processed file.

Option A (automatic):   python prepare_data.py
Option B (manual file): python prepare_data.py --file ~/Downloads/data-centers-share-electricity-demand.zip
                        (a .zip or .csv downloaded from the OWID page both work)

The raw file is saved UNTOUCHED in data/raw/. Every processing step is printed so
you can screenshot it as evidence for your source register.
"""
import argparse, datetime, io, os, zipfile
import pandas as pd
import requests

URL = ("https://ourworldindata.org/grapher/data-centers-share-electricity-demand.csv"
       "?v=1&csvType=full&useColumnShortNames=false")
RAW = "data/raw/data-centers-share-electricity-demand.csv"
OUT = "data/processed/grid_share.csv"

ap = argparse.ArgumentParser()
ap.add_argument("--file", help="path to a manually downloaded .zip or .csv")
args = ap.parse_args()
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

if args.file:
    if args.file.lower().endswith(".zip"):
        with zipfile.ZipFile(args.file) as z:
            name = [n for n in z.namelist() if n.endswith(".csv")][0]
            content = z.read(name)
    else:
        content = open(args.file, "rb").read()
else:
    r = requests.get(URL, headers={"User-Agent": "Our World In Data data fetch/1.0"}, timeout=60)
    r.raise_for_status()
    content = r.content
with open(RAW, "wb") as f:
    f.write(content)
print(f"[1] Raw file saved to {RAW} on {datetime.date.today()} ({len(content):,} bytes)")

df = pd.read_csv(io.BytesIO(content))
print("[2] Raw columns:", list(df.columns), "| rows:", len(df))

value_col = df.columns[-1]            # the indicator is the last column
df = df.rename(columns={"Entity": "location", "Code": "code", "Year": "year", value_col: "share_pct"})
n0 = len(df)
df = df.dropna(subset=["share_pct"])
print(f"[3] Dropped {n0 - len(df)} rows with a missing share (no interpolation, no filling)")

df["year"] = df["year"].astype(int)
df["share_pct"] = df["share_pct"].astype(float)       # already in percent (unit: %)
df = df[["location", "code", "year", "share_pct"]].sort_values(["year", "share_pct"], ascending=[True, False])
df.to_csv(OUT, index=False)
print(f"[4] Wrote {OUT}: {len(df)} rows")
print("    Years present   :", sorted(df['year'].unique()))
print("    Locations present:", sorted(df['location'].unique()))
print("    Unit: percent (data-centre electricity / total electricity demand x 100)")

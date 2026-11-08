"""Process the raw OWID file into the tidy file the dashboard reads.

Run from the project root:  python scripts/process_owid.py

Transformations (document these in docs/source_log.md):
  1. Rename the long value column to `share_pct` (values unchanged, in percent).
  2. Rename Entity -> entity, Code -> code, Year -> year.
  3. Strip the " (IEA)" suffix into `entity_clean` for display.
  4. Add `entity_type`: Country (has an ISO code), Aggregate (World rows),
     Region (everything else).
No values are filled, interpolated or rescaled. Missing years stay missing.
"""
from pathlib import Path
import pandas as pd

RAW = Path("data/raw/data-centers-share-electricity-demand.csv")
OUT = Path("data/processed/owid_data_centres_share_clean.csv")

df = pd.read_csv(RAW)
value_col = [c for c in df.columns if c not in ("Entity", "Code", "Year")][0]
df = df.rename(columns={"Entity": "entity", "Code": "code",
                        "Year": "year", value_col: "share_pct"})

df["entity_clean"] = df["entity"].str.replace(r"\s*\(IEA\)", "", regex=True)

def classify(row):
    if row["entity"].startswith("World"):
        return "Aggregate"
    if isinstance(row["code"], str) and row["code"].strip():
        return "Country"
    return "Region"

df["entity_type"] = df.apply(classify, axis=1)

# Sanity checks that could fail
assert df["share_pct"].notna().all(), "Unexpected missing values"
assert not df.duplicated(["entity", "year"]).any(), "Duplicate entity-year rows"
assert df["share_pct"].between(0, 100).all(), "Value outside 0-100"

OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Wrote {OUT} ({len(df)} rows)")
print(df.groupby("entity_type")["entity_clean"].unique())
print("Years:", sorted(df["year"].unique()))

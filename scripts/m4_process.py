"""Member 4 - Step 1: build the processed file the dashboard reads.

Input : data/source/aqueduct40_country_baseline.csv  (unchanged export of the
        `country_baseline` sheet, Aqueduct 4.0, file dated 2023-07-05)
Output: data/processed/m4_water_stress_drought.csv  (one row per country)

Transform (documented in docs/m4_data_dictionary.md):
  T1  Keep three indicator/weight pairs:
        bws (baseline water stress)   weight = Tot (weighted by total water demand)
        drr (drought risk)            weight = Tot
        rfr (riverine flood risk)     weight = Pop (only weight offered for rfr)
  T2  Replace the NoData sentinel -9999 with missing (NaN) - never with 0.
  T3  Pivot to one row per country (gid_0) with score / cat / label per indicator.
  T4  Add flag `low_stress_elevated_drought` = bws_score < 2 (below 20 % withdrawal
      ratio, i.e. Low or Low-Medium) AND drr_score >= 2 (raw drought risk >= 0.4,
      i.e. Medium or above). Missing if either score is missing.
  T5  Repair mis-encoded country names (UTF-8 read as Latin-1, e.g. Cote d'Ivoire);
      blank names (KIR, MCO, MHL) fall back to the ISO3 code.
  Scores are kept at full source precision (no rounding).
Checks (the script stops if any fails):
  C1  (gid_0, indicator, weight) is unique in the source.
  C2  For every non-missing value, cat == min(floor(score), 4)  - the category
      bands in the source are whole-number score bands.
  C3  Scores lie in [0, 5].

Run from the repo root:  python scripts/m4_process.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data/source/aqueduct40_country_baseline.csv"
OUT = ROOT / "data/processed/m4_water_stress_drought.csv"

KEEP = {("bws", "Tot"), ("drr", "Tot"), ("rfr", "Pop")}
NODATA = -9999

src = pd.read_csv(SRC)

# C1
dups = src.duplicated(["gid_0", "indicator_name", "weight"]).sum()
assert dups == 0, f"C1 failed: {dups} duplicate keys"

# T1
mask = [(i, w) in KEEP for i, w in zip(src.indicator_name, src.weight)]
sel = src.loc[mask, ["gid_0", "name_0", "un_region", "wb_region",
                     "indicator_name", "score", "cat", "label"]].copy()

# T2
for col in ["score", "cat"]:
    sel.loc[sel[col] == NODATA, col] = np.nan

# C2, C3
v = sel.dropna(subset=["score"])
bad = (np.minimum(np.floor(v.score), 4) != v.cat).sum()
assert bad == 0, f"C2 failed: {bad} rows where cat != floor(score)"
assert v.score.between(0, 5).all(), "C3 failed: score outside 0-5"

# T3
wide = (sel.set_index(["gid_0", "name_0", "un_region", "wb_region",
                       "indicator_name"])[["score", "cat", "label"]]
          .unstack("indicator_name"))
wide.columns = [f"{ind}_{field}" for field, ind in wide.columns]
wide = wide.reset_index()
order = ["gid_0", "name_0", "un_region", "wb_region"]
for ind in ["bws", "drr", "rfr"]:
    order += [f"{ind}_score", f"{ind}_cat", f"{ind}_label"]
wide = wide[order].rename(columns={"gid_0": "iso3", "name_0": "country"})
for ind in ["bws", "drr", "rfr"]:
    wide[f"{ind}_score"] = wide[f"{ind}_score"].astype(float)
    wide[f"{ind}_cat"] = wide[f"{ind}_cat"].astype("Int64")

# T5  Repair mis-encoded country names in the source (e.g. "CÃ´te d'Ivoire",
#     UTF-8 bytes read as Latin-1). Names that do not round-trip are left as is.
def _fix(name):
    if not isinstance(name, str):
        return name
    try:
        return name.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name
wide["country"] = wide["country"].map(_fix).fillna(wide["iso3"])  # 3 blank names (KIR, MCO, MHL)

# T4
both = wide.bws_score.notna() & wide.drr_score.notna()
flag = (wide.bws_score < 2) & (wide.drr_score >= 2)
wide["low_stress_elevated_drought"] = flag.where(both).astype("boolean")

wide = wide.sort_values("iso3").reset_index(drop=True)
OUT.parent.mkdir(parents=True, exist_ok=True)
wide.to_csv(OUT, index=False)

print(f"Wrote {OUT.relative_to(ROOT)}: {len(wide)} countries")
for ind in ["bws", "drr", "rfr"]:
    print(f"  {ind}: {wide[f'{ind}_score'].notna().sum()} with a score, "
          f"{wide[f'{ind}_score'].isna().sum()} NoData")
print(f"  bws and drr both present: {both.sum()}; flagged: {int(flag[both].sum())}")

# Processing script

`process_owid.py` regenerates `data/processed/owid_data_centres_share_clean.csv` from the raw OWID file. Run it from this member folder (`contributors/Brighty`):

```
python scripts/process_owid.py
```

It renames columns, strips the " (IEA)" suffix and classifies entities. Assertions stop the script if any value is missing, any entity-year row is duplicated or any value is outside 0–100.
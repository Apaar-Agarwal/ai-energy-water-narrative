# Brighty: electricity comparison dashboard

`electricity_comparison.py` is a standalone Streamlit dashboard answering: *Where do data centres account for the greatest share of electricity demand?*

It shows a ranked horizontal bar chart of data-centre share of electricity demand with a World reference line, a year selector (2020, 2023, 2024, 2025), entity-type and entity filters, a values table, and a panel that shows the matching row from the original OWID file.

Run from the project root:

```
python -m streamlit run contributors/Brighty/dashboards/electricity_comparison.py
```

Data paths are anchored to this member folder. The integrated group story (root `app.py`) adapts this comparison as Chapter 1.

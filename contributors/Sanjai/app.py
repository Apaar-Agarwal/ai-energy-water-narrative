"""Team entry point. Each member provides a module with render(). Add theirs to SECTIONS."""
import importlib
import streamlit as st

st.set_page_config(page_title="AI infrastructure: electricity and water", page_icon="⚡", layout="wide")
st.title("Should electricity and water limit AI infrastructure expansion?")
st.caption("Persona: a regional infrastructure planner deciding on a new data centre.")

SECTIONS = {"Grid pressure": "grid_pressure"}   # e.g. add "Electricity demand": "electricity_demand"
tabs = st.tabs(list(SECTIONS))
for tab, module in zip(tabs, SECTIONS.values()):
    with tab:
        try:
            importlib.import_module(module).render()
        except Exception as e:
            st.error(f"Section failed to load: {e}")

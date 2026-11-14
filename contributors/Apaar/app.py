import streamlit as st
from water_dashboard import render_water_dashboard

st.set_page_config(page_title='Water, before expansion | Aqueduct', page_icon='💧', layout='wide')
render_water_dashboard()

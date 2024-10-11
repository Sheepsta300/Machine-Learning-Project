import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium
from folium.plugins import Search

# Leave this top area for prediction data to be read in

st.set_page_config(layout="wide")

st.title('New Zealand House Price Forecasting Map')

st.sidebar.header("Search for City")

nz_coordinates = [-41, 174]
nz_map = folium.Map(location=nz_coordinates, zoom_start = 7)

st_display_map = st_folium(nz_map, width=3000, height=1200)


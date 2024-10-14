import streamlit as st
import pandas as pd
import folium
import os
import xgboost as xg

from streamlit_folium import st_folium
from folium.plugins import Search


@st.cache_data
def get_data():
    cwd = os.getcwd()
    dir = f'{cwd}/datasets/regional'
    regional_data = []
    for file in os.listdir(dir):
        data = pd.read_csv(os.path.join(dir, file))
        data.index = data.date
        data.index = pd.to_datetime(data.index)
        data = data[[data.columns[2], data.columns[3]]] 
        regional_data.append(data)
    
    return regional_data

# def train_models(regional_data):
#     params = {'colsample_bytree': 0.9, 
#               'learning_rate': 0.1, 
#               'max_depth': 5, 
#               'min_child_weight': 5, 
#               'n_estimators': 100, 
#               'subsample': 1.0}
#     return

def main():
    st.set_page_config(layout="wide")
    
    regional_data = get_data()
    print([data.columns for data in regional_data])

    st.title('New Zealand House Price Forecasting Map')


    regions = {
        "Auckland": [-36.8509, 174.7645],
        "Bay of Plenty": [-38.165340, 176.771464],
        "Canterbury": [-43.495529, 171.655733],
        "Gisborne": [-38.6623, 178.0176],
        "Hawke's Bay": [-39.251823, 176.732583],
        "Manawatu": [-39.825695, 175.583917],
        "Marlborough": [-41.703693, 173.521309],
        "Nelson": [-41.2706, 173.2836],
        "Northland": [-35.515071, 173.862480],
        "Otago": [-45.265596, 169.703430],
        "Southland": [-45.719799, 168.012629],
        "Taranaki": [-39.374290, 174.407109],
        "Tasman": [-41.509514, 172.731471],
        "Waikato": [-37.501184, 175.107651],
        "Wellington": [-41.2924, 174.7787],
        "West Coast": [-43.082830, 170.493740]
    }


    region = st.selectbox(
        "Search for Region",
        list(regions.keys())
    )

    # Set default map location to New Zealand's center
    nz_coordinates = [-41.2924, 174.7787]
    nz_map = folium.Map(location=nz_coordinates, zoom_start=7)

    # Update map with selected region's coordinates
    region_coordinates = regions[region]
    nz_map = folium.Map(location=region_coordinates, zoom_start=8)

    # Optionally, add markers or other features based on the region
    folium.Marker(region_coordinates, popup=region).add_to(nz_map)

    # Display the map
    st_display_map = st_folium(nz_map, width=1200, height=800)

if __name__ == "__main__":
    main()
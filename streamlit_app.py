import streamlit as st
import pandas as pd
import folium
import os
import xgboost as xgb
import data_cleaning as dc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from streamlit_folium import st_folium
from folium.plugins import Search

global_regions = ['Auckland', 
           'Bay of Plenty', 
           'Canterbury', 
           'Gisborne', 
           "Hawke's Bay",
            'Manawatu', 
            'Marlborough', 
            'Nelson', 
            'Northland', 
            'Otago',
            'Southland', 
            'Taranaki', 
            'Tasman', 
            'Waikato', 
            'Wellington', 
            'West Coast']

@st.cache_data
def get_data():
    cwd = os.getcwd()
    dir = f'{cwd}/datasets/processed'
    regional_data = {}
    i = 0
    for file in os.listdir(dir):
        data = pd.read_csv(os.path.join(dir, file))
        dc.clean(data)
        regional_data[global_regions[i]] = data
        i+= 1
    return regional_data

def train_model(df):
    
    last_pred = None
    current_val = df.iloc[-1:].Price.values[0]
    for i in range(4):

        features = ['Year', 'Month', 'DayOfWeek', 'Spring', 'Summer', 'Winter',
                'Months_since_1992', 'lagged', 'Price_Lag_7', 
                'Price_Rolling_Mean_7', 'Price_Rolling_Mean_30']
        X = df[features]
        y = df['Price']

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X)
        
        params = {'colsample_bytree': 0.9, 
                'learning_rate': 0.1, 
                'max_depth': 3, 
                'min_child_weight': 3, 
                'n_estimators': 200, 
                'subsample': 1.0}
        best_model = xgb.XGBRegressor(**params, random_state=42)
        best_model.fit(X_train_scaled, y)

            
        temp_data = dc.add_row(df)
        last_pred = best_model.predict(scaler.transform(temp_data[-1:][features]))
        df.loc[df.index.values[-1], "Price"] = last_pred
        temp_data.loc[temp_data.index.values[-1], "Price"] = last_pred
    
    percentage_change = (last_pred[0] - current_val) / current_val
    return [last_pred[0], percentage_change]

@st.cache_data
def train_all_models():
    regional_data = get_data()
    predictions = {}
    for k, v in regional_data.items():
        predictions[k] = train_model(v)
    return predictions

def main():
    st.set_page_config(layout="wide")
    
    
    predictions = train_all_models()
    
    
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

    folium.Marker(region_coordinates, popup=f'''{region.upper()}\n 
                                            Predicted 2024 year end Median House Price: {predictions[region][0]}\n
                                            Predicted Change from now: {predictions[region][1]}''').add_to(nz_map)


    st_display_map = st_folium(nz_map, width=1200, height=800)

if __name__ == "__main__":
    main()
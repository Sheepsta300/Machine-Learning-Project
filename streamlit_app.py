import streamlit as st
import folium
import xgboost as xgb
import data_cleaning as dc
<<<<<<< HEAD
=======
import base64
from sklearn.model_selection import train_test_split
>>>>>>> 72eb5b6 (Updated popups, adding images)
from sklearn.preprocessing import StandardScaler

from streamlit_folium import st_folium
from folium.plugins import Search


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
    regional_data = dc.get_data()
    predictions = {}
    for k, v in regional_data.items():
        predictions[k] = train_model(v)
    return predictions

def main():
    st.set_page_config(layout="wide")
    
    
    predictions = train_all_models()
    
    
    st.title('New Zealand House Price Forecasting Map')

    regions = {
        "Auckland": {"coordinates":[-36.8509, 174.7645], "image": "Auckland.jpeg"},
        "Bay of Plenty": {"coordinates":[-38.165340, 176.771464],"image": "Bay of Plenty.jpeg"},
        "Canterbury": {"coordinates":[-43.495529, 171.655733],"image": "Canterbury.jpeg"},
        "Gisborne": {"coordinates":[-38.6623, 178.0176],"image": "Gisborne.jpeg"},
        "Hawke's Bay": {"coordinates":[-39.251823, 176.732583],"image": "Hawkes Bay.jpeg"},
        "Manawatu": {"coordinates":[-39.825695, 175.583917],"image": "Manawatu.jpeg"},
        "Marlborough": {"coordinates":[-41.703693, 173.521309],"image": "Marlborough.jpeg"},
        "Nelson": {"coordinates":[-41.2706, 173.2836],"image": "Nelson.jpeg"},
        "Northland": {"coordinates":[-35.515071, 173.862480],"image": "Northland.jpeg"},
        "Otago": {"coordinates":[-45.265596, 169.703430],"image": "Otago.jpeg"},
        "Southland": {"coordinates":[-45.719799, 168.012629],"image": "Southland.jpeg"},
        "Taranaki": {"coordinates":[-39.374290, 174.407109],"image": "Taranaki.jpeg"},
        "Tasman": {"coordinates":[-41.509514, 172.731471],"image": "Tasman.jpeg"},
        "Waikato": {"coordinates":[-37.501184, 175.107651],"image": "Waikato.jpeg"},
        "Wellington": {"coordinates":[-41.2924, 174.7787],"image": "Wellington.jpeg"},
        "West Coast": {"coordinates":[-43.082830, 170.493740],"image": "West Coast.jpeg"},
    }
    
    
    region = st.selectbox(
        "Search for Region",
        list(regions.keys())
    )

    # Set default map location to New Zealand's center
    nz_coordinates = [-41.2924, 174.7787]
    nz_map = folium.Map(location=nz_coordinates, zoom_start=7)

    # Update map with selected region's coordinates and images
    region_coordinates = regions[region]["coordinates"]
    image_files = regions[region]["image"]
    
    # Create a path to the images folder
    region_images_folder = "images"
    region_image_path = os.path.join(region_images_folder, image_files)
    
    # Had to look in to this but apparently it is a better way to embed images in a web app in Folium 
    with open(region_image_path, "rb") as reg_img_file:
        converted_image = base64.b64encode(reg_img_file.read()).decode("utf-8")

<<<<<<< HEAD
    folium.Marker(region_coordinates, popup=f'''{region.upper()}\n 
                                            Predicted 2024 year end Median House Price: ${predictions[region][0]}\n
                                            Predicted Change from now: {predictions[region][1]}''').add_to(nz_map)
=======
    # Have placed some basic styling for the popups
    # need to use html for folium popups  
    popup_styling = f'''
        <div style="font-family: Verdana, sans-serif;text-align: center; width: 250px;">
            <h3 style="margin-bottom: 10px;"><strong>{region.upper()}</strong></h3>
            <img src="data:image/jpeg;base64,{converted_image}" alt="{region}" style="width: 100%; height: auto; margin-bottom: 10px;">
            <p><strong>Predicted 2024 Year End Median House Price:</strong></p><p>${predictions[region][0]}</p>
            <p><strong>Predicted Change from Now:</strong></p><p>${predictions[region][1]}</p>
        </div>
    '''
    popup_marker = folium.Popup(popup_styling, max_width=300)
    folium.Marker(region_coordinates, popup=popup_marker).add_to(nz_map)
>>>>>>> 72eb5b6 (Updated popups, adding images)


    st_display_map = st_folium(nz_map, width=2000, height=800)

if __name__ == "__main__":
    main()
import pandas as pd
import os
import streamlit as st

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
        clean(data)
        regional_data[global_regions[i]] = data
        i+= 1
    return regional_data

def clean(df):
    df.index = df.date
    df.index = pd.to_datetime(df.index)
    df = df[[df.columns[2], df.columns[3]]] 
    return df

def get_season(date):
    if date.month >= 9 and date.month <= 11:
        return "Spring"
    if date.month >= 3 and date.month <= 5:
        return "Autumn"
    if date.month >= 6 and date.month <= 8:
        return "Winter"
    return "Summer"

def add_row(df):
    date =  df[-1:].index + pd.tseries.offsets.MonthEnd()
    df.loc[-1] = 0
    df.index.values[-1] = date[0]
    df.index = pd.to_datetime(df.index)
    df['Month'] = [date.month for date in df.index]
    df['Season'] = [get_season(date) for date in df.index]
    df['Summer'] = [True if season == "Summer" else False for season in df['Season'].values]
    df['Winter'] = [True if season == "Winter" else False for season in df['Season'].values]
    df['Spring'] = [True if season == "Spring" else False for season in df['Season'].values]
    df['Autumn'] = [True if season == "Autumn" else False for season in df['Season'].values]
    df['Year'] = [date.year for date in df.index]
    df['Months_since_1992'] = [(date.year - min(df.index).year) * 12 + date.month - min(df.index).month for date in df.index]
    df['DayOfWeek'] = df.index.dayofweek
    
    df['lagged'] = df['Price'].shift(1)
    df['Price_Lag_7'] = df['Price'].shift(7)
    df['Price_Rolling_Mean_7'] = df['lagged'].rolling(window=7).mean()
    df['Price_Rolling_Mean_30'] = df['lagged'].rolling(window=30).mean()
    return df.dropna()

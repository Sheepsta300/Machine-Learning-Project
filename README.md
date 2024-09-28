# 🏡 Housing Price Predictor for Aotearoa

## Overview
This project aims to predict housing prices across different regions of Aotearoa (New Zealand) using machine learning models and historical data. We incorporate regional economic indicators, property attributes, and time-series data to build a model that forecasts housing prices. The final output is an interactive demo where regions are color-coded based on predicted price ranges, offering a visual and intuitive way to explore housing market trends.

## Features
- **Time-Series Forecasting**: Predicts housing prices based on historical data trends.
- **Regional Breakdown**: Offers insights into housing prices across different regions, including urban and rural areas.
- **Economic Indicators**: Utilizes economic data like interest rates, unemployment, and inflation as features.
- **Interactive Visualization**: Visualizes regional price predictions on a map of Aotearoa, color-coded from green (less expensive) to red (more expensive).
- **Model Evaluation**: Provides model performance metrics such as Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

## Data Sources
- **Real Estate New Zealand (REINZ)**: Property sales and housing price data.
- **Geospatial Data**: Regional and district-level geographic features.
- **Economic Indicators**: Data on interest rates, inflation, unemployment, etc.
- **Government and Open Data Portals**: Various economic and property datasets.

## Predictive Model
Our machine learning model predicts housing prices using:
- **Linear Regression**: As a baseline model to assess performance.
- **Random Forest Regressor / XGBoost**: To capture complex relationships in the data.
- **Gradient Boosting**: For advanced modelling

## App Demonstration
The final project delivers an interactive app built with **Dash** or **Streamlit** that presents predicted housing prices across Aotearoa. Key features of the app include:
- A **map of New Zealand**, with regions color-coded to indicate housing price predictions.
  - **Green**: More affordable regions.
  - **Red**: More expensive regions.
- Users can click on each region to see detailed price trends and breakdowns of contributing factors.
import streamlit as st
import numpy as np  
import pandas as pd
from datetime import date
st.set_page_config(layout='wide')
# Libraries for retrieving and downloading data
import requests 
from io import BytesIO
import base64 

# Plotting libraries
import plotly.express as px
import plotly.graph_objects as go

# Customs modules
from modules.assets import AssetManager
from modules.utils import SessionState
from modules.data import download_data

@st.cache(allow_output_mutation=True)
def get_session():
    return SessionState()

session_state = get_session()
session_state.data = pd.DataFrame()

# Streamlit APP
st.title("Efficient Portfolio Tool")
st.header("Pick your assets", divider="rainbow")


with st.sidebar:
    st.subheader("Times Series Resampler")

    freq_to_resample = st.selectbox('Freq to resample:', ['Daily','Weekly','Quartely','Monthly'], index=1)
    aggregation = st.selectbox('Aggregation', ['sum', 'mean', 'median', 'valor exacto'], index=1)

    if st.button('Resample Dataframe'):
        pass

    st.subheader("Moving Average")

    days = st.number_input('Day(s)', min_value=1, max_value=100, value=3)
    method = st.selectbox('Method', ['gap', 'rolling'], index=1)

    if st.button('Apply'):
        pass

    st.subheader('Missing Values')

    if st.button('Drop NAs'):
        pass


# select box widget to choose timeframes
selected_timeframes = st.selectbox('Select Timeframe:', ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=7)

# creating a dictionary of dictionaries with all available tickers
asset_manager = AssetManager()
assets_list = {
    'CURRENCIES': asset_manager.CURRENCIES,
    'CRYPTO': asset_manager.CRYPTO,
    'B3_STOCKS': asset_manager.B3_STOCKS,
    'SP500': asset_manager.SP500,
    'NASDAQ100': asset_manager.NASDAQ100,
    'INDEXES': asset_manager.INDEXES 
}

# combining dictionaries when the user selects one or more in assets_list
selected_dict_names = st.multiselect('Select dictionaries to combine', list(assets_list.keys()))
combined_dict = {}
for name in selected_dict_names:
    dictionary = assets_list.get(name)
    if dictionary:
        combined_dict.update(dictionary)

# dictionary to actually store retrieved data
selected_ticker_dict = {}

# looping through the chosen tickers
if selected_dict_names:
    # the list to iterate over tickers
    tickers = st.multiselect('Asset Selection', list(combined_dict.keys()))
    if tickers and st.button("Download data"):
        for key in tickers:
            if key in combined_dict:
                selected_ticker_dict[key] = combined_dict[key]
        # Assigning data object as the result of the function download_data
        session_state.data = download_data(selected_ticker_dict, selected_timeframes)

# Handle tickers entered manually
type_tickers = st.text_input('Enter Tickers (comma-separated):')
if type_tickers and st.button("Download data"):
    tickers = [ticker.strip() for ticker in type_tickers.split(',')]
    # doing the same for tickers separated by commas
    session_state.data = download_data(tickers, selected_timeframes)

if not session_state.data.empty:
    st.dataframe(session_state.data)
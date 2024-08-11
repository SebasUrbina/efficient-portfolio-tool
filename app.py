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
from modules.plots import Plots
from modules.portfolio import *

@st.cache(allow_output_mutation=True)
def get_session():
    return SessionState()

session_state = get_session()

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
        session_state.data = session_state.data.dropna()
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

    charts = Plots(session_state.data)

    charts.plot_log_returns()

    charts.plot_return_over_time()

    st.subheader('Assets Allocation', divider='rainbow')

    invested_cash = st.number_input('Enter invested cash', min_value=1, max_value=None, value=1000)

    st.subheader('Optimization', divider='rainbow')

    c1, c2 = st.columns([1,3], vertical_alignment='bottom')
    
    with c1:
        trading_days = st.number_input('Please Select timeframe for returns', min_value=1, max_value=365, value=252)
        resampler = st.selectbox('Select Timeframe:', ['A', 'AS', 'BA', 'BAS', '3M', '4M', '6M', '12M', 'Q', 'BQ', 'QS', 'BQS', 'M', 'BM', 'MS', 'BMS', 'W', 'D'], index=0)
        risk_free_rate = st.number_input('Please Select risk free rate', min_value=0.0, max_value=1.0, value=0.05)
        risk_taken = st.number_input('Please Select anualized risk of investment:', min_value=0.0, max_value=1.0, value=0.1)
        expected_return = st.number_input('Please Select anualized expected returns', min_value=0.0, max_value=1.0, value=0.15)
        simulated_portfolios = st.number_input('Please Select anualized expected returns', min_value=1, max_value=10000, value=1000)

        run_simulation = st.button('Run simulations')
    with c2:
        if run_simulation:
            simulated_portfolios = efficient_frontier(
                session_state.data.filter(like='_Close'), 
                trading_days, 
                risk_free_rate,
                simulations= simulated_portfolios, 
                resampler=resampler
            )
            
            # st.write(simulated_portfolios)

            charts.plot_efficient_frontier(
                simulated_portfolios=simulated_portfolios, 
                expected_sharpe=1, 
                expected_return=expected_return, 
                risk_taken=risk_taken
                )
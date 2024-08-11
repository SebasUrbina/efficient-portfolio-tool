import yfinance as yf
import pandas as pd

def download_data(data, period='1y'):
    dfs = []
    if isinstance(data, dict):
        for name, ticker in data.items():
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period=period) # timeframe
            hist.columns = [f"{name}_{col}" for col in hist.columns]  # Add prefix to the name
            hist.index = pd.to_datetime(hist.index.map(lambda x: x.strftime('%Y-%m-%d')))
            dfs.append(hist)
    elif isinstance(data, list):
        for ticker in data:
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period=period)
            # Add prefix to each close price column
            hist.columns = [f'{ticker}_{col}' for col in hist.columns]  
            hist.index = pd.to_datetime(hist.index.map(lambda x: x.strftime('%Y-%m-%d')))
            dfs.append(hist)
    # Use join='outer' to handle different data indices
    combined_df = pd.concat(dfs, axis=1, join='outer')

    return combined_df
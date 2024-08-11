import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

class Plots:
    def __init__(self, df: pd.DataFrame) -> None:
        """Inicializa la clase Plots con un DataFrame."""
        self.df = df

    def plot_log_returns(self) -> None:
        """Calcula y grafica los retornos logarítmicos de los precios de cierre."""
        # Filtrar las columnas de precios de cierre y renombrarlas
        close_prices = self.df.filter(like='_Close').dropna()
        close_prices.columns = close_prices.columns.str.split('_').str[0]
        
        # Calcular los retornos logarítmicos
        log_returns = np.log(close_prices / close_prices.shift(1)).dropna()
        
        # Transformar a formato largo para facilitar la visualización
        log_returns_long = log_returns.reset_index().melt(id_vars=["Date"], var_name="Currency", value_name="Log Return")
        
        # Graficar los retornos logarítmicos
        fig = px.line(
            log_returns_long, 
            x='Date', 
            y='Log Return',
            color='Currency',
            labels={'Log Return': 'Log Returns'},
            title='Log Returns Over Time'
        )
        fig.update_layout(legend_title_text='Assets')
        st.plotly_chart(fig)

    def plot_return_over_time(self) -> None:
        """Calcula y grafica los retornos acumulados sobre el tiempo."""
        # Filtrar las columnas de precios de cierre y renombrarlas
        close_prices = self.df.filter(like='_Close').dropna()
        close_prices.columns = close_prices.columns.str.split('_').str[0]
        
        # Calcular los retornos acumulados
        return_df = close_prices / close_prices.iloc[0] - 1
        
        # Transformar a formato largo para facilitar la visualización
        return_df_long = return_df.reset_index().melt(id_vars=["Date"], var_name="Currency", value_name="Cumulative Return")
        
        # Graficar los retornos acumulados
        fig = px.line(
            return_df_long, 
            x='Date', 
            y='Cumulative Return',
            color='Currency',
            labels={'Cumulative Return': 'Cumulative Returns'},
            title='Cumulative Returns Over Time'
        )
        fig.update_layout(legend_title_text='Assets')
        st.plotly_chart(fig)

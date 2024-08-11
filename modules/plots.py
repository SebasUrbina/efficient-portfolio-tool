import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

    def plot_efficient_frontier(
        self, 
        simulated_portfolios: pd.DataFrame, 
        expected_sharpe: float, 
        expected_return: float, 
        risk_taken: float
        ) -> None:
        """
        Grafica la frontera eficiente de Markowitz con los portafolios simulados.

        :param simulated_portfolios: DataFrame con los portafolios simulados y sus métricas.
        :param expected_sharpe: Ratio de Sharpe esperado para destacar en el gráfico.
        :param expected_return: Retorno esperado para resaltar en el gráfico.
        :param risk_taken: Volatilidad objetivo para resaltar en el gráfico.
        """
        simulated_portfolios = simulated_portfolios.sort_values(by='Volatility')
        
        # Concatenar los pesos para poder verlos al seleccionar puntos de datos
        simulated_portfolios['Weights'] = (
            simulated_portfolios
                .iloc[:, 2:-1]
                .apply(
                    lambda row: '<br>'.join([f'{asset}: {weight:.4f}' for asset, weight in zip(simulated_portfolios.columns[2:-1], row)]),
                    axis=1
                    )
            )
        
        # Crear el gráfico como un gráfico de dispersión
        frontier = px.scatter(
            simulated_portfolios, 
            x='Volatility', 
            y='Returns', 
            width=1200, 
            height=600, 
            title="Markowitz's Efficient Frontier", 
            labels={'Volatility': 'Volatility', 'Returns': 'Return'},
            hover_name='Weights'
        )
        
        # Resaltar el portafolio con el máximo Sharpe Ratio en verde
        max_sharpe_ratio_portfolio = simulated_portfolios.loc[simulated_portfolios['Sharpe_ratio'].idxmax()]
        frontier.add_trace(
            go.Scatter(
                x=[max_sharpe_ratio_portfolio['Volatility']], 
                y=[max_sharpe_ratio_portfolio['Returns']],
                mode='markers',
                marker=dict(color='green', size=10),
                name='Max Sharpe Ratio',
                text=max_sharpe_ratio_portfolio['Weights']
            )
        )
        
        # Resaltar los portafolios con retornos esperados y riesgo asumido en púrpura
        low_risk_portfolios = simulated_portfolios[
            (simulated_portfolios['Returns'] >= expected_return) & 
            (simulated_portfolios['Volatility'] <= risk_taken)
        ]
        frontier.add_trace(
            go.Scatter(
                x=low_risk_portfolios['Volatility'], 
                y=low_risk_portfolios['Returns'],
                mode='markers',
                marker=dict(color='purple', size=5),
                name='Expected Return & Risk Taken',
                text=low_risk_portfolios['Weights']
            )
        )
        
        # Resaltar los portafolios con el ratio de Sharpe esperado en naranja
        expected_portfolio = simulated_portfolios[
            (simulated_portfolios['Sharpe_ratio'] >= expected_sharpe - 0.001) & 
            (simulated_portfolios['Sharpe_ratio'] <= expected_sharpe + 0.001)
        ]
        if not expected_portfolio.empty:
            frontier.add_trace(
                go.Scatter(
                    x=[expected_portfolio['Volatility'].values[0]], 
                    y=[expected_portfolio['Returns'].values[0]],
                    mode='markers',
                    marker=dict(color='orange', size=10),
                    name='Expected Sharpe Ratio',
                    text=expected_portfolio['Weights']
                )
            )
        
        # Resaltar el portafolio con la menor volatilidad en rojo
        frontier.add_trace(
            go.Scatter(
                x=[simulated_portfolios.iloc[0]['Volatility']], 
                y=[simulated_portfolios.iloc[0]['Returns']],
                mode='markers',
                marker=dict(color='red', size=10),
                name='Min Volatility', 
                text=simulated_portfolios.iloc[0]['Weights']
            )
        )
        
        # Configurar el diseño del gráfico
        frontier.update_layout(
            legend=dict(
                orientation='h',
                yanchor='top',
                y=1.1,
                xanchor='center',
                x=0.5
            )
        )
        st.plotly_chart(frontier)
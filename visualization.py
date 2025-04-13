# visualization.py
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_stock_data(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Cria um gráfico de preços de fechamento de uma ação.
    
    Args:
        df: DataFrame com colunas 'Date' e 'Close'
        ticker: Código da ação (ex.: 'PETR4')
    
    Returns:
        go.Figure: Gráfico Plotly
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        name=f'{ticker} Close',
        line=dict(color='blue')  # Define a cor da linha
    ))
    fig.update_layout(
        title=f'Preço de Fechamento - {ticker}',
        xaxis_title='Data',
        yaxis_title='Preço (R$)',
        template='plotly_dark',  # Tema escuro para combinar com o Streamlit
        hovermode='x unified'    # Mostra informações ao passar o mouse
    )
    return fig

def plot_predictions(df: pd.DataFrame, predictions: np.ndarray, ticker: str) -> go.Figure:
    """
    Cria um gráfico com preços históricos e previsões.
    
    Args:
        df: DataFrame com colunas 'Date' e 'Close'
        predictions: Array com previsões para os próximos 5 dias
        ticker: Código da ação (ex.: 'PETR4')
    
    Returns:
        go.Figure: Gráfico Plotly
    """
    fig = go.Figure()
    
    # Preços históricos
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        name='Preço Real',
        line=dict(color='blue')
    ))
    
    # Previsões
    forecast_dates = pd.date_range(start=df['Date'].iloc[-1], periods=len(predictions)+1, freq='B')[1:]  # Dias úteis
    fig.add_trace(go.Scatter(
        x=forecast_dates,
        y=predictions.flatten(),
        mode='lines',
        name='Previsão (5 dias)',
        line=dict(color='orange', dash='dash')  # Linha tracejada para previsões
    ))
    
    fig.update_layout(
        title=f'Previsão de Preços - {ticker}',
        xaxis_title='Data',
        yaxis_title='Preço (R$)',
        template='plotly_dark',
        hovermode='x unified'
    )
    return fig

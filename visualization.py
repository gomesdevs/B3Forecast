# visualization.py
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def plot_stock_data(df: pd.DataFrame, ticker: str) -> go.Figure:
    # Calcular média móvel de 20 dias
    df['MA20'] = df['Close'].rolling(window=20).mean()
    
    # Criar figura com eixo secundário para volume
    fig = go.Figure()
    
    # Gráfico de preços
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        name=f'{ticker} Close',
        line=dict(color='blue')
    ))
    
    # Média móvel
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['MA20'],
        mode='lines',
        name='Média Móvel (20 dias)',
        line=dict(color='orange', dash='dash')
    ))
    
    # Gráfico de volume (eixo secundário)
    fig.add_trace(go.Bar(
        x=df['Date'],
        y=df['Volume'],
        name='Volume',
        marker_color='rgba(128, 128, 128, 0.5)',
        yaxis='y2'
    ))
    
    # Atualizar layout com dois eixos y
    fig.update_layout(
        title=f'Preço de Fechamento - {ticker}',
        xaxis_title='Data',
        yaxis_title='Preço (R$)',
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        template='plotly_dark',
        legend=dict(x=0, y=1.1, orientation='h')
    )
    return fig

def plot_predictions(df: pd.DataFrame, predictions: np.ndarray, ticker: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines',
        name='Preço Real'
    ))
    forecast_dates = pd.date_range(start=df['Date'].iloc[-1], periods=len(predictions)+1, freq='B')[1:]
    fig.add_trace(go.Scatter(
        x=forecast_dates,
        y=predictions.flatten(),
        mode='lines',
        name='Previsão (5 dias)',
        line=dict(dash='dash')
    ))
    fig.update_layout(
        title=f'Previsão de Preços - {ticker}',
        xaxis_title='Data',
        yaxis_title='Preço (R$)',
        template='plotly_dark'
    )
    return fig

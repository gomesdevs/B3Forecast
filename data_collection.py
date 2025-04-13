# data_collection.py
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import requests

@st.cache_data
def fetch_stock_data(ticker: str, start_date: str = None, end_date: str = None) -> tuple:
    """
    Coleta dados históricos de uma ação usando a API do Alpha Vantage.
    
    Args:
        ticker: Código da ação (ex.: 'PETR4.SA')
        start_date: Data inicial (formato 'YYYY-MM-DD')
        end_date: Data final (formato 'YYYY-MM-DD')
    
    Returns:
        Tuple: (DataFrame com dados, mensagem de erro se houver)
    """
    # Configuração da API do Alpha Vantage
    API_KEY = "YOUR_API_KEY"  # Substitua por sua chave API
    BASE_URL = "https://www.alphavantage.co/query"

    if not ticker.endswith('.SA'):
        ticker += '.SA'

    if not start_date:
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    # Validar se o intervalo contém dias úteis
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    date_range = pd.date_range(start=start, end=end)
    business_days = sum(1 for day in date_range if day.weekday() < 5)
    if business_days == 0:
        return pd.DataFrame(), f"O período especificado ({start_date} a {end_date}) não contém dias úteis."

    # Parâmetros da requisição
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "full",  
        "apikey": KBOIXH9LTSSOR4KY
    }

    try:
        # Fazer a requisição à API
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Levanta uma exceção para erros HTTP
        data = response.json()

        # Verificar se há erro na resposta
        if "Error Message" in data:
            return pd.DataFrame(), f"Erro na API do Alpha Vantage: {data['Error Message']}"
        if "Time Series (Daily)" not in data:
            return pd.DataFrame(), f"Dados não disponíveis para {ticker} no período especificado ({start_date} a {end_date})."

        # Converter os dados para DataFrame
        time_series = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(time_series, orient='index')
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)

        # Filtrar pelo período solicitado
        df = df[(df.index >= start) & (df.index <= end)]
        if df.empty:
            return pd.DataFrame(), f"Dados vazios para {ticker} no período especificado ({start_date} a {end_date})."

        # Reorganizar colunas e resetar índice
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Date'}, inplace=True)

        return df, None

    except Exception as e:
        return pd.DataFrame(), f"Erro ao coletar dados para {ticker}: {str(e)}"

def get_available_tickers() -> list:
    """
    Retorna uma lista de tickers populares da B3.
    """
    return ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3']

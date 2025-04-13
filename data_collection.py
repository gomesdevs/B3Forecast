# data_collection.py
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import requests

@st.cache_data
def fetch_stock_data(ticker: str, start_date: str = None, end_date: str = None) -> tuple:
    """
    Coleta dados históricos de uma ação usando a API do EODHD.
    
    Args:
        ticker: Código da ação (ex.: 'PETR4.SA')
        start_date: Data inicial (formato 'YYYY-MM-DD')
        end_date: Data final (formato 'YYYY-MM-DD')
    
    Returns:
        Tuple: (DataFrame com dados, mensagem de erro se houver)
    """
    # Configuração da API do EODHD
    API_KEY = "67fbec3a8b3891.80065862"  # Sua chave API do EODHD
    BASE_URL = "https://eodhd.com/api/eod"

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
        "api_token": API_KEY,
        "fmt": "json",
        "from": start_date,
        "to": end_date
    }

    try:
        # Fazer a requisição à API
        url = f"{BASE_URL}/{ticker}"
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta uma exceção para erros HTTP
        data = response.json()

        # Verificar se a resposta contém dados
        if not data:
            st.warning(f"Dados vazios retornados para {ticker} no período {start_date} a {end_date}.")
            return pd.DataFrame(), f"Dados vazios para {ticker} no período especificado ({start_date} a {end_date})."

        # Converter os dados para DataFrame
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.rename(columns={
            "date": "Date",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        })

        # Filtrar pelo período solicitado (embora a API já deva ter feito isso)
        df = df[(df['Date'] >= start) & (df['Date'] <= end)]
        if df.empty:
            st.warning(f"Dados vazios retornados para {ticker} no período {start_date} a {end_date} após filtragem.")
            return pd.DataFrame(), f"Dados vazios para {ticker} no período especificado ({start_date} a {end_date})."

        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']], None

    except Exception as e:
        st.warning(f"Erro ao coletar dados para {ticker}: {str(e)}")
        return pd.DataFrame(), f"Erro ao coletar dados para {ticker}: {str(e)}"

def get_available_tickers() -> list:
    """
    Retorna uma lista de tickers populares da B3.
    """
    return ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3']

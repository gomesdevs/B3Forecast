# data_collection.py
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import time
import os

@st.cache_data
def fetch_stock_data(ticker: str, start_date: str = None, end_date: str = None, retries: int = 3) -> tuple:
    original_ticker = ticker
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

    # Tentar coletar dados do Yahoo Finance
    tickers_to_try = [ticker, original_ticker]
    for t in tickers_to_try:
        for attempt in range(retries):
            try:
                stock = yf.Ticker(t)
                df = stock.history(start=start_date, end=end_date)
                if df.empty:
                    st.warning(f"Dados vazios retornados para {t} no período {start_date} a {end_date}.")
                    break
                df.reset_index(inplace=True)
                df['Date'] = pd.to_datetime(df['Date'])
                return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']], None
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(2)
                    continue
                st.warning(f"Erro ao coletar dados para {t} após {retries} tentativas: {str(e)}.")

    # Fallback: usar dados locais se disponíveis
    fallback_file = f"{original_ticker}_historical.csv"
    if os.path.exists(fallback_file):
        try:
            df = pd.read_csv(fallback_file)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df[(df['Date'] >= start) & (df['Date'] <= end)]
            if df.empty:
                return pd.DataFrame(), f"Dados locais para {original_ticker} não cobrem o período especificado ({start_date} a {end_date})."
            return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']], None
        except Exception as e:
            return pd.DataFrame(), f"Erro ao carregar dados locais para {original_ticker}: {str(e)}"
    
    return pd.DataFrame(), f"Sem dados disponíveis para {original_ticker} no período especificado ({start_date} a {end_date}) e nenhum dado local encontrado."

def get_available_tickers() -> list:
    return ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3']

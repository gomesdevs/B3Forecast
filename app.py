# app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from data_collection import fetch_stock_data, get_available_tickers
from preprocessing import prepare_data, split_data
from model import build_lstm_model, train_model, predict
from visualization import plot_stock_data, plot_predictions
from utils import get_default_dates

# Configuração da página
st.set_page_config(page_title="B3Forecast", layout="wide")
st.title("📈 B3Forecast - Previsão de Ações")
st.markdown("Preveja tendências de curto prazo para ações da B3 com redes neurais LSTM.")

# Sidebar para seleção
st.sidebar.header("Configurações")
ticker = st.sidebar.selectbox("Selecione a Ação", get_available_tickers())
start_date, end_date = get_default_dates()
start_date = st.sidebar.date_input("Data Inicial", pd.to_datetime(start_date))
end_date = st.sidebar.date_input("Data Final", pd.to_datetime(end_date))

# Validar a data final
current_date = pd.to_datetime("2025-04-12")
if end_date > current_date.date():
    st.sidebar.warning(f"A data final foi ajustada para {current_date.date()} (data atual).")
    end_date = current_date.date()

# Validar o intervalo de datas
if start_date >= end_date:
    st.sidebar.error("A data inicial deve ser anterior à data final.")
    st.stop()

# Exibir as datas selecionadas para depuração
st.sidebar.write(f"Período selecionado: {start_date} a {end_date}")

predict_button = st.sidebar.button("Prever")

# Coleta de dados
if ticker:
    df, error_message = fetch_stock_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    
    if not df.empty:
        # Arredondar os valores para 2 casas decimais
        df_display = df.copy()
        df_display[['Open', 'High', 'Low', 'Close']] = df_display[['Open', 'High', 'Low', 'Close']].round(2)
        
        # Calcular a variação percentual
        if len(df_display) > 1:
            initial_price = df_display['Close'].iloc[0]
            final_price = df_display['Close'].iloc[-1]
            variation = ((final_price - initial_price) / initial_price) * 100
            st.subheader(f"Variação de Preço - {ticker}")
            st.write(f"Variação no período: {variation:.2f}%")
        
        # Exibir dados brutos
        st.subheader(f"Dados Históricos - {ticker}")
        st.dataframe(df_display.tail())
        
        # Plotar preços
        st.subheader("Preço de Fechamento")
        fig = plot_stock_data(df, ticker)
        st.plotly_chart(fig, use_container_width=True)
        
        # Treinamento e previsão
        if predict_button:
            with st.spinner("Treinando modelo e gerando previsões..."):
                # Preparar dados
                X, y, scaler = prepare_data(df, sequence_length=60)
                X_train, X_test, y_train, y_test = split_data(X, y)
                
                # Construir e treinar modelo
                model = build_lstm_model(sequence_length=60)
                model = train_model(model, X_train, y_train, epochs=5)
                
                # Prever 5 dias
                last_sequence = X[-1:]
                predictions = []
                for _ in range(5):
                    pred = model.predict(last_sequence, verbose=0)
                    predictions.append(pred[0, 0])
                    last_sequence = np.roll(last_sequence, -1, axis=1)
                    last_sequence[0, -1, 0] = pred
                
                predictions = np.array(predictions).reshape(-1, 1)
                predictions = scaler.inverse_transform(predictions)
                
                # Exibir previsões
                st.subheader("Previsão para os Próximos 5 Dias")
                fig_pred = plot_predictions(df, predictions, ticker)
                st.plotly_chart(fig_pred, use_container_width=True)
    else:
        st.error(f"Não foi possível coletar dados para esta ação. Detalhes: {error_message}")

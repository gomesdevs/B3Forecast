# preprocessing.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def prepare_data(df: pd.DataFrame, target_col: str = 'Close', sequence_length: int = 60) -> tuple:
    """
    Prepara dados para o modelo LSTM.
    
    Args:
        df: DataFrame com coluna 'Close'
        target_col: Coluna alvo para previsão
        sequence_length: Tamanho da sequência temporal
    
    Returns:
        Tuple: (X, y, scaler)
    """
    # Normalização
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[[target_col]])
    
    # Criação de sequências
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i])
        y.append(scaled_data[i])
    
    X = np.array(X)
    y = np.array(y)
    
    return X, y, scaler

def split_data(X: np.ndarray, y: np.ndarray, train_ratio: float = 0.8) -> tuple:
    """
    Divide dados em treino e teste.
    
    Returns:
        Tuple: (X_train, X_test, y_train, y_test)
    """
    train_size = int(len(X) * train_ratio)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    return X_train, X_test, y_train, y_test

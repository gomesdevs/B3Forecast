
# model.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def build_lstm_model(sequence_length: int) -> Sequential:

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(model: Sequential, X_train: np.ndarray, y_train: np.ndarray, 
                epochs: int = 10, batch_size: int = 32) -> Sequential:
   
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    return model

def predict(model: Sequential, X: np.ndarray, scaler: MinMaxScaler) -> np.ndarray:
  
    predictions = model.predict(X)
    return scaler.inverse_transform(predictions)

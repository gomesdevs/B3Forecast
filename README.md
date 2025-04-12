# B3Forecast

## LSTM-Based Stock Prediction for Brazilian Market

B3Forecast is a machine learning application that predicts short-term trends for stocks listed on B3 (Brazil's Stock Exchange) using LSTM neural networks and technical analysis.

## Features

- Real-time data collection from major Brazilian stocks
- LSTM-based prediction model for 5-day forecasting
- Interactive dashboard with Streamlit
- Technical indicators visualization
- Performance metrics and model evaluation

## Technology Stack

- Python 3.8+
- TensorFlow/Keras for LSTM implementation
- Pandas & NumPy for data manipulation
- yfinance for market data acquisition
- Plotly for interactive visualizations
- Streamlit for web dashboard

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Required packages listed in requirements.txt

### Installation
```bash
# Clone this repository
git clone https://github.com/yourusername/b3forecast.git

# Navigate to the project directory
cd b3forecast

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# utils.py
from datetime import datetime, timedelta

def get_default_dates() -> tuple:
   
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    return start_date, end_date

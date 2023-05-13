'''
This script is used to call wolframalpha and aplhavantage apis

'''

#imports
import config
import wolframalpha
import requests
import datetime
import yfinance as yf
import numpy as np




API_KEY = config.ALPHA_VANTAGE_KEY
BASE_URL = "https://www.alphavantage.co/query"






def fetch_data(symbol: str,function:str) -> dict:
    """
    Fetches data for a given stock symbol.

    Args:
        symbol (str): The stock symbol.
        function (str):The function value.
    Returns:
        dict: A dictionary containing the stock symbol and chart data.
    """
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=5min&apikey={API_KEY}'.format(function,symbol,API_KEY)
    response = requests.get(url)
    json_data = response.json()
    if "Note" in json_data:
        return {"status":"bad","message":"API CALL LIMIT REACHED!Try Again After Some Time."}
    if "Error Message" in json_data:
        return {"status":"bad","message":"Invalid Api Call!"}
    try:
        if function=="TIME_SERIES_INTRADAY":
            time_series = json_data["Time Series (5min)"]

        elif function=="TIME_SERIES_WEEKLY":
            time_series = json_data["Weekly Time Series"]
        elif function=="TIME_SERIES_MONTHLY":
            time_series = json_data["Monthly Time Series"]
    except Exception as e:
        return {"status":"bad","message":"Error! can't display chart. Try again."}
    chart_data = [
    {
    "date": date,
    "open": float(data["1. open"]),
    "high": float(data["2. high"]),
    "low": float(data["3. low"]),
    "close": float(data["4. close"]),
    "volume": int(data["5. volume"]),
    }
    for date, data in time_series.items()
    ]
    

    j={
        "status":"ok",
        "symbol": symbol,
        "chart_data": chart_data,
        }
    return j


def get_eq(data: list, degree: int) -> dict:
    """
    Fetches the result equation for the specified degree polynomial fit using Alpha Vantage API data.

    Args:
        data (list): List of dictionaries containing 'date' and 'close' keys.
        degree (int): Degree of fit.

    Returns:
        dict: A dictionary containing the status and the equation message.
    """
    dates = [datetime.datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S').timestamp() for item in data]
    prices = [item['close'] for item in data]

    try:
        if len(dates) < degree + 1:
            return {"status": "bad", "message": "Insufficient data points for the specified degree."}

        coefficients = np.polyfit(dates, prices, degree)
        equation = np.poly1d(coefficients)

        return {"status": "ok", "message": str(equation)}
    except Exception as e:
        return {"status": "bad", "message": f"Error fitting curve: {str(e)}"}



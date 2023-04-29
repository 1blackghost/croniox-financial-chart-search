'''
This script is used to call wolframalpha and aplhavantage apis

'''

#imports
import config
import wolframalpha
import requests


API_KEY = config.ALPHA_VANTAGE_KEY
BASE_URL = "https://www.alphavantage.co/query"
WOLFRAM_ALPHA_API_KEY = config.WOLFRAM_ALPHA_KEY




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


def get_eq(data: list, degree: int) -> str:
    """
    Fetches result equation for degree for the specified data points

    Args:
        data (list): List of dictionaries containing 'date' and 'close' keys.
        degree (int): degree of fit

    Returns:
        str: A str of equation.
    """

    if not data:
        return "No data available."
    
    if not all(isinstance(d, dict) and 'date' in d and 'close' in d for d in data):
        return "Invalid data format."
    
    data_points = ", ".join(f"({item['date']}, {item['close']})" for item in data)
    query = f"polynomial fit of degree {degree} for {{ {data_points} }}"
    client = wolframalpha.Client(WOLFRAM_ALPHA_API_KEY)
    result = client.query(query)
    equation = next(result.results).text
    return equation


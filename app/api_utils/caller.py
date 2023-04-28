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




def fetch_data(symbol: str) -> dict:
    """
    Fetches data for a given stock symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        dict: A dictionary containing the stock symbol and chart data.
    """
    function="TIME_SERIES_INTRADAY"
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=5min&apikey={API_KEY}'.format(function,symbol,API_KEY)
    response = requests.get(url)
    json_data = response.json()
    print(json_data)
    time_series = json_data["Time Series (5min)"]
    chart_data = []
    for date, data in time_series.items():
        chart_data.append({
            "date": date,
            "open": float(data["1. open"]),
            "high": float(data["2. high"]),
            "low": float(data["3. low"]),
            "close": float(data["4. close"]),
            "volume": int(data["5. volume"]),
        })
    return {
        "symbol": symbol,
        "chart_data": chart_data,
    }

def get_eq(data:str,degree:int)->str:
	"""
	Fetches result equation for degree for the specified data points

	Args:
        data (str):	data points
        degree (int): degree of fit

    Returns:
        str: A str of equation.

    """
	data_points = ", ".join(f"({item['date']}, {item['close']})" for item in data)
	query = f"polynomial fit of degree {degree} for {{ {data_points} }}"
	client = wolframalpha.Client(WOLFRAM_ALPHA_API_KEY)
	result = client.query(query)
	equation = next(result.results).text

	return equation
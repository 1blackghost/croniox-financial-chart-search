'''
This script is used to call wolframalpha and aplhavantage apis

'''

#imports
import config
import requests
import datetime
from polygon import RESTClient
from datetime import date
import numpy as np




API_KEY = config.ALPHA_VANTAGE_KEY
BASE_URL = "https://www.alphavantage.co/query"

api_key=config.POLYGON_IO

import requests
from datetime import date

from datetime import date, timedelta

from datetime import date, timedelta
def fetch_data(ticker: str):
    """
    Fetches data points for the previous day using the Polygon API.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: A dictionary containing the data points.
    """
    today = date.today()
    previous_day = today - timedelta(days=1)
    date_str = previous_day.strftime("%Y-%m-%d")

    url = f"https://api.polygon.io/v2/aggs/ticker/{str(ticker)}/range/1/day/{date_str}/{date_str}?adjusted=true&sort=asc&limit=120&apiKey={api_key}"
    response = requests.get(url)
    json_data = response.json()
    print(json_data)  # Print the JSON response for debugging

    if json_data.get("status") == "OK":
        result_data = json_data.get("results")

        if result_data:
            symbol = json_data["ticker"]
            bar_data = [
                {
                    "v": bar["v"],
                    "vw": bar["vw"],
                    "o": bar["o"],
                    "c": bar["c"],
                    "h": bar["h"],
                    "l": bar["l"],
                    "t": bar["t"],
                    "n": bar["n"]
                }
                for bar in result_data
            ]

            data = {
                "symbol": symbol,
                "date": date_str,
                "bar_data": bar_data
            }
            j = {
                "status": "ok",
                "symbol": symbol,
                "chart_data": data,
            }
            return j

    return {"status": "bad","message":"Invalid!"}

def get_eq(data: dict, degree: int) -> dict:
    """
    Fetches the result equation for the specified degree polynomial fit using the provided data.

    Args:
        data (dict): A dictionary containing the chart data with 'bar_data', 'date', and 'symbol' keys.
        degree (int): Degree of fit.

    Returns:
        dict: A dictionary containing the status and the equation message.
    """
    try:
        bar_data = data['bar_data']
        dates = [bar['t'] for bar in bar_data]
        prices = [bar['c'] for bar in bar_data]

        if len(dates) < degree + 1:
            return {"status": "bad", "message": "Insufficient data points for the specified degree."}

        coefficients = np.polyfit(dates, prices, degree)
        equation = np.poly1d(coefficients)

        return {"status": "ok", "message": str(equation)}
    except Exception as e:
        return {"status": "bad", "message": f"Error fitting curve: {str(e)}"}




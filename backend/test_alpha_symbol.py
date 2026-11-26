import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

url = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "WIPRO.BSE",
    "outputsize": "compact",
    "apikey": API_KEY
}

response = requests.get(url, params=params, timeout=30)
result = response.json()

print("\nAlpha Vantage API response:")

if "Error Message" in result:
    print("API ERROR:", result["Error Message"])

elif "Note" in result:
    print("API LIMIT:", result["Note"])

elif "Information" in result:
    print("API INFORMATION:", result["Information"])

else:
    time_series = result.get("Time Series (Daily)")

    if time_series:
        print("SUCCESS: Historical data received!")
        print("Total records:", len(time_series))
        print("Latest record:", next(iter(time_series.items())))
    else:
        print("Unexpected response:")
        print(result)

import yfinance as yf
import pandas as pd


def get_historical_stock_data(ticker: str, period: str):

    stock = yf.Ticker(ticker)

    data = stock.history(
        period=period,
        interval="1d",
        auto_adjust=False
    )

    if data.empty:
        return None

    data = data.reset_index()

    data = data[
        ["Date", "Open", "High", "Low", "Close", "Volume"]
    ]

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    numeric_columns = ["Open", "High", "Low", "Close", "Volume"]

    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(subset=["Date"] + numeric_columns)

    data = data[
        (data["Open"] > 0) &
        (data["High"] > 0) &
        (data["Low"] > 0) &
        (data["Close"] > 0) &
        (data["Volume"] >= 0) &
        (data["High"] >= data["Low"]) &
        (data["High"] >= data["Open"]) &
        (data["High"] >= data["Close"]) &
        (data["Low"] <= data["Open"]) &
        (data["Low"] <= data["Close"])
    ].copy()

    data = data.sort_values(by="Date")
    data = data.drop_duplicates(subset=["Date"], keep="last")
    data = data.reset_index(drop=True)

    data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

    if data.empty:
        return None

    return data

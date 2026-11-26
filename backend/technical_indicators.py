import pandas as pd
import numpy as np
from pydantic import BaseModel
 
 
 
# Structured output for Technical Analysis
class TechnicalAnalysisOutput(BaseModel):
    ticker: str
 
    # Indicator values
    sma_20: float | None
    sma_50: float | None
    ema_12: float | None
    ema_26: float | None
    rsi_value: float | None
    macd_value: float | None
    signal_line: float | None
    macd_histogram: float | None
    historical_volatility: float | None
 
    # Indicator interpretations
    price_trend: str
    ema_trend: str
    ema_crossover: str
    rsi_status: str
    rsi_explanation: str
    macd_crossover: str
    macd_status: str
    macd_explanation: str
    volatility_status: str
    volatility_explanation: str
 
 
# Validate historical stock data
def validate_historical_data(df):
 
    df = df.copy()
 
    required_columns = [
        "Date", "Open", "High", "Low", "Close", "Volume"
    ]
 
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")
 
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
 
    df = df.dropna(subset=["Date"])
    df = df.sort_values(by="Date")
    df = df.drop_duplicates(subset=["Date"], keep="last")
 
    numeric_columns = [
        "Open", "High", "Low", "Close", "Volume"
    ]
 
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
 
    df = df.dropna(subset=numeric_columns)
 
    # Validate stock prices and volume
    df = df[
        (df["Open"] > 0) &
        (df["High"] > 0) &
        (df["Low"] > 0) &
        (df["Close"] > 0) &
        (df["Volume"] >= 0) &
        (df["High"] >= df["Low"]) &
        (df["High"] >= df["Open"]) &
        (df["High"] >= df["Close"]) &
        (df["Low"] <= df["Open"]) &
        (df["Low"] <= df["Close"])
    ].copy()
 
    if df.empty:
        raise ValueError("No valid historical stock data available.")
 
    return df.reset_index(drop=True)
 
 
# Calculate Technical Indicators
def calculate_technical_indicators(df):
 
    df = validate_historical_data(df)
 
    if len(df) < 50:
        raise ValueError(
            "At least 50 valid historical records are required for technical analysis."
        )
    # Calculate SMA
    df["SMA_5"] = df["Close"].rolling(window=5).mean()
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
 
    # Calculate EMA
    df["EMA_5"] = df["Close"].ewm(
        span=5,
        adjust=False
    ).mean()
 
    df["EMA_12"] = df["Close"].ewm(
        span=12,
        adjust=False
    ).mean()
 
    df["EMA_26"] = df["Close"].ewm(
        span=26,
        adjust=False
    ).mean()
 
    # Calculate MACD
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
 
    df["Signal_Line"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()
 
    df["MACD_Histogram"] = df["MACD"] - df["Signal_Line"]
 
    # Calculate RSI using Wilder's smoothing method
    delta = df["Close"].diff()
 
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
 
    avg_gain = gain.ewm(
        alpha=1/14,
        min_periods=14,
        adjust=False
    ).mean()
 
    avg_loss = loss.ewm(
        alpha=1/14,
        min_periods=14,
        adjust=False
    ).mean()
 
    rs = avg_gain / avg_loss
 
    df["RSI_14"] = 100 - (100 / (1 + rs))
 
    # Calculate Historical Volatility
    df["Daily_Return"] = df["Close"].pct_change()
 
    df["Historical_Volatility"] = (
        df["Daily_Return"]
        .rolling(window=20)
        .std()
        * np.sqrt(252)
        * 100
    )
 
    return df
 
 
# Interpret Technical Indicators
def interpret_technical_indicators(df, ticker):
 
    if df is None or df.empty:
        raise ValueError(
            "Cannot interpret technical indicators: no valid historical data available."
        )
 
    latest = df.iloc[-1]
 
    # Analyse Price Trend using SMA-20
    if pd.isna(latest["SMA_20"]):
        price_trend = "Insufficient data"
 
    elif latest["Close"] > latest["SMA_20"]:
        price_trend = "Uptrend"
 
    elif latest["Close"] < latest["SMA_20"]:
        price_trend = "Downtrend"
 
    else:
        price_trend = "Neutral"
 
    # Analyse EMA Trend
    if pd.isna(latest["EMA_12"]) or pd.isna(latest["EMA_26"]):
        ema_trend = "Insufficient data"
 
    elif latest["EMA_12"] > latest["EMA_26"]:
        ema_trend = "Upward Momentum"
 
    elif latest["EMA_12"] < latest["EMA_26"]:
        ema_trend = "Downward Momentum"
 
    else:
        ema_trend = "Neutral Momentum"
 
            # Detect EMA Crossover
    if len(df) < 2:
        ema_crossover = "Insufficient data"
 
    else:
        previous = df.iloc[-2]
        current = df.iloc[-1]
 
        if (
            pd.isna(previous["EMA_12"])
            or pd.isna(previous["EMA_26"])
            or pd.isna(current["EMA_12"])
            or pd.isna(current["EMA_26"])
        ):
            ema_crossover = "Insufficient data"
 
        elif (
            previous["EMA_12"] <= previous["EMA_26"]
            and current["EMA_12"] > current["EMA_26"]
        ):
            ema_crossover = "Bullish Crossover"
 
        elif (
            previous["EMA_12"] >= previous["EMA_26"]
            and current["EMA_12"] < current["EMA_26"]
        ):
            ema_crossover = "Bearish Crossover"
 
        else:
            ema_crossover = "No Crossover"
 
    # Analyse RSI
    rsi = latest["RSI_14"]
 
    if pd.isna(rsi):
        rsi_status = "Insufficient data"
        rsi_explanation = "Not enough historical data to calculate RSI."
 
    elif rsi > 70:
        rsi_status = "Potentially Overbought"
        rsi_explanation = "RSI is above 70, indicating potentially overbought conditions."
 
    elif rsi < 30:
        rsi_status = "Potentially Oversold"
        rsi_explanation = "RSI is below 30, indicating potentially oversold conditions."
 
    else:
        rsi_status = "Neutral"
        rsi_explanation = "RSI is between 30 and 70, indicating neither overbought nor oversold conditions."
 
    # Analyse MACD
    if pd.isna(latest["MACD"]) or pd.isna(latest["Signal_Line"]):
        macd_status = "Insufficient data"
        macd_explanation = "Not enough historical data to interpret MACD."
 
    elif latest["MACD"] > latest["Signal_Line"]:
        macd_status = "Positive Momentum"
        macd_explanation = "MACD is above the Signal Line, indicating positive momentum."
 
    elif latest["MACD"] < latest["Signal_Line"]:
        macd_status = "Negative Momentum"
        macd_explanation = "MACD is below the Signal Line, indicating negative momentum."
 
    else:
        macd_status = "Neutral Momentum"
        macd_explanation = "MACD and Signal Line are equal, indicating neutral momentum."
 
 
# Detect MACD Crossover
    if len(df) < 2:
        macd_crossover = "Insufficient data"
 
    else:
        previous = df.iloc[-2]
        current = df.iloc[-1]
 
        if (
            pd.isna(previous["MACD"])
            or pd.isna(previous["Signal_Line"])
            or pd.isna(current["MACD"])
            or pd.isna(current["Signal_Line"])
        ):
            macd_crossover = "Insufficient data"
 
        elif (
            previous["MACD"] <= previous["Signal_Line"]
            and current["MACD"] > current["Signal_Line"]
        ):
            macd_crossover = "Bullish Crossover"
 
        elif (
            previous["MACD"] >= previous["Signal_Line"]
            and current["MACD"] < current["Signal_Line"]
        ):
            macd_crossover = "Bearish Crossover"
 
        else:
            macd_crossover = "No Crossover"
 
    # Analyse Historical Volatility
    volatility = latest["Historical_Volatility"]
 
    if pd.isna(volatility):
        volatility_status = "Insufficient data"
        volatility_explanation = (
            "Not enough historical data to calculate volatility."
        )
 
    elif volatility > 40:
        volatility_status = "High Volatility"
        volatility_explanation = (
            "20-day annualized historical volatility is above 40%, "
            "indicating larger price fluctuations."
        )
 
    elif volatility < 20:
        volatility_status = "Low Volatility"
        volatility_explanation = (
            "20-day annualized historical volatility is below 20%, "
            "indicating relatively smaller price fluctuations."
        )
 
    else:
        volatility_status = "Moderate Volatility"
        volatility_explanation = (
    "20-day annualized historical volatility is between 20% and 40%, "
    "indicating moderate price fluctuations."
)
 
    # Return structured analysis
    return TechnicalAnalysisOutput(
        ticker=ticker,
 
        # Indicator values
        sma_20=float(latest["SMA_20"]) if pd.notna(latest["SMA_20"]) else None,
        sma_50=float(latest["SMA_50"]) if pd.notna(latest["SMA_50"]) else None,
        ema_12=float(latest["EMA_12"]) if pd.notna(latest["EMA_12"]) else None,
        ema_26=float(latest["EMA_26"]) if pd.notna(latest["EMA_26"]) else None,
        rsi_value=float(latest["RSI_14"]) if pd.notna(latest["RSI_14"]) else None,
        macd_value=float(latest["MACD"]) if pd.notna(latest["MACD"]) else None,
        signal_line=float(latest["Signal_Line"]) if pd.notna(latest["Signal_Line"]) else None,
        macd_histogram=float(latest["MACD_Histogram"]) if pd.notna(latest["MACD_Histogram"]) else None,
        historical_volatility=float(latest["Historical_Volatility"]) if pd.notna(latest["Historical_Volatility"]) else None,
 
        # Indicator interpretations
        price_trend=price_trend,
        ema_trend=ema_trend,
        ema_crossover=ema_crossover,
        rsi_status=rsi_status,
        rsi_explanation=rsi_explanation,
        macd_status=macd_status,
        macd_explanation=macd_explanation,
        macd_crossover=macd_crossover,
        volatility_status=volatility_status,
        volatility_explanation=volatility_explanation
    )
 

 
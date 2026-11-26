
import pandas as pd
import numpy as np


# ---------------------------------
# 1. Validate Historical Price Data
# ---------------------------------

def validate_price_data(data):

    if data is None or data.empty:
        raise ValueError("Historical stock data is empty.")

    if "Close" not in data.columns:
        raise ValueError("Close price column is missing.")

    prices = pd.to_numeric(
        data["Close"],
        errors="coerce"
    )

    prices = prices.replace(
        [np.inf, -np.inf],
        np.nan
    ).dropna()

    prices = prices[prices > 0]

    if len(prices) < 2:
        raise ValueError(
            "At least two valid closing prices are required."
        )

    return prices.reset_index(drop=True)


# ---------------------------------
# 2. Calculate Daily Returns
# ---------------------------------

def calculate_daily_returns(data):

    prices = validate_price_data(data)

    daily_returns = prices.pct_change().dropna()

    return daily_returns


# ---------------------------------
# 3. Historical Volatility
# ---------------------------------

def calculate_historical_volatility(
    data,
    trading_days=252
):

    daily_returns = calculate_daily_returns(data)

    if len(daily_returns) < 2:
        return None

    daily_volatility = daily_returns.std(ddof=1)

    annualized_volatility = (
        daily_volatility * np.sqrt(trading_days)
    ) * 100

    return round(float(annualized_volatility), 2)


# ---------------------------------
# 4. Maximum Drawdown
# ---------------------------------

def calculate_maximum_drawdown(data):

    if data is None or data.empty:
        raise ValueError("Historical stock data is empty.")

    if "Close" not in data.columns:
        raise ValueError("Close price column is missing.")

    # Keep prices and dates together while cleaning
    valid_data = data.copy()

    valid_data["Close"] = pd.to_numeric(
        valid_data["Close"],
        errors="coerce"
    )

    valid_data["Close"] = valid_data["Close"].replace(
        [np.inf, -np.inf],
        np.nan
    )

    valid_data = valid_data.dropna(
        subset=["Close"]
    )

    valid_data = valid_data[
        valid_data["Close"] > 0
    ].reset_index(drop=True)

    if len(valid_data) < 2:
        raise ValueError(
            "At least two valid closing prices are required."
        )

    prices = valid_data["Close"]

    # Extract matching dates
    if "Date" in valid_data.columns:
        dates = valid_data["Date"].astype(str)
    else:
        dates = pd.Series(
            [str(index) for index in range(len(prices))]
        )

    # Calculate running peak
    running_peak = prices.cummax()

    # Calculate drawdown
    drawdowns = (
        (prices - running_peak) / running_peak
    )

    # Find maximum drawdown point
    trough_index = drawdowns.idxmin()

    # Find peak before the trough
    peak_index = prices.loc[:trough_index].idxmax()

    maximum_drawdown = (
        abs(float(drawdowns.loc[trough_index])) * 100
    )

    return {
        "maximum_drawdown": round(
            maximum_drawdown, 2
        ),

        "peak_price": round(
            float(prices.loc[peak_index]), 2
        ),

        "trough_price": round(
            float(prices.loc[trough_index]), 2
        ),

        "peak_date": dates.loc[peak_index],

        "trough_date": dates.loc[trough_index]
    }


# ---------------------------------
# 5. Classify Volatility Risk
# ---------------------------------

def classify_volatility(volatility):

    if volatility is None:
        return "Unavailable"

    if volatility < 15:
        return "Low"

    elif volatility < 30:
        return "Moderate"

    elif volatility < 50:
        return "High"

    else:
        return "Very High"


# ---------------------------------
# 6. Classify Drawdown Risk
# ---------------------------------

def classify_drawdown(drawdown):

    if drawdown is None:
        return "Unavailable"

    if drawdown < 5:
        return "Low"

    elif drawdown < 10:
        return "Moderate"

    elif drawdown < 20:
        return "High"

    else:
        return "Very High"


# ---------------------------------
# 7. Combined Price Risk Analysis
# ---------------------------------

def calculate_price_risk(data):

    volatility = calculate_historical_volatility(data)

    drawdown = calculate_maximum_drawdown(data)

    volatility_result = {
        "value": volatility,
        "unit": "Percentage",
        "risk_level": classify_volatility(volatility),
        "method": (
            "Standard deviation of daily closing-price returns "
            "multiplied by the square root of 252 trading days."
        )
    }

    drawdown_result = {
        **drawdown,
        "risk_level": classify_drawdown(
            drawdown["maximum_drawdown"]
        )
    }

    return {
        "historical_volatility": volatility_result,
        "maximum_drawdown": drawdown_result
    }

# import pandas as pd
# import numpy as np


# # ---------------------------------
# # 1. Validate Historical Price Data
# # ---------------------------------

# def validate_price_data(data):

#     if data is None or data.empty:
#         raise ValueError("Historical stock data is empty.")

#     if "Close" not in data.columns:
#         raise ValueError("Close price column is missing.")

#     prices = pd.to_numeric(
#         data["Close"],
#         errors="coerce"
#     )

#     prices = prices.replace(
#         [np.inf, -np.inf],
#         np.nan
#     ).dropna()

#     prices = prices[prices > 0]

#     if len(prices) < 2:
#         raise ValueError(
#             "At least two valid closing prices are required."
#         )

#     return prices.reset_index(drop=True)


# # ---------------------------------
# # 2. Calculate Daily Returns
# # ---------------------------------

# def calculate_daily_returns(data):

#     prices = validate_price_data(data)

#     daily_returns = prices.pct_change().dropna()

#     return daily_returns


# # ---------------------------------
# # 3. Historical Volatility
# # ---------------------------------

# def calculate_historical_volatility(
#     data,
#     trading_days=252
# ):

#     daily_returns = calculate_daily_returns(data)

#     if len(daily_returns) < 2:
#         return None

#     daily_volatility = daily_returns.std(ddof=1)

#     annualized_volatility = (
#         daily_volatility * np.sqrt(trading_days)
#     ) * 100

#     return round(float(annualized_volatility), 2)


# # ---------------------------------
# # 4. Maximum Drawdown
# # ---------------------------------

# def calculate_maximum_drawdown(data):

#     prices = validate_price_data(data)

#     if "Date" in data.columns:
#         dates = (
#             data.loc[prices.index, "Date"]
#             .astype(str)
#             .reset_index(drop=True)
#         )
#     else:
#         dates = pd.Series(
#             [str(index) for index in range(len(prices))]
#         )

#     running_peak = prices.cummax()

#     drawdowns = (
#         (prices - running_peak) / running_peak
#     )

#     trough_index = drawdowns.idxmin()

#     peak_index = prices.loc[:trough_index].idxmax()

#     maximum_drawdown = (
#         abs(float(drawdowns.loc[trough_index])) * 100
#     )

#     return {
#         "maximum_drawdown": round(
#             maximum_drawdown, 2
#         ),

#         "peak_price": round(
#             float(prices.loc[peak_index]), 2
#         ),

#         "trough_price": round(
#             float(prices.loc[trough_index]), 2
#         ),

#         "peak_date": dates.loc[peak_index],

#         "trough_date": dates.loc[trough_index]
#     }


# # ---------------------------------
# # 5. Classify Volatility Risk
# # ---------------------------------

# def classify_volatility(volatility):

#     if volatility is None:
#         return "Unavailable"

#     if volatility < 15:
#         return "Low"

#     elif volatility < 30:
#         return "Moderate"

#     elif volatility < 50:
#         return "High"

#     else:
#         return "Very High"


# # ---------------------------------
# # 6. Classify Drawdown Risk
# # ---------------------------------

# def classify_drawdown(drawdown):

#     if drawdown is None:
#         return "Unavailable"

#     if drawdown < 5:
#         return "Low"

#     elif drawdown < 10:
#         return "Moderate"

#     elif drawdown < 20:
#         return "High"

#     else:
#         return "Very High"


# # ---------------------------------
# # 7. Combined Price Risk Analysis
# # ---------------------------------

# def calculate_price_risk(data):

#     volatility = calculate_historical_volatility(data)

#     drawdown = calculate_maximum_drawdown(data)

#     volatility_result = {
#         "value": volatility,
#         "unit": "Percentage",
#         "risk_level": classify_volatility(volatility),
#         "method": (
#             "Standard deviation of daily closing-price returns "
#             "multiplied by the square root of 252 trading days."
#         )
#     }

#     drawdown_result = {
#         **drawdown,
#         "risk_level": classify_drawdown(
#             drawdown["maximum_drawdown"]
#         )
#     }

#     return {
#         "historical_volatility": volatility_result,
#         "maximum_drawdown": drawdown_result
#     }

# import pandas as pd
# import numpy as np


# # ---------------------------------
# # 1. Validate Historical Price Data
# # ---------------------------------

# def validate_price_data(data):

#     if data is None or data.empty:
#         raise ValueError("Historical stock data is empty.")

#     if "Close" not in data.columns:
#         raise ValueError("Close price column is missing.")

#     prices = pd.to_numeric(
#         data["Close"],
#         errors="coerce"
#     )

#     prices = prices.replace(
#         [np.inf, -np.inf],
#         np.nan
#     ).dropna()

#     prices = prices[prices > 0]

#     if len(prices) < 2:
#         raise ValueError(
#             "At least two valid closing prices are required."
#         )

#     return prices.reset_index(drop=True)


# # ---------------------------------
# # 2. Calculate Daily Returns
# # ---------------------------------

# def calculate_daily_returns(data):

#     prices = validate_price_data(data)

#     daily_returns = prices.pct_change().dropna()

#     return daily_returns


# # ---------------------------------
# # 3. Historical Volatility
# # ---------------------------------

# def calculate_historical_volatility(
#     data,
#     trading_days=252
# ):

#     daily_returns = calculate_daily_returns(data)

#     if len(daily_returns) < 2:
#         return None

#     daily_volatility = daily_returns.std(ddof=1)

#     annualized_volatility = (
#         daily_volatility * np.sqrt(trading_days)
#     ) * 100

#     return round(float(annualized_volatility), 2)


# # ---------------------------------
# # 4. Maximum Drawdown
# # ---------------------------------

# def calculate_maximum_drawdown(data):

#     if data is None or data.empty:
#         raise ValueError("Historical stock data is empty.")

#     if "Close" not in data.columns:
#         raise ValueError("Close price column is missing.")

#     # Keep prices and dates aligned
#     valid_data = data.copy()

#     valid_data["Close"] = pd.to_numeric(
#         valid_data["Close"],
#         errors="coerce"
#     )

#     valid_data["Close"] = valid_data["Close"].replace(
#         [np.inf, -np.inf],
#         np.nan
#     )

#     valid_data = valid_data.dropna(
#         subset=["Close"]
#     )

#     valid_data = valid_data[
#         valid_data["Close"] > 0
#     ].reset_index(drop=True)

#     if len(valid_data) < 2:
#         raise ValueError(
#             "At least two valid closing prices are required."
#         )

#     prices = valid_data["Close"]

#     if "Date" in valid_data.columns:
#         dates = (
#             valid_data["Date"]
#             .astype(str)
#             .reset_index(drop=True)
#         )
#     else:
#         dates = pd.Series(
#             [str(index) for index in range(len(prices))]
#         )

#     # Calculate running peak
#     running_peak = prices.cummax()

#     # Calculate drawdown
#     drawdowns = (
#         (prices - running_peak) / running_peak
#     )

#     # Find maximum drawdown point
#     trough_index = drawdowns.idxmin()

#     # Find peak before the trough
#     peak_index = prices.loc[:trough_index].idxmax()

#     maximum_drawdown = (
#         abs(float(drawdowns.loc[trough_index])) * 100
#     )

#     return {
#         "maximum_drawdown": round(
#             maximum_drawdown, 2
#         ),

#         "peak_price": round(
#             float(prices.loc[peak_index]), 2
#         ),

#         "trough_price": round(
#             float(prices.loc[trough_index]), 2
#         ),

#         "peak_date": dates.loc[peak_index],

#         "trough_date": dates.loc[trough_index]
#     }


# # ---------------------------------
# # 5. Classify Volatility Risk
# # ---------------------------------

# def classify_volatility(volatility):

#     if volatility is None:
#         return "Unavailable"

#     if volatility < 15:
#         return "Low"

#     elif volatility < 30:
#         return "Moderate"

#     elif volatility < 50:
#         return "High"

#     else:
#         return "Very High"


# # ---------------------------------
# # 6. Classify Drawdown Risk
# # ---------------------------------

# def classify_drawdown(drawdown):

#     if drawdown is None:
#         return "Unavailable"

#     if drawdown < 5:
#         return "Low"

#     elif drawdown < 10:
#         return "Moderate"

#     elif drawdown < 20:
#         return "High"

#     else:
#         return "Very High"


# # ---------------------------------
# # 7. Combined Price Risk Analysis
# # ---------------------------------

# def calculate_price_risk(data):

#     volatility = calculate_historical_volatility(data)

#     drawdown = calculate_maximum_drawdown(data)

#     volatility_result = {
#         "value": volatility,
#         "unit": "Percentage",
#         "risk_level": classify_volatility(volatility),
#         "method": (
#             "Standard deviation of daily closing-price returns "
#             "multiplied by the square root of 252 trading days."
#         )
#     }

#     drawdown_result = {
#         **drawdown,
#         "risk_level": classify_drawdown(
#             drawdown["maximum_drawdown"]
#         )
#     }

#     return {
#         "historical_volatility": volatility_result,
#         "maximum_drawdown": drawdown_result
#     }

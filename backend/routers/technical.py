
from fastapi import APIRouter, HTTPException, Query
from typing import Literal
import math
from technical_stock_data import get_historical_stock_data
from technical_indicators import (
    calculate_technical_indicators,
    interpret_technical_indicators
)

router = APIRouter(tags=["Technical Analysis"])


@router.get("/technical-analysis/{ticker}")
def analyze_technical(
    ticker: str,
    period: Literal["1mo", "3mo", "6mo", "1y", "2y", "5y"] = Query("1y")
):

    try:
        # Step 1: Fetch historical stock data
        historical_data = get_historical_stock_data(ticker, period)

        if historical_data is None or historical_data.empty:
            raise HTTPException(
                status_code=404,
                detail="No historical stock data available."
            )

        # Step 2: Calculate technical indicators
        calculated_data = calculate_technical_indicators(
            historical_data
        )

        # Step 3: Interpret technical indicators
        analysis = interpret_technical_indicators(
            calculated_data,
            ticker
        )

        # Step 4: Return the analysis
        return {
             "success": True,
    "ticker": ticker,
    "period": period,
    "total_records": len(calculated_data),
    "technical_analysis": analysis.model_dump(),
    "historical_data": (
        calculated_data.astype(object)
        .where(calculated_data.notna(), None)
        .to_dict(orient="records")
            )
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

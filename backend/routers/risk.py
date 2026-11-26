
from fastapi import APIRouter, HTTPException

from schemas.risk_schema import (
    RiskAnalysisRequest,
    RiskAnalysisResponse
)

from services.risk_agent.analysis import analyze_stock_risk
from services.risk_agent.explainer import explain_risk_report

from stock_data import get_historical_stock_data
from company_financials import get_company_financial_information


router = APIRouter(
    prefix="/risk",
    tags=["Risk Analysis Agent"]
)


@router.post("/analyze")
def generate_risk_report(request: RiskAnalysisRequest):

    try:
        # Step 1: Normalize stock symbol
        symbol = request.symbol.strip().upper()

        # Step 2: Fetch historical stock data
        historical_result = get_historical_stock_data(
            symbol,
            request.period
        )

        if not historical_result or historical_result.get("data") is None:
            raise HTTPException(
                status_code=404,
                detail="Historical stock data is unavailable."
            )

        historical_data = historical_result["data"]

        if historical_data.empty:
            raise HTTPException(
                status_code=404,
                detail="No historical stock records were found."
            )

        # Step 3: Fetch company financial information
        company_profile = None
        financial_information = None

        try:
            financial_result = get_company_financial_information(
                symbol
            )

            if financial_result and financial_result.get("success"):

                financial_information = financial_result

                profile_result = financial_result.get(
                    "company_profile", {}
                )

                if profile_result.get("success"):
                    company_profile = profile_result.get("data")

        except Exception as financial_error:
            print(
                f"Financial data unavailable for {symbol}: "
                f"{financial_error}"
            )

        # Step 4: Perform deterministic Python risk analysis
        risk_report = analyze_stock_risk(
            symbol=symbol,
            period=request.period,
            historical_data=historical_data,
            company_profile=company_profile,
            financial_information=financial_information
        )

        # Step 5: Get Gemini's structured interpretation
        interpretation = explain_risk_report(risk_report)

        # Step 6: Merge Python and Gemini results
        risk_report.update(interpretation)

        # Step 7: Validate the complete final report
        validated_report = RiskAnalysisResponse.model_validate(
            risk_report
        )

        # Step 8: Return final response
        return {
            "success": True,
            "risk_report": validated_report.model_dump()
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"Risk Analysis Error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Risk analysis failed. Check backend logs for details."
        )

# from fastapi import APIRouter, HTTPException

# from schemas.risk_schema import (
#     RiskAnalysisRequest,
#     RiskAnalysisResponse
# )

# from services.risk_agent.analysis import analyze_stock_risk
# from services.risk_agent.explainer import explain_risk_report

# from technical_stock_data import get_historical_stock_data
# # from company_financials import get_company_financial_information
# from yahoo_company_financials import get_company_financial_information

# router = APIRouter(
#     prefix="/risk",
#     tags=["Risk Analysis Agent"]
# )


# @router.post("/analyze")
# def generate_risk_report(request: RiskAnalysisRequest):

#     try:
#         # Step 1: Normalize stock symbol
#         symbol = request.symbol.strip().upper()

#         # Step 2: Fetch historical stock data using Yahoo Finance
#         historical_data = get_historical_stock_data(
#             symbol,
#             request.period
#         )

#         if historical_data is None or historical_data.empty:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Historical stock data is unavailable."
#             )

#         # Step 3: Fetch company financial information
#         company_profile = None
#         financial_information = None

#         try:
#             financial_result = get_company_financial_information(
#                 symbol
#             )

#             if financial_result and financial_result.get("success"):

#                 financial_information = financial_result

#                 profile_result = financial_result.get(
#                     "company_profile", {}
#                 )

#                 if profile_result.get("success"):
#                     company_profile = profile_result.get("data")

#         except Exception as financial_error:
#             print(
#                 f"Financial data unavailable for {symbol}: "
#                 f"{financial_error}"
#             )

#         # Step 4: Perform deterministic Python risk analysis
#         risk_report = analyze_stock_risk(
#             symbol=symbol,
#             period=request.period,
#             historical_data=historical_data,
#             company_profile=company_profile,
#             financial_information=financial_information
#         )

#         # Step 5: Get Gemini's structured interpretation
#         interpretation = explain_risk_report(risk_report)

#         # Step 6: Merge Python and Gemini results
#         risk_report.update(interpretation)

#         # Step 7: Validate the complete final report
#         validated_report = RiskAnalysisResponse.model_validate(
#             risk_report
#         )

#         # Step 8: Return final response
#         return {
#             "success": True,
#             "risk_report": validated_report.model_dump()
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         print(f"Risk Analysis Error: {e}")

#         raise HTTPException(
#             status_code=500,
#             detail="Risk analysis failed. Check backend logs for details."
#         )

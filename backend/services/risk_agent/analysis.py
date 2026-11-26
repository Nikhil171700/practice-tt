
# from services.risk_agent.calculations import calculate_price_risk

# from schemas.risk_schema import (
#     HistoricalVolatility,
#     MaximumDrawdown,
#     FinancialRisk,
#     RiskAnalysisResponse
# )


# # -----------------------------------------
# # 1. Extract Financial Statement Metrics
# # -----------------------------------------

# def get_statement_metrics(financial_information, statement_name):

#     statements = financial_information.get(
#         "financial_statements", {}
#     )

#     statement = statements.get(statement_name, {})

#     if not statement.get("success"):
#         return {}

#     metrics = {}

#     for item in statement.get("data", []):

#         metric_name = item.get("metric", "").lower()

#         values = item.get("values", {})

#         metrics[metric_name] = values

#     return metrics


# # -----------------------------------------
# # 2. Extract Annual Financial Values
# # -----------------------------------------

# def get_annual_values(metrics, metric_name):

#     values = metrics.get(
#         metric_name.lower(), {}
#     )

#     annual_values = []

#     for period, value in values.items():

#         if "(Annual)" not in period:
#             continue

#         try:
#             number = float(value)

#             if number != number:
#                 continue

#             date = period.replace(
#                 " (Annual)", ""
#             )

#             annual_values.append(
#                 (date, number)
#             )

#         except (ValueError, TypeError):
#             continue

#     annual_values.sort(
#         key=lambda item: item[0],
#         reverse=True
#     )

#     return annual_values


# # -----------------------------------------
# # 3. Analyze Financial Risks
# # -----------------------------------------

# def analyze_financial_risks(financial_information):

#     risks = []

#     if not financial_information:
#         return risks

#     income = get_statement_metrics(
#         financial_information,
#         "income_statement"
#     )

#     balance = get_statement_metrics(
#         financial_information,
#         "balance_sheet"
#     )

#     cash_flow = get_statement_metrics(
#         financial_information,
#         "cash_flow_statement"
#     )

#     # ---------------------------------
#     # A. Liabilities to Assets Ratio
#     # ---------------------------------

#     liabilities = get_annual_values(
#         balance,
#         "totalLiabilities"
#     )

#     assets = get_annual_values(
#         balance,
#         "totalAssets"
#     )

#     if liabilities and assets:

#         latest_liabilities = liabilities[0][1]

#         latest_assets = assets[0][1]

#         if latest_assets > 0:

#             ratio = (
#                 latest_liabilities / latest_assets
#             )

#             if ratio > 0.70:

#                 risks.append(
#                     FinancialRisk(
#                         risk_name="High liabilities relative to assets",
#                         description=(
#                             "The company's total liabilities "
#                             "are high relative to its total assets."
#                         ),
#                         severity="High",
#                         evidence=(
#                             f"Liabilities-to-assets ratio: "
#                             f"{ratio:.2f}"
#                         )
#                     )
#                 )

#             elif ratio > 0.50:

#                 risks.append(
#                     FinancialRisk(
#                         risk_name="Elevated liabilities",
#                         description=(
#                             "The company's liabilities represent "
#                             "a significant portion of its assets."
#                         ),
#                         severity="Moderate",
#                         evidence=(
#                             f"Liabilities-to-assets ratio: "
#                             f"{ratio:.2f}"
#                         )
#                     )
#                 )

#     # ---------------------------------
#     # B. Current Ratio
#     # ---------------------------------

#     current_assets = get_annual_values(
#         balance,
#         "currentAssets"
#     )

#     current_liabilities = get_annual_values(
#         balance,
#         "currentLiabilities"
#     )

#     if current_assets and current_liabilities:

#         ca = current_assets[0][1]

#         cl = current_liabilities[0][1]

#         if cl > 0:

#             current_ratio = ca / cl

#             if current_ratio < 1:

#                 risks.append(
#                     FinancialRisk(
#                         risk_name="Weak current liquidity",
#                         description=(
#                             "Current liabilities exceed current "
#                             "assets, which may indicate short-term "
#                             "liquidity pressure."
#                         ),
#                         severity="High",
#                         evidence=(
#                             f"Current ratio: {current_ratio:.2f}"
#                         )
#                     )
#                 )

#             elif current_ratio < 1.5:

#                 risks.append(
#                     FinancialRisk(
#                         risk_name="Limited liquidity buffer",
#                         description=(
#                             "The company's current assets provide "
#                             "a relatively limited buffer against "
#                             "short-term obligations."
#                         ),
#                         severity="Moderate",
#                         evidence=(
#                             f"Current ratio: {current_ratio:.2f}"
#                         )
#                     )
#                 )

#     # ---------------------------------
#     # C. Net Income Analysis
#     # ---------------------------------

#     net_income = get_annual_values(
#         income,
#         "netIncome"
#     )

#     if net_income:

#         latest_profit = net_income[0][1]

#         if latest_profit < 0:

#             risks.append(
#                 FinancialRisk(
#                     risk_name="Negative net income",
#                     description=(
#                         "The latest available annual report "
#                         "shows a net loss."
#                     ),
#                     severity="High",
#                     evidence=(
#                         f"Net income for {net_income[0][0]}: "
#                         f"{latest_profit}"
#                     )
#                 )
#             )

#         elif len(net_income) >= 2:

#             previous_profit = net_income[1][1]

#             if previous_profit > 0:

#                 decline = (
#                     (previous_profit - latest_profit)
#                     / previous_profit
#                 ) * 100

#                 if decline > 25:

#                     risks.append(
#                         FinancialRisk(
#                             risk_name="Declining net income",
#                             description=(
#                                 "Net income declined significantly "
#                                 "compared with the previous annual report."
#                             ),
#                             severity=(
#                                 "High" if decline > 50
#                                 else "Moderate"
#                             ),
#                             evidence=(
#                                 f"Annual net income decline: "
#                                 f"{decline:.2f}%"
#                             )
#                         )
#                     )

#     # ---------------------------------
#     # D. Operating Cash Flow
#     # ---------------------------------

#     operating_cash_flow = get_annual_values(
#         cash_flow,
#         "operatingCashflow"
#     )

#     if operating_cash_flow:

#         latest_cash_flow = operating_cash_flow[0][1]

#         if latest_cash_flow < 0:

#             risks.append(
#                 FinancialRisk(
#                     risk_name="Negative operating cash flow",
#                     description=(
#                         "The latest annual report shows negative "
#                         "cash flow from operating activities."
#                     ),
#                     severity="High",
#                     evidence=(
#                         f"Operating cash flow for "
#                         f"{operating_cash_flow[0][0]}: "
#                         f"{latest_cash_flow}"
#                     )
#                 )
#             )

#     return risks


# # -----------------------------------------
# # 4. Determine Overall Risk
# # -----------------------------------------

# def determine_overall_risk(volatility, drawdown, financial_risks):

#     priority = {
#         "Low": 1,
#         "Moderate": 2,
#         "High": 3,
#         "Critical": 4,
#         "Very High": 4,
#         "Unavailable": 0
#     }

#     levels = [
#         volatility.risk_level,
#         drawdown.risk_level
#     ]

#     levels.extend(
#         risk.severity for risk in financial_risks
#     )

#     available_levels = [
#         level for level in levels
#         if priority.get(level, 0) > 0
#     ]

#     if not available_levels:
#         return "Unavailable"

#     highest = max(
#         available_levels,
#         key=lambda level: priority.get(level, 0)
#     )

#     if highest == "Very High":
#         return "Critical"

#     return highest


# # -----------------------------------------
# # 5. Main Risk Analysis Function
# # -----------------------------------------

# def analyze_stock_risk(
#     symbol,
#     period,
#     historical_data,
#     company_profile=None,
#     financial_information=None
# ):

#     # Calculate historical price risks
#     price_risk = calculate_price_risk(
#         historical_data
#     )

#     volatility = HistoricalVolatility(
#         **price_risk["historical_volatility"]
#     )

#     drawdown = MaximumDrawdown(
#         **price_risk["maximum_drawdown"]
#     )

#     # Extract company information
#     profile = company_profile or {}

#     company_name = profile.get("company_name")

#     sector = profile.get("sector")

#     # Analyze financial statements
#     financial_risks = analyze_financial_risks(
#         financial_information
#     )

#     # Identify missing information
#     missing_information = []

#     if not company_profile:

#         missing_information.append(
#             "Company profile is unavailable."
#         )

#     if not financial_information:

#         missing_information.append(
#             "Financial statements are unavailable."
#         )

#     if not financial_risks:

#         missing_information.append(
#             "No financial risk indicators were identified. "
#             "This does not prove that financial risks are absent."
#         )

#     missing_information.extend([
#         "Other agents' findings are not yet connected.",
#         "Sector-specific evidence is not yet independently verified."
#     ])

#     # Determine overall risk
#     overall_risk = determine_overall_risk(
#         volatility,
#         drawdown,
#         financial_risks
#     )

#     # Build preliminary report
#     report = RiskAnalysisResponse(

#         company_name=company_name,

#         symbol=symbol.upper(),

#         sector=sector,

#         period=period,

#         historical_volatility=volatility,

#         maximum_drawdown=drawdown,

#         financial_risks=financial_risks,

#         sector_risks=[],

#         conflicting_findings=[],

#         missing_information=missing_information,

#         alternative_scenarios=[],

#         uncertainties_and_limitations=[
#             "Historical volatility and drawdown describe past price movements.",
#             "Financial risk checks use available annual financial statements.",
#             "Some financial metrics may be missing or outdated.",
#             "Risk thresholds are preliminary screening rules, not universal standards.",
#             "Sector and other agent findings have not yet been integrated."
#         ],

#         overall_risk=overall_risk,

#         risk_summary=(
#             "Preliminary risk assessment based on historical "
#             "price data and available financial statements."
#         )
#     )

#     return report.model_dump()

import math

from services.risk_agent.calculations import calculate_price_risk

from schemas.risk_schema import (
    HistoricalVolatility,
    MaximumDrawdown,
    FinancialRisk,
    RiskAnalysisResponse
)


# -----------------------------------------
# 1. Extract Financial Statement Metrics
# -----------------------------------------

def get_statement_metrics(financial_information, statement_name):

    if not financial_information:
        return {}

    statements = financial_information.get(
        "financial_statements", {}
    )

    statement = statements.get(statement_name, {})

    if not statement or not statement.get("success"):
        return {}

    metrics = {}

    for item in statement.get("data", []):

        metric_name = item.get("metric", "").lower()

        values = item.get("values", {})

        if metric_name and isinstance(values, dict):
            metrics[metric_name] = values

    return metrics


# -----------------------------------------
# 2. Extract Annual Financial Values
# -----------------------------------------

def get_annual_values(metrics, metric_name):

    values = metrics.get(
        metric_name.lower(), {}
    )

    annual_values = []

    for period, value in values.items():

        if "(Annual)" not in period:
            continue

        try:
            number = float(value)

            if not math.isfinite(number):
                continue

            date = period.replace(
                " (Annual)", ""
            )

            annual_values.append(
                (date, number)
            )

        except (ValueError, TypeError):
            continue

    annual_values.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return annual_values


# -----------------------------------------
# 3. Get Latest Matching Financial Values
# -----------------------------------------

def get_latest_matching_values(
    first_values,
    second_values
):

    first_data = dict(first_values)
    second_data = dict(second_values)

    common_dates = sorted(
        set(first_data.keys()) & set(second_data.keys()),
        reverse=True
    )

    if not common_dates:
        return None

    latest_date = common_dates[0]

    return (
        latest_date,
        first_data[latest_date],
        second_data[latest_date]
    )


# -----------------------------------------
# 4. Check Financial Statement Availability
# -----------------------------------------

def get_unavailable_statements(financial_information):

    required_statements = [
        "income_statement",
        "balance_sheet",
        "cash_flow_statement"
    ]

    unavailable = []

    statements = (
        financial_information.get("financial_statements", {})
        if financial_information
        else {}
    )

    for statement_name in required_statements:

        statement = statements.get(
            statement_name, {}
        )

        if (
            not statement
            or not statement.get("success")
            or not statement.get("data")
        ):

            unavailable.append(statement_name)

    return unavailable


# -----------------------------------------
# 5. Analyze Financial Risks
# -----------------------------------------

def analyze_financial_risks(financial_information):

    risks = []

    if not financial_information:
        return risks

    income = get_statement_metrics(
        financial_information,
        "income_statement"
    )

    balance = get_statement_metrics(
        financial_information,
        "balance_sheet"
    )

    cash_flow = get_statement_metrics(
        financial_information,
        "cash_flow_statement"
    )

    # ---------------------------------
    # A. Liabilities to Assets Ratio
    # ---------------------------------

    liabilities = get_annual_values(
        balance,
        "totalLiabilities"
    )

    assets = get_annual_values(
        balance,
        "totalAssets"
    )

    matching_values = get_latest_matching_values(
        liabilities,
        assets
    )

    if matching_values:

        date, latest_liabilities, latest_assets = matching_values

        if latest_assets > 0:

            ratio = latest_liabilities / latest_assets

            if ratio > 0.70:

                risks.append(
                    FinancialRisk(
                        risk_name="High liabilities relative to assets",
                        description=(
                            "The company's total liabilities "
                            "are high relative to its total assets."
                        ),
                        severity="High",
                        evidence=(
                            f"Liabilities-to-assets ratio: "
                            f"{ratio:.2f} for {date}"
                        )
                    )
                )

            elif ratio > 0.50:

                risks.append(
                    FinancialRisk(
                        risk_name="Elevated liabilities",
                        description=(
                            "The company's liabilities represent "
                            "a significant portion of its assets."
                        ),
                        severity="Moderate",
                        evidence=(
                            f"Liabilities-to-assets ratio: "
                            f"{ratio:.2f} for {date}"
                        )
                    )
                )

    # ---------------------------------
    # B. Current Ratio
    # ---------------------------------

    current_assets = get_annual_values(
        balance,
        "currentAssets"
    )

    current_liabilities = get_annual_values(
        balance,
        "currentLiabilities"
    )

    matching_values = get_latest_matching_values(
        current_assets,
        current_liabilities
    )

    if matching_values:

        date, ca, cl = matching_values

        if cl > 0:

            current_ratio = ca / cl

            if current_ratio < 1:

                risks.append(
                    FinancialRisk(
                        risk_name="Weak current liquidity",
                        description=(
                            "Current liabilities exceed current "
                            "assets, which may indicate short-term "
                            "liquidity pressure."
                        ),
                        severity="High",
                        evidence=(
                            f"Current ratio: {current_ratio:.2f} "
                            f"for {date}"
                        )
                    )
                )

            elif current_ratio < 1.5:

                risks.append(
                    FinancialRisk(
                        risk_name="Limited liquidity buffer",
                        description=(
                            "The company's current assets provide "
                            "a relatively limited buffer against "
                            "short-term obligations."
                        ),
                        severity="Moderate",
                        evidence=(
                            f"Current ratio: {current_ratio:.2f} "
                            f"for {date}"
                        )
                    )
                )

    # ---------------------------------
    # C. Net Income Analysis
    # ---------------------------------

    net_income = get_annual_values(
        income,
        "netIncome"
    )

    if net_income:

        latest_date, latest_profit = net_income[0]

        if latest_profit < 0:

            risks.append(
                FinancialRisk(
                    risk_name="Negative net income",
                    description=(
                        "The latest available annual report "
                        "shows a net loss."
                    ),
                    severity="High",
                    evidence=(
                        f"Net income for {latest_date}: "
                        f"{latest_profit}"
                    )
                )
            )

        elif len(net_income) >= 2:

            previous_date, previous_profit = net_income[1]

            if previous_profit > 0:

                decline = (
                    (previous_profit - latest_profit)
                    / previous_profit
                ) * 100

                if decline > 25:

                    risks.append(
                        FinancialRisk(
                            risk_name="Declining net income",
                            description=(
                                "Net income declined significantly "
                                "compared with the previous annual report."
                            ),
                            severity=(
                                "High" if decline > 50
                                else "Moderate"
                            ),
                            evidence=(
                                f"Annual net income decline: "
                                f"{decline:.2f}% "
                                f"({previous_date} to {latest_date})"
                            )
                        )
                    )

    # ---------------------------------
    # D. Operating Cash Flow
    # ---------------------------------

    operating_cash_flow = get_annual_values(
        cash_flow,
        "operatingCashflow"
    )

    if operating_cash_flow:

        latest_date, latest_cash_flow = operating_cash_flow[0]

        if latest_cash_flow < 0:

            risks.append(
                FinancialRisk(
                    risk_name="Negative operating cash flow",
                    description=(
                        "The latest annual report shows negative "
                        "cash flow from operating activities."
                    ),
                    severity="High",
                    evidence=(
                        f"Operating cash flow for {latest_date}: "
                        f"{latest_cash_flow}"
                    )
                )
            )

    return risks


# -----------------------------------------
# 6. Determine Overall Risk
# -----------------------------------------

def determine_overall_risk(
    volatility,
    drawdown,
    financial_risks
):

    priority = {
        "Low": 1,
        "Moderate": 2,
        "High": 3,
        "Critical": 4,
        "Very High": 4,
        "Unavailable": 0
    }

    levels = [
        volatility.risk_level,
        drawdown.risk_level
    ]

    levels.extend(
        risk.severity for risk in financial_risks
    )

    available_levels = [
        level for level in levels
        if priority.get(level, 0) > 0
    ]

    if not available_levels:
        return "Unavailable"

    highest = max(
        available_levels,
        key=lambda level: priority.get(level, 0)
    )

    if highest == "Very High":
        return "Critical"

    return highest


# -----------------------------------------
# 7. Main Risk Analysis Function
# -----------------------------------------

def analyze_stock_risk(
    symbol,
    period,
    historical_data,
    company_profile=None,
    financial_information=None
):

    # Calculate historical price risks
    price_risk = calculate_price_risk(
        historical_data
    )

    volatility = HistoricalVolatility(
        **price_risk["historical_volatility"]
    )

    drawdown = MaximumDrawdown(
        **price_risk["maximum_drawdown"]
    )

    # Extract company information
    profile = company_profile or {}

    company_name = profile.get("company_name")

    sector = profile.get("sector")

    # Analyze financial statements
    financial_risks = analyze_financial_risks(
        financial_information
    )

    # Identify missing information
    missing_information = []

    if not company_profile:

        missing_information.append(
            "Company profile is unavailable."
        )

    unavailable_statements = get_unavailable_statements(
        financial_information
    )

    for statement_name in unavailable_statements:

        missing_information.append(
            f"{statement_name.replace('_', ' ').title()} "
            "is unavailable or contains no data."
        )

    if not financial_information:

        missing_information.append(
            "Financial information could not be retrieved."
        )

    if not financial_risks:

        missing_information.append(
            "No financial risk indicators were identified. "
            "This does not prove that financial risks are absent."
        )

    missing_information.extend([
        "Other agents' findings are not yet connected.",
        "Sector-specific evidence is not yet independently verified."
    ])

    # Determine overall risk
    overall_risk = determine_overall_risk(
        volatility,
        drawdown,
        financial_risks
    )

    # Build preliminary report
    report = RiskAnalysisResponse(

        company_name=company_name,

        symbol=symbol.upper(),

        sector=sector,

        period=period,

        historical_volatility=volatility,

        maximum_drawdown=drawdown,

        financial_risks=financial_risks,

        sector_risks=[],

        conflicting_findings=[],

        missing_information=missing_information,

        alternative_scenarios=[],

        uncertainties_and_limitations=[
            "Historical volatility and drawdown describe past price movements.",
            "Financial risk checks use available annual financial statements.",
            "Some financial metrics may be missing or outdated.",
            "Risk thresholds are preliminary screening rules, not universal standards.",
            "Sector and other agent findings have not yet been integrated."
        ],

        overall_risk=overall_risk,

        risk_summary=(
            "Preliminary risk assessment based on historical "
            "price data and available financial statements."
        )
    )

    return report.model_dump()

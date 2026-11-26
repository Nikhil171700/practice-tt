
# from pydantic import BaseModel, Field, ConfigDict
# from typing import Optional, List, Literal


# # -------------------------------
# # 1. API Request
# # -------------------------------

# class RiskAnalysisRequest(BaseModel):

#     model_config = ConfigDict(str_strip_whitespace=True)

#     symbol: str = Field(
#         min_length=1,
#         max_length=20,
#         pattern=r"^[A-Za-z0-9._-]+$"
#     )

#     period: Literal[
#         "1mo", "3mo", "6mo", "1y", "2y", "5y"
#     ]

#     company_name: Optional[str] = None
#     sector: Optional[str] = None
#     industry: Optional[str] = None


# # -------------------------------
# # 2. Financial Risk
# # -------------------------------

# class FinancialRisk(BaseModel):

#     risk_name: str
#     description: str

#     severity: Literal[
#         "Low", "Moderate", "High", "Critical"
#     ]

#     evidence: Optional[str] = None


# # -------------------------------
# # 3. Other Agent Findings
# # -------------------------------

# class AgentFinding(BaseModel):

#     agent_name: str
#     finding: str
#     risk_level: Optional[str] = None


# # -------------------------------
# # 4. Historical Volatility
# # -------------------------------

# class HistoricalVolatility(BaseModel):

#     value: Optional[float] = None
#     unit: str = "Percentage"

#     risk_level: Literal[
#         "Low", "Moderate", "High", "Very High", "Unavailable"
#     ]

#     method: str


# # -------------------------------
# # 5. Maximum Drawdown
# # -------------------------------

# class MaximumDrawdown(BaseModel):

#     maximum_drawdown: Optional[float] = None
#     peak_price: Optional[float] = None
#     trough_price: Optional[float] = None

#     peak_date: Optional[str] = None
#     trough_date: Optional[str] = None

#     risk_level: Literal[
#         "Low", "Moderate", "High", "Very High", "Unavailable"
#     ]


# # -------------------------------
# # 6. Alternative Scenarios
# # -------------------------------

# class RiskScenario(BaseModel):

#     scenario: Literal[
#         "Positive", "Neutral", "Negative"
#     ]

#     description: str
#     possible_impact: str


# # -------------------------------
# # 7. Gemini Interpretation
# # -------------------------------

# class RiskInterpretation(BaseModel):

#     sector_risks: List[FinancialRisk] = Field(
#         default_factory=list
#     )

#     alternative_scenarios: List[RiskScenario] = Field(
#         default_factory=list
#     )

#     conflicting_findings: List[str] = Field(
#         default_factory=list
#     )

#     uncertainties_and_limitations: List[str] = Field(
#         default_factory=list
#     )

#     risk_summary: str


# # -------------------------------
# # 8. Final Risk Analysis Response
# # -------------------------------

# class RiskAnalysisResponse(BaseModel):

#     company_name: Optional[str] = None
#     symbol: str
#     sector: Optional[str] = None
#     period: str

#     historical_volatility: HistoricalVolatility
#     maximum_drawdown: MaximumDrawdown

#     financial_risks: List[FinancialRisk] = Field(
#         default_factory=list
#     )

#     sector_risks: List[FinancialRisk] = Field(
#         default_factory=list
#     )

#     conflicting_findings: List[str] = Field(
#         default_factory=list
#     )

#     missing_information: List[str] = Field(
#         default_factory=list
#     )

#     alternative_scenarios: List[RiskScenario] = Field(
#         default_factory=list
#     )

#     uncertainties_and_limitations: List[str] = Field(
#         default_factory=list
#     )

#     overall_risk: Literal[
#         "Low", "Moderate", "High", "Critical", "Unavailable"
#     ]

#     risk_summary: str

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal


# -------------------------------
# 1. API Request
# -------------------------------

class RiskAnalysisRequest(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True)

    symbol: str = Field(
        min_length=1,
        max_length=20,
        pattern=r"^[A-Za-z0-9._-]+$"
    )

    period: Literal[
        "1mo", "3mo", "6mo", "1y", "2y", "5y"
    ]

    company_name: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None


# -------------------------------
# 2. Financial Risk
# -------------------------------

class FinancialRisk(BaseModel):

    risk_name: str
    description: str

    severity: Literal[
        "Low", "Moderate", "High", "Critical"
    ]

    evidence: Optional[str] = None


# -------------------------------
# 3. Other Agent Findings
# -------------------------------

class AgentFinding(BaseModel):

    agent_name: str
    finding: str
    risk_level: Optional[str] = None


# -------------------------------
# 4. Historical Volatility
# -------------------------------

class HistoricalVolatility(BaseModel):

    value: Optional[float] = None
    unit: str = "Percentage"

    risk_level: Literal[
        "Low", "Moderate", "High", "Very High", "Unavailable"
    ]

    method: str


# -------------------------------
# 5. Maximum Drawdown
# -------------------------------

class MaximumDrawdown(BaseModel):

    maximum_drawdown: Optional[float] = None
    peak_price: Optional[float] = None
    trough_price: Optional[float] = None

    peak_date: Optional[str] = None
    trough_date: Optional[str] = None

    risk_level: Literal[
        "Low", "Moderate", "High", "Very High", "Unavailable"
    ]


# -------------------------------
# 6. Alternative Scenarios
# -------------------------------

class RiskScenario(BaseModel):

    scenario: Literal[
        "Positive", "Neutral", "Negative"
    ]

    description: str
    possible_impact: str


# -------------------------------
# 7. Groq Interpretation
# -------------------------------

class RiskInterpretation(BaseModel):

    sector_risks: List[FinancialRisk] = Field(
        default_factory=list
    )

    alternative_scenarios: List[RiskScenario] = Field(
        default_factory=list
    )

    conflicting_findings: List[str] = Field(
        default_factory=list
    )

    uncertainties_and_limitations: List[str] = Field(
        default_factory=list
    )

    risk_summary: str


# -------------------------------
# 8. Final Risk Analysis Response
# -------------------------------

class RiskAnalysisResponse(BaseModel):

    company_name: Optional[str] = None
    symbol: str
    sector: Optional[str] = None
    period: str

    historical_volatility: HistoricalVolatility
    maximum_drawdown: MaximumDrawdown

    financial_risks: List[FinancialRisk] = Field(
        default_factory=list
    )

    sector_risks: List[FinancialRisk] = Field(
        default_factory=list
    )

    conflicting_findings: List[str] = Field(
        default_factory=list
    )

    missing_information: List[str] = Field(
        default_factory=list
    )

    alternative_scenarios: List[RiskScenario] = Field(
        default_factory=list
    )

    uncertainties_and_limitations: List[str] = Field(
        default_factory=list
    )

    overall_risk: Literal[
        "Low", "Moderate", "High", "Critical", "Unavailable"
    ]

    risk_summary: str

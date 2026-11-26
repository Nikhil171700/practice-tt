
# import os
# import json

# from dotenv import load_dotenv
# # from google import genai
# # from google.genai import types
# from groq import Groq
# from schemas.risk_schema import (
#     RiskAnalysisResponse,
#     RiskInterpretation
# )


# # -----------------------------------------
# # 1. Load Gemini Configuration
# # -----------------------------------------

# load_dotenv()

# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # GEMINI_MODEL = os.getenv(
# #     "GEMINI_MODEL",
# #     "gemini-3.8-flash"
# # )
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# GROQ_MODEL = os.getenv("GROQ_MODEL")

# # -----------------------------------------
# # 2. Gemini Risk Interpretation
# # -----------------------------------------

# def explain_risk_report(risk_report):

#     if not GROQ_API_KEY:
#         raise ValueError(
#             "GROQ_API_KEY is missing from the .env file."
#         )

#     if not GROQ_MODEL:
#         raise ValueError(
#             "GROQ_MODEL is missing from the .env file."
#         )
#     # Validate Python-generated report
#     validated_report = RiskAnalysisResponse.model_validate(
#         risk_report
#     )

#     report_data = validated_report.model_dump()

#     client = genai.Client(
#         api_key=GROQ_API_KEY
#     )

#     # ---------------------------------
#     # Tool: Retrieve Validated Evidence
#     # ---------------------------------

#     def get_validated_risk_evidence():

#         """
#         Retrieves the validated numerical risk results,
#         company information and financial risk findings.
#         """

#         return json.dumps(
#             report_data,
#             default=str
#         )

#     # ---------------------------------
#     # Gemini Instructions
#     # ---------------------------------

#     prompt = """
#     You are a professional financial risk analysis assistant.

#     First, call the get_validated_risk_evidence tool
#     to retrieve the stock risk report.

#     Analyze the evidence and return a structured interpretation.

#     Your responsibilities:

#     1. Identify relevant sector-related risks.
#     2. Generate a positive scenario.
#     3. Generate a neutral scenario.
#     4. Generate a negative scenario.
#     5. Identify conflicting findings if available.
#     6. Explain missing information.
#     7. Explain uncertainties and limitations.
#     8. Provide a clear overall risk summary.

#     IMPORTANT RULES:

#     - Never invent stock prices or financial figures.
#     - Never modify Python-calculated numerical metrics.
#     - Do not assume that a company's sector automatically
#       proves a particular risk exists.
#     - Distinguish general sector risks from verified company risks.
#     - Scenarios must be hypothetical possibilities, not predictions.
#     - If evidence is unavailable, clearly mention it.
#     - Do not claim that other agents' findings are available
#       when they have not been supplied.
#     - Do not provide guaranteed investment advice.
#     - Explain everything in simple English.
#     """

#     try:

#         # ---------------------------------
#         # Generate Structured Gemini Output
#         # ---------------------------------

#         response = client.models.generate_content(

#             model=GEMINI_MODEL,

#             contents=prompt,

#             config=types.GenerateContentConfig(

#                 tools=[
#                     get_validated_risk_evidence
#                 ],

#                 temperature=0.2,

#                 response_mime_type="application/json",

#                 response_schema=RiskInterpretation
#             )
#         )

#         # ---------------------------------
#         # Validate Gemini Response
#         # ---------------------------------

#         interpretation = response.parsed

#         if interpretation is None:

#             raise ValueError(
#                 "Gemini did not return a valid structured response."
#             )

#         validated_interpretation = (
#             RiskInterpretation.model_validate(
#                 interpretation
#             )
#         )

#         return validated_interpretation.model_dump()

#     finally:

#         client.close()

# import os
# import json

# from dotenv import load_dotenv
# from groq import Groq

# from schemas.risk_schema import (
#     RiskAnalysisResponse,
#     RiskInterpretation
# )


# # -----------------------------------------
# # 1. Load Groq Configuration
# # -----------------------------------------

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# GROQ_MODEL = os.getenv("GROQ_MODEL")


# # -----------------------------------------
# # 2. Groq Risk Interpretation
# # -----------------------------------------

# def explain_risk_report(risk_report):

#     if not GROQ_API_KEY:
#         raise ValueError(
#             "GROQ_API_KEY is missing from the .env file."
#         )

#     if not GROQ_MODEL:
#         raise ValueError(
#             "GROQ_MODEL is missing from the .env file."
#         )

#     # Validate Python-generated report
#     validated_report = RiskAnalysisResponse.model_validate(
#         risk_report
#     )

#     report_data = validated_report.model_dump()

#     client = Groq(
#         api_key=GROQ_API_KEY
#     )

#     try:

#         # ---------------------------------
#         # Tool: Retrieve Validated Evidence
#         # ---------------------------------

#         def get_validated_risk_evidence():

#             """
#             Retrieves validated numerical risk results,
#             company information and financial risk findings.
#             """

#             return json.dumps(
#                 report_data,
#                 default=str
#             )

#         # ---------------------------------
#         # Groq Instructions
#         # ---------------------------------

#         prompt = """
#         You are a professional financial risk analysis assistant.

#         IMPORTANT:
#         Return your final interpretation in valid JSON format.
#         The JSON must match the RiskInterpretation Pydantic schema.
#         Do not include Markdown code fences or additional text.

#         First, call the get_validated_risk_evidence tool
#         to retrieve the stock risk report.

#         Analyze the evidence and return a structured interpretation.

#         Your responsibilities:

#         1. Identify relevant sector-related risks.
#         2. Generate a positive scenario.
#         3. Generate a neutral scenario.
#         4. Generate a negative scenario.
#         5. Identify conflicting findings if available.
#         6. Explain missing information.
#         7. Explain uncertainties and limitations.
#         8. Provide a clear overall risk summary.

#         IMPORTANT RULES:

#         - Never invent stock prices or financial figures.
#         - Never modify Python-calculated numerical metrics.
#         - Do not assume that a company's sector automatically
#           proves a particular risk exists.
#         - Distinguish general sector risks from verified company risks.
#         - Scenarios must be hypothetical possibilities, not predictions.
#         - If evidence is unavailable, clearly mention it.
#         - Do not claim that other agents' findings are available
#           when they have not been supplied.
#         - Do not provide guaranteed investment advice.
#         - Explain everything in simple English.
#         """

#         # ---------------------------------
#         # Tool Definition
#         # ---------------------------------

#         tools = [
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "get_validated_risk_evidence",
#                     "description": (
#                         "Retrieve validated Python-generated "
#                         "stock risk analysis results."
#                     ),
#                     "parameters": {
#                         "type": "object",
#                         "properties": {},
#                         "required": []
#                     }
#                 }
#             }
#         ]

#         messages = [
#             {
#                 "role": "system",
#                 "content": prompt
#             },
#             {
#                 "role": "user",
#                 "content": "Analyze the validated stock risk report and return the interpretation in JSON format."
#             }
#         ]

#         # ---------------------------------
#         # First Groq Call: Tool Calling
#         # ---------------------------------

#         response = client.chat.completions.create(

#             model=GROQ_MODEL,

#             messages=messages,

#             tools=tools,

#             tool_choice="required",

#             temperature=0.2
#         )

#         assistant_message = response.choices[0].message

#         if not assistant_message.tool_calls:
#             raise ValueError(
#                 "Groq did not call the risk evidence tool."
#             )

#         messages.append(
#             assistant_message.model_dump(exclude_none=True)
#         )

#         # ---------------------------------
#         # Execute Tool
#         # ---------------------------------

#         for tool_call in assistant_message.tool_calls:

#             if (
#                 tool_call.function.name
#                 == "get_validated_risk_evidence"
#             ):

#                 evidence = get_validated_risk_evidence()

#                 messages.append({
#                     "role": "tool",
#                     "tool_call_id": tool_call.id,
#                     "content": evidence
#                 })

#             else:
#                 raise ValueError(
#                     "Groq requested an unknown tool."
#                 )

#         # ---------------------------------
#         # Second Groq Call: Interpretation
#         # ---------------------------------

#         final_response = client.chat.completions.create(

#             model=GROQ_MODEL,

#             messages=messages,

#             response_format={
#                 "type": "json_object"
#             },

#             temperature=0.2
#         )

#         # ---------------------------------
#         # Parse Groq Response
#         # ---------------------------------

#         response_content = (
#             final_response.choices[0].message.content
#         )

#         if not response_content:
#             raise ValueError(
#                 "Groq returned an empty interpretation."
#             )

#         interpretation = json.loads(
#             response_content
#         )

#         # ---------------------------------
#         # Validate Groq Response with Pydantic
#         # ---------------------------------

#         validated_interpretation = (
#             RiskInterpretation.model_validate(
#                 interpretation
#             )
#         )

#         return validated_interpretation.model_dump()

#     finally:

#         client.close()

# import os
# import json

# from dotenv import load_dotenv
# from groq import Groq

# from schemas.risk_schema import (
#     RiskAnalysisResponse,
#     RiskInterpretation
# )


# # -----------------------------------------
# # 1. Load Groq Configuration
# # -----------------------------------------

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = os.getenv("GROQ_MODEL")


# # -----------------------------------------
# # 2. Groq Risk Interpretation
# # -----------------------------------------

# def explain_risk_report(risk_report):

#     if not GROQ_API_KEY:
#         raise ValueError(
#             "GROQ_API_KEY is missing from the .env file."
#         )

#     if not GROQ_MODEL:
#         raise ValueError(
#             "GROQ_MODEL is missing from the .env file."
#         )

#     # Validate Python-generated report
#     validated_report = RiskAnalysisResponse.model_validate(
#         risk_report
#     )

#     report_data = validated_report.model_dump()

#     client = Groq(api_key=GROQ_API_KEY)

#     try:

#         # ---------------------------------
#         # Tool: Retrieve Validated Evidence
#         # ---------------------------------

#         def get_validated_risk_evidence():
#             return json.dumps(
#                 report_data,
#                 default=str
#             )

#         # ---------------------------------
#         # Groq Instructions
#         # ---------------------------------

#         prompt = """
#         You are a professional financial risk analysis assistant.

#         First, call the get_validated_risk_evidence tool.

#         Analyze only the evidence returned by that tool.

#         Return valid JSON matching the RiskInterpretation schema.

#         The JSON MUST contain ALL these fields:

#         {
#             "sector_risks": [],
#             "alternative_scenarios": [],
#             "conflicting_findings": [],
#             "uncertainties_and_limitations": [],
#             "risk_summary": "A clear overall risk summary"
#         }

#         FIELD REQUIREMENTS:

#         1. sector_risks:
#            A list of objects containing:
#            risk_name, description, severity, evidence.

#            severity must be Low, Moderate, High, or Critical.

#         2. alternative_scenarios:
#            A list of objects containing:
#            scenario, description, possible_impact.

#            scenario must be Positive, Neutral, or Negative.

#         3. conflicting_findings:
#            A list of strings.

#         4. uncertainties_and_limitations:
#            A list of strings.

#         5. risk_summary:
#            A mandatory, non-empty string explaining the overall
#            risk situation in simple English.

#         IMPORTANT RULES:

#         - Never omit risk_summary.
#         - Never return null for risk_summary.
#         - Use empty lists when no evidence is available.
#         - Never invent stock prices or financial figures.
#         - Never modify Python-calculated numerical metrics.
#         - Distinguish general sector risks from verified company risks.
#         - Scenarios must be hypothetical possibilities, not predictions.
#         - Do not claim other agents' findings are available
#           when they have not been supplied.
#         - Explain missing information and uncertainty.
#         - Do not provide guaranteed investment advice.
#         - Use simple English.
#         """

#         # ---------------------------------
#         # Tool Definition
#         # ---------------------------------

#         tools = [
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "get_validated_risk_evidence",
#                     "description": (
#                         "Retrieve validated Python-generated "
#                         "stock risk analysis results."
#                     ),
#                     "parameters": {
#                         "type": "object",
#                         "properties": {},
#                         "required": []
#                     }
#                 }
#             }
#         ]

#         messages = [
#             {
#                 "role": "system",
#                 "content": prompt
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     "Analyze the validated stock risk report "
#                     "and return every required JSON field."
#                 )
#             }
#         ]

#         # ---------------------------------
#         # First Groq Call: Tool Calling
#         # ---------------------------------

#         response = client.chat.completions.create(
#             model=GROQ_MODEL,
#             messages=messages,
#             tools=tools,
#             tool_choice="required",
#             temperature=0.2
#         )

#         assistant_message = response.choices[0].message

#         if not assistant_message.tool_calls:
#             raise ValueError(
#                 "Groq did not call the risk evidence tool."
#             )

#         messages.append(
#             assistant_message.model_dump(exclude_none=True)
#         )

#         # ---------------------------------
#         # Execute Tool
#         # ---------------------------------

#         for tool_call in assistant_message.tool_calls:

#             if (
#                 tool_call.function.name
#                 == "get_validated_risk_evidence"
#             ):

#                 evidence = get_validated_risk_evidence()

#                 messages.append({
#                     "role": "tool",
#                     "tool_call_id": tool_call.id,
#                     "content": evidence
#                 })

#             else:
#                 raise ValueError(
#                     "Groq requested an unknown tool."
#                 )

#         # ---------------------------------
#         # Second Groq Call: Interpretation
#         # ---------------------------------

#         final_response = client.chat.completions.create(
#             model=GROQ_MODEL,
#             messages=messages,
#             response_format={
#                 "type": "json_object"
#             },
#             temperature=0.2
#         )

#         # ---------------------------------
#         # Parse Groq Response
#         # ---------------------------------

#         response_content = (
#             final_response.choices[0].message.content
#         )

#         if not response_content:
#             raise ValueError(
#                 "Groq returned an empty interpretation."
#             )

#         interpretation = json.loads(response_content)

#         # ---------------------------------
#         # Validate Groq Response with Pydantic
#         # ---------------------------------

#         validated_interpretation = (
#             RiskInterpretation.model_validate(
#                 interpretation
#             )
#         )

#         return validated_interpretation.model_dump()

#     finally:
#         client.close()

import os
import json

from dotenv import load_dotenv
from groq import Groq

from schemas.risk_schema import (
    RiskAnalysisResponse,
    RiskInterpretation
)


# -----------------------------------------
# 1. Load Groq Configuration
# -----------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")


# -----------------------------------------
# 2. Groq Risk Interpretation
# -----------------------------------------

def explain_risk_report(risk_report):

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing from the .env file."
        )

    if not GROQ_MODEL:
        raise ValueError(
            "GROQ_MODEL is missing from the .env file."
        )

    # Validate Python-generated report
    validated_report = RiskAnalysisResponse.model_validate(
        risk_report
    )

    report_data = validated_report.model_dump()

    client = Groq(api_key=GROQ_API_KEY)

    try:

        # ---------------------------------
        # Tool: Retrieve Validated Evidence
        # ---------------------------------

        def get_validated_risk_evidence():

            """
            Retrieves validated numerical risk results,
            company information and financial risk findings.
            """

            return json.dumps(
                report_data,
                default=str
            )

        # ---------------------------------
        # Groq Instructions
        # ---------------------------------

        prompt = """
        You are a professional financial risk analysis assistant.

        IMPORTANT:
        Return your final interpretation in valid JSON format.
        The JSON must match the RiskInterpretation Pydantic schema.
        Do not include Markdown code fences or additional text.

        First, call the get_validated_risk_evidence tool
        to retrieve the stock risk report.

        Analyze the evidence and return a structured interpretation.

        Your responsibilities:

        1. Identify relevant sector-related risks.
        2. Generate a positive scenario.
        3. Generate a neutral scenario.
        4. Generate a negative scenario.
        5. Identify conflicting findings if available.
        6. Explain missing information.
        7. Explain uncertainties and limitations.
        8. Provide a clear overall risk summary.

        IMPORTANT RULES:

        - Never invent stock prices or financial figures.
        - Never modify Python-calculated numerical metrics.
        - Do not assume that a company's sector automatically
          proves a particular risk exists.
        - Distinguish general sector risks from verified company risks.
        - Scenarios must be hypothetical possibilities, not predictions.
        - If evidence is unavailable, clearly mention it.
        - Do not claim that other agents' findings are available
          when they have not been supplied.
        - Do not provide guaranteed investment advice.
        - Explain everything in simple English.

        JSON REQUIREMENTS:

        - Always include sector_risks as a list.
        - Always include alternative_scenarios as a list.
        - Always include conflicting_findings as a list.
        - Always include uncertainties_and_limitations as a list.
        - Always include risk_summary as a non-empty string.
        - Generate all three scenarios: Positive, Neutral and Negative.
        """

        # ---------------------------------
        # Tool Definition
        # ---------------------------------

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_validated_risk_evidence",
                    "description": (
                        "Retrieve validated Python-generated "
                        "stock risk analysis results."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": (
                    "Analyze the validated stock risk report "
                    "and return the interpretation in JSON format."
                )
            }
        ]

        # ---------------------------------
        # First Groq Call: Tool Calling
        # ---------------------------------

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=tools,
            tool_choice="required",
            temperature=0.2
        )

        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            raise ValueError(
                "Groq did not call the risk evidence tool."
            )

        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # ---------------------------------
        # Execute Tool
        # ---------------------------------

        for tool_call in assistant_message.tool_calls:

            if (
                tool_call.function.name
                == "get_validated_risk_evidence"
            ):

                evidence = get_validated_risk_evidence()

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": evidence
                })

            else:
                raise ValueError(
                    "Groq requested an unknown tool."
                )

        # ---------------------------------
        # Second Groq Call: Interpretation
        # ---------------------------------

        final_response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            response_format={
                "type": "json_object"
            },
            temperature=0.2
        )

        # ---------------------------------
        # Parse Groq Response
        # ---------------------------------

        response_content = (
            final_response.choices[0].message.content
        )

        if not response_content:
            raise ValueError(
                "Groq returned an empty interpretation."
            )

        interpretation = json.loads(response_content)

        # ---------------------------------
        # Validate Groq Response with Pydantic
        # ---------------------------------

        validated_interpretation = (
            RiskInterpretation.model_validate(
                interpretation
            )
        )

        return validated_interpretation.model_dump()

    finally:
        client.close()

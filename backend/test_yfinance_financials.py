
import yfinance as yf

ticker = yf.Ticker("INFY.NS")

print("Company Name:", ticker.info.get("longName"))
print("Sector:", ticker.info.get("sector"))
print("Industry:", ticker.info.get("industry"))

print("\n--- Balance Sheet ---")
print(ticker.balance_sheet)

print("\n--- Income Statement ---")
print(ticker.income_stmt)

print("\n--- Cash Flow ---")
print(ticker.cashflow)

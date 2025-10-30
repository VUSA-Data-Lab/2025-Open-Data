import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["VWCE.DE", "EUNL.DE", "CSPX.DE", "WDEF.DE"]

data = yf.download(tickers, period="5y")["Adj Close"].dropna()

# Normalized performance chart (start = 100)
normalized = data / data.iloc[0] * 100
normalized.plot(figsize=(12, 6))
plt.title("ETF Performance (Last 5 Years, Base = 100)")
plt.ylabel("Index (100 = start)")
plt.grid(True)
plt.tight_layout()
plt.savefig("performance_5y.png")
plt.show()

data_1y = yf.download(tickers, period="1y")["Adj Close"].dropna()
normalized_1y = data_1y / data_1y.iloc[0] * 100
normalized_1y.plot(figsize=(12, 6))
plt.title("ETF Performance (Last 1 Year, Base = 100)")
plt.ylabel("Index (100 = start)")
plt.grid(True)
plt.tight_layout()
plt.savefig("performance_1y.png")
plt.show()

print("✅ Grafikai sugeneruoti: performance_5y.png ir performance_1y.png")

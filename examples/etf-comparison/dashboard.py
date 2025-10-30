import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("ETF Palyginimo Dashboard")

default_tickers = ["VWCE.DE", "EUNL.DE", "CSPX.DE", "WDEF.DE"]
tickers = st.multiselect("Pasirinkite ETF", default_tickers, default=default_tickers)

period = st.selectbox(
    "Laikotarpis",
    ["1y", "3y", "5y", "max"],
    index=0
)

if len(tickers) > 0:
    data = yf.download(tickers, period=period)["Adj Close"].dropna()
    normalized = data / data.iloc[0] * 100

    st.line_chart(normalized)

    st.write("### Normalizuoti duomenys (100 = pradžios taškas)")
    st.dataframe(normalized.tail(10))
else:
    st.warning("Pasirinkite bent vieną ETF.")

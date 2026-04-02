import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("Yahoo Finance Data App")

ticker_symbol = st.text_input("Enter ticker symbol", "AAPL").upper()

if ticker_symbol:
    stock = yf.Ticker(ticker_symbol)

    # 1) Price data: usually the most important part
    try:
        hist = stock.history(period="1y")
        if hist.empty:
            st.warning("No historical price data found.")
        else:
            st.subheader("Historical Price Data")
            st.dataframe(hist.tail())
            st.line_chart(hist["Close"])
    except Exception as e:
        st.error(f"Could not fetch price history: {e}")

    # 2) Lightweight summary data instead of stock.info
    try:
        fast = stock.fast_info

        summary = {
            "Last Price": fast.get("lastPrice"),
            "Previous Close": fast.get("previousClose"),
            "Open": fast.get("open"),
            "Day High": fast.get("dayHigh"),
            "Day Low": fast.get("dayLow"),
            "Volume": fast.get("lastVolume"),
            "Market Cap": fast.get("marketCap"),
            "Currency": fast.get("currency"),
        }

        st.subheader("Stock Summary")
        st.write(pd.DataFrame(summary.items(), columns=["Metric", "Value"]))
    except Exception as e:
        st.warning(f"Summary data temporarily unavailable: {e}")

    # 3) Optional: only fetch full info if user asks
    if st.checkbox("Show extended company info (may hit rate limit)"):
        try:
            time.sleep(2)  # small delay helps a bit
            info = stock.info
            st.subheader("Extended Company Info")
            st.json({
                "longName": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "country": info.get("country"),
                "website": info.get("website"),
                "longBusinessSummary": info.get("longBusinessSummary"),
            })
        except Exception as e:
            st.error(
                "Yahoo Finance rate-limited the extended info request. "
                "Try again later or leave this box unchecked."
            )

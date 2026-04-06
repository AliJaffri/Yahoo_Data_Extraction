import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Page title
st.title("Stock Price Viewer")
st.write("This app downloads stock data and shows the closing price chart.")

# User input
ticker = st.text_input("Enter a stock ticker:", "AAPL")
start_date = st.date_input("Start date", pd.to_datetime("2024-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))

# Download data
if st.button("Get Data"):
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        st.error("No data found. Please check the ticker symbol.")
    else:
        st.subheader("Raw Data")
        st.dataframe(data)

        st.subheader("Closing Price Chart")
        fig, ax = plt.subplots()
        ax.plot(data.index, data["Close"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price")
        ax.set_title(f"{ticker} Closing Price")
        st.pyplot(fig)

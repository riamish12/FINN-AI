import os
os.system("pip install yfinance")
import yfinance as yf
import streamlit as st
import requests
import pandas as pd

# 🎙️ FINN's personality stays intact!
st.title("💰 FINN - AI Financial Assistant")
st.write("Hello! I’m **FINN**, your AI financial Advisor. Ask me about stocks, investments, and market insights.")

# ✅ Function to Fetch Live Stock Price
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1d")
        
        if stock_data.empty:
            return "❌ Yahoo Finance is not returning data. This may be a Yahoo issue."
        
        price = stock_data["Close"].iloc[-1]
        return f"📈 The current price of {ticker.upper()} is **${price:.2f}**."
    
    except Exception as e:
        return f"❌ Error fetching stock data: {e}"

# 🏦 User Input for Stock Symbol
ticker = st.text_input("Enter stock ticker (e.g., TSLA):")

if st.button("Get Stock Price"):
    if ticker:
        response = get_stock_price(ticker)
        st.write(response)
    else:
        st.warning("⚠️ Please enter a stock ticker.")

# 📝 Debugging Logs (Shown in Hugging Face Logs)
try:
    debug_test = yf.Ticker("TSLA").history(period="1d")
    if debug_test.empty:
        print("❌ Yahoo Finance is not returning data. Check if the API is working.")
    else:
        print(f"✅ Debug Test: Live Tesla price fetched successfully.")
except Exception as err:
    print(f"❌ Debugging Error: {err}")


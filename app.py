import streamlit as st
import requests
import json

# 🔹 Replace with your Finnhub API Key
FINNHUB_API_KEY = "cvctdp1r01qodeubgv3gcvctdp1r01qodeubgv40"
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# 🔹 Streamlit UI Setup
st.title("💰 FINN - AI Financial Assistant")
st.write("Hello! I’m FINN, your AI financial Advisor. Ask me about stocks, investments, and market insights.")

# 🔹 User input for stock ticker
ticker = st.text_input("Enter stock ticker (e.g., TSLA)", "")

# 🔹 Function to fetch stock price
def get_stock_price(symbol):
    try:
        url = f"{FINNHUB_BASE_URL}/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if "c" in data and data["c"] is not None:
            return data["c"]
        else:
            return None
    except Exception as e:
        return None

# 🔹 Fetch and display stock price
if ticker:
    st.write(f"Fetching real-time price for **{ticker.upper()}**...")
    
    price = get_stock_price(ticker.upper())
    
    if price is not None:
        st.success(f"✅ **Current price of {ticker.upper()}: ${price:.2f}**")
    else:
        st.error("❌ Unable to fetch stock price. Please check the stock symbol or try again later.")

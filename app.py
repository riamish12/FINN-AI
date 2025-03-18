import streamlit as st
import ollama
import yfinance as yf
import requests
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates
from pycoingecko import CoinGeckoAPI
from newsapi import NewsApiClient

# API Keys (Replace with valid keys)
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

# Initialize APIs
currency_rates = CurrencyRates()
cg = CoinGeckoAPI()
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Streamlit Page Config
st.set_page_config(page_title="💰 FINN - AI Financial Assistant", page_icon="🤖")

# Custom CSS for Chat Look
st.markdown("""
    <style>
    .message { padding: 10px; border-radius: 10px; margin: 5px 0; }
    .user { background-color: #d1e7fd; text-align: right; }
    .bot { background-color: #e3e3e3; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

# Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("💰 FINN - AI Financial Assistant")
st.write("Hello! I’m FINN, your AI financial advisor. Ask me about stocks, investments, and market insights!")

# Function to Fetch Stock Prices
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="1d")

        if stock_data.empty:
            return "❌ Yahoo Finance is not returning data. This may be a Yahoo issue."

        price = stock_data["Close"].iloc[-1]
        return f"✅ Current price of {ticker.upper()}: **${price:.2f}**"

    except Exception as e:
        return f"❌ Error fetching stock data: {e}"

# Function to Fetch Crypto Prices
def get_crypto_price(crypto):
    try:
        data = cg.get_price(ids=crypto, vs_currencies='usd')
        if not data:
            return "❌ Unable to fetch crypto prices. Try again later."
        return f"✅ Current price of {crypto.capitalize()}: **${data[crypto]['usd']:.2f}**"

    except:
        return "❌ Error fetching crypto price."

# Function to Fetch Forex Exchange Rates
def get_forex_rate(currency_pair):
    try:
        base, target = currency_pair.split("/")
        rate = currency_rates.get_rate(base.upper(), target.upper())
        return f"✅ Exchange rate for {currency_pair.upper()}: **{rate:.2f}**"
    except:
        return "❌ Unable to fetch exchange rate."

# Function to Fetch Market News
def get_market_news():
    try:
        articles = newsapi.get_top_headlines(category="business", language="en")["articles"]
        if not articles:
            return "❌ No market news available."
        news_list = "\n\n".join([f"📰 **{article['title']}**\n{article['url']}" for article in articles[:5]])
        return f"📢 **Latest Market News:**\n\n{news_list}"
    except:
        return "❌ Error fetching market news."

# Function to Provide AI Financial Insights
def ai_financial_advice(user_input):
    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": user_input}]
        )["message"]["content"]
        return response
    except:
        return "❌ AI is currently unavailable. Try again later."

# Display Chat History
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "bot"
    st.markdown(f'<div class="message {role}">{message["content"]}</div>', unsafe_allow_html=True)

# User Input Field
user_input = st.text_input("Type your message:", key="input")

# Handle User Input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = ""

    # Detect Intent (Stock, Crypto, Forex, News, or AI Finance Advice)
    if "stock price of" in user_input.lower():
        ticker = user_input.split("stock price of")[-1].strip().upper()
        response = get_stock_price(ticker)

    elif "crypto price of" in user_input.lower():
        crypto = user_input.split("crypto price of")[-1].strip().lower()
        response = get_crypto_price(crypto)

    elif "forex rate of" in user_input.lower():
        pair = user_input.split("forex rate of")[-1].strip().upper()
        response = get_forex_rate(pair)

    elif "market news" in user_input.lower() or "finance news" in user_input.lower():
        response = get_market_news

import streamlit as st
import yfinance as yf
import pandas as pd
from textblob import TextBlob

st.title("Free NSE Predictor Bot")

ticker = st.text_input("NSE Stock (e.g. RELIANCE.NS):").upper()
if ticker and st.button("Predict Buy/Sell"):

    data = yf.download(ticker, period="1mo")
    data['EMA20'] = data['Close'].ewm(span=20).mean()
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    latest = data.iloc[-1]
    signal = "🟢 BUY" if latest['Close'] > latest['EMA20'] and latest['RSI'] < 70 else "🔴 SELL"
    
    sentiment = TextBlob("Positive market news").sentiment.polarity
    
    st.success(f"**{signal}** at ₹{latest['Close']:.0f} | RSI: {latest['RSI']:.1f} | EMA Bullish: {'Yes' if latest['Close'] > latest['EMA20'] else 'No'}")
    st.line_chart(data[['Close', 'EMA20']][-10:])

st.info("Type NSE ticker + Predict!")

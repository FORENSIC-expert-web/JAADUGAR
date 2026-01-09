import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("🔥 Free NSE Predictor Bot")

ticker = st.text_input("Enter NSE Stock (RELIANCE.NS):", "RELIANCE.NS").upper()
if st.button("🚀 Predict Buy/Sell") and ticker:

    with st.spinner("Fetching live NSE data..."):
        try:
            data = yf.download(ticker, period="1mo", progress=False, timeout=10)
            if data.empty:
                st.error("❌ No data! Check ticker (add .NS) or internet.")
            else:
                data['EMA20'] = data['Close'].ewm(span=20).mean()
                delta = data['Close'].diff(1)
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = -delta.where(delta < 0, 0).rolling(14).mean()
                rs = gain / loss
                data['RSI'] = 100 - (100 / (1 + rs))
                
                latest = data.iloc[-1]
                prev = data.iloc[-2]
                signal = "🟢 STRONG BUY" if latest['Close'] > latest['EMA20'] and latest['RSI'] < 70 else "🔴 SELL"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Price", f"₹{latest['Close']:.0f}", f"{((latest['Close']-prev['Close'])/prev['Close']*100):+.1f}%")
                    st.metric("RSI", f"{latest['RSI']:.1f}", "50.0")
                with col2:
                    st.metric("Signal", signal)
                    st.metric("Volume", f"{latest['Volume']/1e6:.1f}M")
                
                st.line_chart(data[['Close', 'EMA20']][-20:])
                st.balloons()
        except Exception as e:
            st.error(f"❌ Error: {str(e)[:100]} Try TCS.NS or check NSE holiday.")

st.caption("Daily signals for NSE stocks | No API keys needed!")            

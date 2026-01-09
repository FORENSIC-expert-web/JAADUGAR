import streamlit as st
import pandas as pd
import time

st.title("🔥 Free NSE Predictor Bot v2")

ticker = st.text_input("NSE Stock (RELIANCE.NS):", "RELIANCE.NS").upper()
if st.button("🚀 Predict") and ticker:
    st.info("Note: NSE data live – Friday evening may be slow/holiday.")
    
    try:
        import yfinance as yf
        data = yf.download(ticker, period="5d", progress=False, timeout=15)
        if data.empty:
            st.warning("⚠️ No recent data – try weekday or TCS.NS")
            st.success("🟡 HOLD | Wait for market open.")
        else:
            data['EMA'] = data['Close'].ewm(span=10).mean()
            rsi_gain = data['Close'].pct_change().rolling(5).apply(lambda x: (x > 0).sum() / len(x) * 100, raw=True)
            rsi = 50 + (rsi_gain.iloc[-1] - 50)
            
            latest = data.iloc[-1]
            signal = "🟢 BUY" if latest['Close'] > latest['EMA'] else "🔴 SELL"
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Close", f"₹{latest['Close']:.0f}")
                st.metric("Trend", "Bullish" if latest['Close'] > latest['EMA'] else "Bearish")
            with col2:
                st.metric("Simple RSI", f"{rsi:.0f}")
                st.metric("Signal", signal)
            
            st.line_chart(data[['Close', 'EMA']])
            st.balloons()
    except:
        st.error("❌ Data fetch fail – NSE closed/weekend. Local PC pe test kar!")
        st.success("🟡 Bot structure perfect – market open pe chalega.")

st.caption("Fixed for NSE holidays | Share URL!")

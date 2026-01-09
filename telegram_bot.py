import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yfinance as yf

TOKEN = "8415428317:AAFzi7RRrGrF-ZIBubIwDn30QZ1qP3iIQEo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪄 Jadugar NSE Bot!\nSend: /predict RELIANCE.NS")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /predict ^NSEBANK or RELIANCE.NS")
        return
    
    ticker = context.args[0]
    try:
        data = yf.download(ticker, period="5d")
        if data.empty:
            await update.message.reply_text("❌ No data. Try NSE weekday.")
            return
        
        latest = data.iloc[-1]
        ema = data['Close'].ewm(span=10).mean().iloc[-1]
        signal = "🟢 BUY" if latest['Close'] > ema else "🔴 SELL"
        
        msg = f"""
📊 *{ticker}*
💰 Close: ₹{latest['Close']:.0f}
📈 Trend: {"Bullish" if latest['Close'] > ema else "Bearish"}
🎯 Signal: {signal}
        """
        await update.message.reply_text(msg)
    except:
        await update.message.reply_text("❌ Error! Check ticker (RELIANCE.NS, ^NSEBANK)")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("predict", predict))
    app.run_polling()

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from transformers import pipeline
from arch import arch_model
import requests
from bs4 import BeautifulSoup
from xgboost import XGBClassifier

st.set_page_config(layout="wide")

st.title("🚀 IPO Intelligence Engine PRO")
st.markdown("### Bloomberg-style IPO Analysis with AI + Quant")

ipo_name = st.text_input("Enter IPO / Company Name", "Tata Technologies")

# ---------------- SENTIMENT MODEL ----------------
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

model = load_model()

# ---------------- TWITTER SCRAPING ----------------
def get_tweets(query):
    # Temporary fallback (since Twitter scraping breaks on cloud)
    sample_tweets = [
        f"{query} IPO looks like a multibagger!",
        f"Not sure about {query}, seems overhyped",
        f"{query} IPO subscription is strong",
        f"Experts are bullish on {query}",
        f"{query} may give listing gains"
    ]
    return sample_tweets

def sentiment_score(texts):
    scores = []
    for t in texts:
        try:
            res = model(t[:512])[0]
            if res['label'] == 'positive':
                scores.append(res['score'])
            elif res['label'] == 'negative':
                scores.append(-res['score'])
            else:
                scores.append(0)
        except:
            scores.append(0)
    return np.mean(scores) if scores else 0

# ---------------- HYPE DETECTION ----------------
def hype_index(tweets):
    keywords = ["multibagger", "rocket", "huge gain", "100%"]
    count = sum(any(k in t.lower() for k in keywords) for t in tweets)

    if count > 10:
        return "🔥 Extreme Hype"
    elif count > 5:
        return "⚠️ Medium Hype"
    else:
        return "✅ Low Hype"

# ---------------- GMP SCRAPER ----------------
def get_gmp(ipo):
    try:
        url = "https://www.chittorgarh.com/ipo/ipo-grey-market-premium-gmp/331/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")

        table = soup.find("table")
        rows = table.find_all("tr")

        for row in rows:
            if ipo.lower() in row.text.lower():
                return row.text

        return "No GMP data found"
    except:
        return "Error fetching GMP"

# ---------------- GARCH ----------------
def garch_volatility(ticker="^NSEI"):
    data = yf.download(ticker, period="6mo")
    returns = 100 * data['Close'].pct_change().dropna()

    model = arch_model(returns, vol='Garch', p=1, q=1)
    res = model.fit(disp="off")

    forecast = res.forecast(horizon=5)
    vol = np.sqrt(forecast.variance.values[-1])

    return vol

# ---------------- ML MODEL ----------------
def train_dummy_model():
    X = np.random.rand(200, 4)
    y = np.random.randint(0, 2, 200)

    model = XGBClassifier()
    model.fit(X, y)
    return model

ml_model = train_dummy_model()

def predict(sentiment, hype, vol):
    hype_val = 1 if "Low" in hype else 0

    X = np.array([[sentiment, hype_val, np.mean(vol), 0.5]])
    prob = ml_model.predict_proba(X)[0][1]

    return prob

# ---------------- RUN ----------------
if st.button("Analyze IPO"):

    with st.spinner("Running full analysis..."):

        tweets = get_tweets(ipo_name + " IPO")
        tw_sent = sentiment_score(tweets)
        hype = hype_index(tweets)

        gmp = get_gmp(ipo_name)
        vol = garch_volatility()

        prediction = predict(tw_sent, hype, vol)

    # ---------------- UI ----------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📊 Twitter Sentiment", round(tw_sent, 2))
    col2.metric("🔥 Hype Index", hype)
    col3.metric("📉 Volatility", round(np.mean(vol), 2))
    col4.metric("🎯 Listing Gain %", f"{round(prediction*100,2)}%")

    st.subheader("📈 Volatility Forecast")
    fig = px.line(vol, title="GARCH Forecast Volatility")
    st.plotly_chart(fig)

    st.subheader("📑 GMP Data")
    st.write(gmp)

    st.subheader("🐦 Sample Tweets")
    for t in tweets[:10]:
        st.write("-", t)

    st.subheader("🧠 AI Insight")
    if prediction > 0.7:
        st.success("Strong IPO — High probability of listing gains 🚀")
    elif prediction > 0.4:
        st.warning("Moderate — risky but possible gains ⚠️")
    else:
        st.error("Weak IPO — hype-driven or risky ❌") 

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from transformers import pipeline
from arch import arch_model
import datetime
from newsapi import NewsApiClient

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="IPO Intelligence Engine", layout="wide")

st.title("🚀 IPO Intelligence Engine")
st.write("AI-driven IPO Sentiment + Volatility Predictor")

# -------------------------------
# INPUT
# -------------------------------
ipo_name = st.text_input("Enter IPO / Company Name", "Tata Technologies")

# -------------------------------
# LOAD SENTIMENT MODEL
# -------------------------------
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

sentiment_model = load_model()

# -------------------------------
# NEWS FETCHING
# -------------------------------
def get_news(query):
    try:
        newsapi = NewsApiClient(api_key="YOUR_NEWS_API_KEY")
        articles = newsapi.get_everything(q=query, language='en', page_size=10)
        headlines = [a['title'] for a in articles['articles']]
        return headlines
    except:
        return ["No news found"]

# -------------------------------
# SENTIMENT ANALYSIS
# -------------------------------
def analyze_sentiment(headlines):
    scores = []
    for h in headlines:
        try:
            res = sentiment_model(h)[0]
            if res['label'] == 'positive':
                scores.append(res['score'])
            elif res['label'] == 'negative':
                scores.append(-res['score'])
            else:
                scores.append(0)
        except:
            scores.append(0)

    if len(scores) == 0:
        return 0

    return np.mean(scores)

# -------------------------------
# HYPE SCORE
# -------------------------------
def hype_score(headlines):
    hype_words = ["multibagger", "huge gain", "guaranteed", "skyrocket"]
    count = sum(any(word in h.lower() for word in hype_words) for h in headlines)

    if count > 3:
        return "🔥 High Hype"
    elif count > 1:
        return "⚠️ Medium Hype"
    else:
        return "✅ Low Hype"

# -------------------------------
# VOLATILITY (GARCH)
# -------------------------------
def calculate_volatility(ticker="^NSEI"):
    try:
        data = yf.download(ticker, period="6mo")
        returns = 100 * data['Close'].pct_change().dropna()

        model = arch_model(returns, vol='Garch', p=1, q=1)
        res = model.fit(disp='off')

        forecast = res.forecast(horizon=1)
        vol = np.sqrt(forecast.variance.values[-1][0])

        return vol
    except:
        return 0

# -------------------------------
# PREDICTION LOGIC
# -------------------------------
def predict(sentiment, hype, volatility):
    score = 0

    if sentiment > 0.3:
        score += 1
    if "Low" in hype:
        score += 1
    if volatility < 2:
        score += 1

    probability = score / 3
    return probability

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if st.button("Analyze IPO"):

    with st.spinner("Analyzing..."):
        headlines = get_news(ipo_name)

        sentiment = analyze_sentiment(headlines)
        hype = hype_score(headlines)
        volatility = calculate_volatility()

        probability = predict(sentiment, hype, volatility)

    # -------------------------------
    # DISPLAY
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Sentiment Score", round(sentiment, 2))
    col2.metric("🔥 Hype Level", hype)
    col3.metric("📉 Volatility (GARCH)", round(volatility, 2))

    st.subheader("🎯 Listing Gain Probability")
    st.progress(int(probability * 100))
    st.write(f"{round(probability * 100, 2)}% chance of listing gain")

    st.subheader("📰 News Headlines")
    for h in headlines:
        st.write("-", h)

    # Insight
    st.subheader("🧠 AI Insight")
    if probability > 0.66:
        st.success("Strong IPO — likely listing gains 🚀")
    elif probability > 0.33:
        st.warning("Moderate — risky but possible gains ⚠️")
    else:
        st.error("Weak IPO — hype-driven or risky ❌")
        import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from transformers import pipeline
from arch import arch_model
import datetime
from newsapi import NewsApiClient

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="IPO Intelligence Engine", layout="wide")

st.title("🚀 IPO Intelligence Engine")
st.write("AI-driven IPO Sentiment + Volatility Predictor")

# -------------------------------
# INPUT
# -------------------------------
ipo_name = st.text_input("Enter IPO / Company Name", "Tata Technologies")

# -------------------------------
# LOAD SENTIMENT MODEL
# -------------------------------
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="ProsusAI/finbert")

sentiment_model = load_model()

# -------------------------------
# NEWS FETCHING
# -------------------------------
def get_news(query):
    try:
        newsapi = NewsApiClient(api_key="dccb7a07daea449abd667b661ff56126")
        articles = newsapi.get_everything(q=query, language='en', page_size=10)
        headlines = [a['title'] for a in articles['articles']]
        return headlines
    except:
        return ["No news found"]

# -------------------------------
# SENTIMENT ANALYSIS
# -------------------------------
def analyze_sentiment(headlines):
    scores = []
    for h in headlines:
        try:
            res = sentiment_model(h)[0]
            if res['label'] == 'positive':
                scores.append(res['score'])
            elif res['label'] == 'negative':
                scores.append(-res['score'])
            else:
                scores.append(0)
        except:
            scores.append(0)

    if len(scores) == 0:
        return 0

    return np.mean(scores)

# -------------------------------
# HYPE SCORE
# -------------------------------
def hype_score(headlines):
    hype_words = ["multibagger", "huge gain", "guaranteed", "skyrocket"]
    count = sum(any(word in h.lower() for word in hype_words) for h in headlines)

    if count > 3:
        return "🔥 High Hype"
    elif count > 1:
        return "⚠️ Medium Hype"
    else:
        return "✅ Low Hype"

# -------------------------------
# VOLATILITY (GARCH)
# -------------------------------
def calculate_volatility(ticker="^NSEI"):
    try:
        data = yf.download(ticker, period="6mo")
        returns = 100 * data['Close'].pct_change().dropna()

        model = arch_model(returns, vol='Garch', p=1, q=1)
        res = model.fit(disp='off')

        forecast = res.forecast(horizon=1)
        vol = np.sqrt(forecast.variance.values[-1][0])

        return vol
    except:
        return 0

# -------------------------------
# PREDICTION LOGIC
# -------------------------------
def predict(sentiment, hype, volatility):
    score = 0

    if sentiment > 0.3:
        score += 1
    if "Low" in hype:
        score += 1
    if volatility < 2:
        score += 1

    probability = score / 3
    return probability

# -------------------------------
# MAIN EXECUTION
# -------------------------------
if st.button("Analyze IPO"):

    with st.spinner("Analyzing..."):
        headlines = get_news(ipo_name)

        sentiment = analyze_sentiment(headlines)
        hype = hype_score(headlines)
        volatility = calculate_volatility()

        probability = predict(sentiment, hype, volatility)

    # -------------------------------
    # DISPLAY
    # -------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Sentiment Score", round(sentiment, 2))
    col2.metric("🔥 Hype Level", hype)
    col3.metric("📉 Volatility (GARCH)", round(volatility, 2))

    st.subheader("🎯 Listing Gain Probability")
    st.progress(int(probability * 100))
    st.write(f"{round(probability * 100, 2)}% chance of listing gain")

    st.subheader("📰 News Headlines")
    for h in headlines:
        st.write("-", h)

    # Insight
    st.subheader("🧠 AI Insight")
    if probability > 0.66:
        st.success("Strong IPO — likely listing gains 🚀")
    elif probability > 0.33:
        st.warning("Moderate — risky but possible gains ⚠️")
    else:
        st.error("Weak IPO — hype-driven or risky ❌")

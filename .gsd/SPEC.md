# SPEC.md — Project Specification

> **Status**: `FINALIZED`
> **Project**: XprojectX — US Stock Price Movement Predictor

## Vision

A web application that predicts US stock price movement direction (up or down) using machine learning. Users enter any US stock ticker, choose a prediction timeframe (next trading day or next week), and receive a directional prediction powered by a scikit-learn model trained on historical data from yfinance. The app includes a Gemini-powered AI chatbot that helps beginner investors learn stock market concepts through natural conversation. The model can be manually retrained on fresh data via a single button click the model improves as more recent data becomes available.

## Goals

1. **Accurate directional prediction** — Train an ML model on historical stock data (technical indicators, price patterns) to predict whether a given US stock will move up or down over the next trading day or next week
2. **Clean, intuitive dashboard** — Display predictions with confidence scores, historical accuracy, and supporting data visualizations on a modern, responsive UI
3. **Beginner education chatbot** — Provide an AI-powered conversational assistant (Gemini free tier) that answers stock market questions in plain language
4. **Manual model retraining** — Allow users to retrain the prediction model on the latest available data with a single button click
5. **Deployment-ready architecture** — Structure the codebase so it can be deployed to a cloud provider later without architectural changes

## Non-Goals (Out of Scope)

- No real trading or brokerage integration
- No portfolio tracking or watchlists
- No user accounts or authentication
- No automatic/scheduled model retraining
- No real-time streaming data (uses end-of-day data from yfinance)
- No financial advice — predictions are educational, not investment recommendations
- No mobile native app (responsive web only)

## Users

**Primary user**: Beginner to intermediate investor who wants to:
- Get a quick directional signal on any US stock before making their own decision
- Learn stock market concepts through conversation with an AI tutor
- Understand how ML can be applied to financial data

**Usage pattern**: Visit the site → enter a ticker → view prediction → optionally chat with the education bot → leave. No account required, no persistent state per user.

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | React (Vite) | Fast dev experience, component-based UI |
| Backend | FastAPI (Python) | Async, fast, great for ML serving |
| ML | scikit-learn | Simple, well-documented, sufficient for classification |
| Data | yfinance | Free historical US stock data, no API key needed |
| Chatbot | Google Gemini API (free tier) | Free, capable, good for educational Q&A |
| Styling | Vanilla CSS | Full control, no framework dependencies |

## Constraints

- **Cost**: Zero — all APIs and data sources must be free tier
- **Data source**: yfinance only (free, no API key, but rate-limited and end-of-day only)
- **ML complexity**: scikit-learn classifiers only (no deep learning frameworks)
- **Deployment**: Runs locally for now; code must be structured for future cloud deployment
- **Gemini API**: Requires a free API key from Google AI Studio
- **Disclaimer**: Must include a visible disclaimer that predictions are not financial advice

## Success Criteria

- [ ] User can enter any valid US stock ticker and receive an up/down prediction
- [ ] User can choose between "next trading day" and "next week" prediction timeframes
- [ ] Predictions display with a confidence score and supporting chart
- [ ] Education chatbot answers beginner stock market questions accurately
- [ ] Manual retrain button fetches fresh data and retrains the model
- [ ] Dashboard loads in under 3 seconds on localhost
- [ ] Application runs locally with a single command (or minimal setup)
- [ ] Codebase is structured for future cloud deployment

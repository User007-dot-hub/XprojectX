# REQUIREMENTS.md

## Functional Requirements

| ID | Requirement | Source | Status |
|----|-------------|--------|--------|
| REQ-01 | Accept any valid US stock ticker symbol as input | SPEC Goal 1 | Pending |
| REQ-02 | Validate ticker symbol against yfinance before processing | SPEC Goal 1 | Pending |
| REQ-03 | Fetch historical stock data (min 2 years) via yfinance | SPEC Goal 1 | Pending |
| REQ-04 | Compute technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands, volume changes) as ML features | SPEC Goal 1 | Pending |
| REQ-05 | Train a scikit-learn classifier to predict up/down movement | SPEC Goal 1 | Pending |
| REQ-06 | Support two prediction timeframes: next trading day and next week | SPEC Goal 1 | Pending |
| REQ-07 | Return prediction result with confidence score (probability) | SPEC Goal 2 | Pending |
| REQ-08 | Display interactive price chart with historical data | SPEC Goal 2 | Pending |
| REQ-09 | Show model accuracy metrics (historical backtest accuracy) | SPEC Goal 2 | Pending |
| REQ-10 | Responsive dashboard layout that works on desktop and tablet | SPEC Goal 2 | Pending |
| REQ-11 | AI chatbot answers stock market questions using Gemini API | SPEC Goal 3 | Pending |
| REQ-12 | Chatbot restricts responses to stock/finance education topics | SPEC Goal 3 | Pending |
| REQ-13 | Manual retrain button triggers fresh data fetch + model retraining | SPEC Goal 4 | Pending |
| REQ-14 | Show retraining progress/status to the user | SPEC Goal 4 | Pending |
| REQ-15 | Display disclaimer that predictions are not financial advice | SPEC Constraints | Pending |

## Non-Functional Requirements

| ID | Requirement | Source | Status |
|----|-------------|--------|--------|
| NFR-01 | Dashboard loads in under 3 seconds on localhost | SPEC Success Criteria | Pending |
| NFR-02 | Prediction API responds in under 10 seconds (includes data fetch + inference) | SPEC Goal 2 | Pending |
| NFR-03 | Application starts with minimal setup commands | SPEC Success Criteria | Pending |
| NFR-04 | Code structured for future cloud deployment (env vars, config separation) | SPEC Goal 5 | Pending |
| NFR-05 | All data sources and APIs are free tier (zero cost) | SPEC Constraints | Pending |

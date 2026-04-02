# ROADMAP.md

> **Current Phase**: Not started
> **Milestone**: v1.0

## Must-Haves (from SPEC)

- [ ] Stock ticker input → up/down prediction with confidence score
- [ ] Two timeframes: next trading day, next week
- [ ] Price chart with historical data
- [ ] Gemini-powered education chatbot
- [ ] Manual retrain button
- [ ] Financial advice disclaimer

## Phases

### Phase 1: Backend Foundation & ML Pipeline
**Status**: ⬜ Not Started
**Objective**: Stand up the FastAPI backend with data fetching via yfinance, feature engineering (technical indicators), and a trained scikit-learn classifier that returns up/down predictions with confidence scores.
**Requirements**: REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, REQ-07
**Deliverable**: API endpoint `POST /api/predict` that accepts a ticker + timeframe and returns a prediction JSON response.

### Phase 2: Frontend Dashboard & Visualization
**Status**: ✅ Complete
**Objective**: Build the React frontend with a modern, responsive dashboard. Includes ticker input, timeframe selector, prediction display with confidence, interactive price chart, and model accuracy metrics.
**Requirements**: REQ-08, REQ-09, REQ-10, REQ-15, NFR-01
**Deliverable**: Fully functional prediction UI connected to the backend API.

### Phase 3: Education Chatbot
**Status**: ⬜ Not Started
**Objective**: Integrate the Gemini API to power a conversational education chatbot. Users can ask stock market questions and receive beginner-friendly answers. Chatbot is scoped to finance/investing topics only.
**Requirements**: REQ-11, REQ-12
**Deliverable**: Chat panel in the dashboard with streaming AI responses.

### Phase 4: Retraining & Polish
**Status**: ⬜ Not Started
**Objective**: Add manual model retraining functionality, progress indicators, error handling, loading states, and final UI polish. Ensure the app is deployment-ready with proper configuration separation.
**Requirements**: REQ-13, REQ-14, NFR-02, NFR-03, NFR-04, NFR-05
**Deliverable**: Production-quality application running locally with all features complete.

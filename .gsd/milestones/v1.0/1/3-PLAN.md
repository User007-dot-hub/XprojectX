---
phase: 1
plan: 3
wave: 2
---

# Plan 1.3: ML Model & Prediction Endpoint

## Objective
Create the ML training pipeline and the FastAPI prediction endpoint. This connects data (Plan 1.1) and features (Plan 1.2) into a working prediction API. By the end, `POST /api/predict` accepts a ticker + timeframe and returns an up/down prediction with confidence.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- backend/app/services/data_service.py (Plan 1.1)
- backend/app/services/feature_service.py (Plan 1.2)

## Tasks

<task type="auto">
  <name>Create ML model service</name>
  <files>
    backend/app/services/ml_service.py
  </files>
  <action>
    1. Create `backend/app/services/ml_service.py`:
       - Class `MLService` with methods:

         a. `__init__(self, model_dir: str = "models")`
            - Creates model_dir if it doesn't exist
            - Stores model_dir path
            - Initializes model and scaler as None

         b. `train(self, ticker: str, timeframe: str) -> dict`
            - Fetches 2 years of data using DataService
            - Computes features using FeatureService
            - Creates target using FeatureService.create_target(timeframe)
            - Drops rows where target is NaN (last rows with no future data)
            - Splits into features (X) and target (y)
            - Feature columns = all columns except OHLCV and target
            - Train/test split: 80/20, shuffle=False (time series — no data leakage)
              WHY shuffle=False: Stock data is sequential. Shuffling would leak future information into training.
            - StandardScaler on features (fit on train, transform on both)
            - Train a RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
              WHY class_weight='balanced': Handles slight class imbalance in up/down labels
            - Evaluate on test set: accuracy, precision, recall
            - Save model + scaler + feature columns using joblib to: {model_dir}/{ticker}_{timeframe}_model.joblib, {model_dir}/{ticker}_{timeframe}_scaler.joblib, {model_dir}/{ticker}_{timeframe}_features.joblib
            - Return dict: {"accuracy": float, "precision": float, "recall": float, "train_size": int, "test_size": int}

         c. `predict(self, ticker: str, timeframe: str) -> dict`
            - Load saved model, scaler, and feature columns from model_dir
            - If no saved model exists, call self.train(ticker, timeframe) first
            - Fetch recent data (6 months) using DataService
            - Compute features using FeatureService
            - Take the LAST row (most recent trading day) as the prediction input
            - Scale features using saved scaler
            - Predict class and probability using model.predict and model.predict_proba
            - Return dict: {"prediction": "up" or "down", "confidence": float (max probability), "model_accuracy": float}

         d. `get_model_path(self, ticker: str, timeframe: str) -> str`
            - Returns the path where model would be saved
            - Used to check if model exists

    AVOID:
    - Do NOT use deep learning (TensorFlow, PyTorch) — scikit-learn only
      WHY: Overkill for binary classification with ~500 samples, and adds massive dependencies
    - Do NOT shuffle the train/test split
      WHY: Time series data — shuffling creates data leakage
    - Do NOT cache the model in memory across requests (load from disk each time for simplicity)
      WHY: Keeps the service stateless and avoids memory issues with many tickers
  </action>
  <verify>
    cd backend && python -c "
from app.services.ml_service import MLService
ml = MLService()
metrics = ml.train('AAPL', '1d')
print(f'Training metrics: {metrics}')
result = ml.predict('AAPL', '1d')
print(f'Prediction: {result}')
assert result['prediction'] in ['up', 'down']
assert 0 <= result['confidence'] <= 1
print('ML Service OK')
"
  </verify>
  <done>
    - MLService.train('AAPL', '1d') completes without errors and returns accuracy metrics
    - MLService.predict('AAPL', '1d') returns prediction with confidence between 0 and 1
    - Model files are saved to disk (models/ directory)
    - Both "1d" and "1w" timeframes work
  </done>
</task>

<task type="auto">
  <name>Create prediction API endpoint</name>
  <files>
    backend/app/routers/__init__.py
    backend/app/routers/prediction.py
    backend/app/main.py (update — uncomment router import)
  </files>
  <action>
    1. Create `backend/app/routers/__init__.py` — empty file

    2. Create `backend/app/routers/prediction.py`:
       - FastAPI APIRouter with prefix="/api" and tags=["prediction"]
       - Endpoints:

         a. `POST /api/predict`
            - Accepts PredictionRequest (ticker, timeframe)
            - Validates ticker using DataService.validate_ticker()
            - If invalid ticker: raise HTTPException(400, "Invalid ticker symbol")
            - Calls MLService.predict(ticker, timeframe)
            - Fetches historical prices (6 months) for chart data using DataService
            - Gets current price using DataService.get_current_price()
            - Returns PredictionResponse with all fields populated
            - Wraps in try/except for yfinance network errors → 503, ML errors → 500

         b. `POST /api/retrain`
            - Accepts: ticker (str), timeframe (str)
            - Calls MLService.train(ticker, timeframe)
            - Returns training metrics dict
            - This endpoint will be used by the retrain button in Phase 4

         c. `GET /api/stock/{ticker}`
            - Returns basic stock info: current price, name, last updated
            - Uses yfinance.Ticker(ticker).info
            - Lightweight endpoint for ticker validation in the UI

    3. Update `backend/app/main.py`:
       - Uncomment the prediction router import
       - Add: `app.include_router(prediction.router)`

    AVOID:
    - Do NOT add rate limiting (unnecessary complexity for local use)
    - Do NOT add background tasks for training (keep synchronous for now)
    - Do NOT add WebSocket support (REST is sufficient)
  </action>
  <verify>
    Start FastAPI server and test endpoints:
    1. cd backend && pip install -r requirements.txt
    2. cd backend && uvicorn app.main:app --reload &
    3. curl -X POST http://localhost:8000/api/predict -H "Content-Type: application/json" -d '{"ticker": "AAPL", "timeframe": "1d"}'
    4. curl http://localhost:8000/api/health
    5. curl http://localhost:8000/api/stock/AAPL

    Alternative PowerShell verification:
    cd backend && python -c "
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
r = client.get('/api/health')
print(f'Health: {r.json()}')
r = client.get('/api/stock/AAPL')
print(f'Stock info: {r.status_code}')
print('API endpoints OK')
"
  </verify>
  <done>
    - POST /api/predict returns a valid PredictionResponse JSON
    - POST /api/retrain returns training metrics
    - GET /api/stock/{ticker} returns stock info
    - GET /api/health returns healthy status
    - Invalid ticker returns 400 error
    - All endpoints have proper error handling
  </done>
</task>

## Success Criteria
- [ ] MLService trains a RandomForest model on any US stock ticker
- [ ] MLService returns up/down prediction with confidence score
- [ ] POST /api/predict endpoint works end-to-end (ticker in → prediction out)
- [ ] POST /api/retrain endpoint retrains and returns metrics
- [ ] Model files persist to disk between server restarts
- [ ] Error handling covers invalid tickers and network failures

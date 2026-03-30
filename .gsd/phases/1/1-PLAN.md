---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Project Scaffolding & Data Service

## Objective
Set up the Python backend project structure with FastAPI and create the yfinance data fetching service. This is the foundation everything else builds on — no ML, no features, just clean project structure and reliable data access.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md

## Tasks

<task type="auto">
  <name>Create Python backend project structure</name>
  <files>
    backend/requirements.txt
    backend/app/__init__.py
    backend/app/main.py
    backend/app/config.py
    backend/.env.example
    backend/.gitignore
  </files>
  <action>
    1. Create `backend/requirements.txt` with these exact dependencies:
       - fastapi>=0.104.0
       - uvicorn[standard]>=0.24.0
       - yfinance>=0.2.31
       - scikit-learn>=1.3.0
       - pandas>=2.1.0
       - numpy>=1.26.0
       - python-dotenv>=1.0.0
       - google-generativeai>=0.3.0
       - pydantic>=2.5.0
       - joblib>=1.3.0

    2. Create `backend/app/__init__.py` — empty file

    3. Create `backend/app/config.py`:
       - Use pydantic BaseSettings for configuration
       - Fields: GEMINI_API_KEY (str, default ""), MODEL_DIR (str, default "models"), DATA_CACHE_DIR (str, default "cache"), CORS_ORIGINS (list, default ["http://localhost:5173"])
       - Load from .env file

    4. Create `backend/app/main.py`:
       - FastAPI app instance with title "XprojectX API", description, version "1.0.0"
       - CORS middleware allowing frontend origin (http://localhost:5173)
       - Health check endpoint: GET /api/health → {"status": "healthy", "version": "1.0.0"}
       - Import and include routers (prediction, chat) — stub imports for now, comment them out

    5. Create `backend/.env.example`:
       - GEMINI_API_KEY=your_api_key_here

    6. Create `backend/.gitignore`:
       - __pycache__/, *.pyc, .env, models/, cache/, venv/, .venv/

    AVOID:
    - Do NOT install dependencies yet (that's a separate step)
    - Do NOT create the frontend yet (Phase 2)
    - Do NOT add authentication middleware (out of scope)
  </action>
  <verify>
    cd backend && python -c "from app.config import Settings; s = Settings(); print(f'Config OK: MODEL_DIR={s.MODEL_DIR}')"
  </verify>
  <done>
    - requirements.txt exists with all dependencies listed
    - FastAPI app module imports without errors
    - Config loads with default values
    - .gitignore excludes pycache, .env, models, cache
  </done>
</task>

<task type="auto">
  <name>Create yfinance data fetching service</name>
  <files>
    backend/app/services/__init__.py
    backend/app/services/data_service.py
    backend/app/schemas/__init__.py
    backend/app/schemas/stock.py
  </files>
  <action>
    1. Create `backend/app/schemas/stock.py` — Pydantic models:
       - `StockDataRequest`: ticker (str), period (str, default "2y")
       - `PredictionRequest`: ticker (str), timeframe (Literal["1d", "1w"])
       - `PredictionResponse`: ticker (str), timeframe (str), prediction (Literal["up", "down"]), confidence (float), current_price (float), model_accuracy (float), timestamp (str), historical_prices (list of dicts with date, open, high, low, close, volume)

    2. Create `backend/app/services/data_service.py`:
       - Class `DataService` with methods:
         a. `fetch_stock_data(ticker: str, period: str = "2y") -> pd.DataFrame`
            - Uses yfinance.download() to fetch OHLCV data
            - Validates that ticker returns data (raise ValueError if empty)
            - Returns clean DataFrame with columns: Open, High, Low, Close, Volume
            - Handles yfinance errors gracefully with try/except

         b. `validate_ticker(ticker: str) -> bool`
            - Uses yfinance.Ticker(ticker).info to check if ticker exists
            - Returns True if valid, False otherwise
            - Handles network errors gracefully

         c. `get_current_price(ticker: str) -> float`
            - Returns the most recent closing price
            - Uses yfinance.Ticker(ticker).history(period="1d")

    3. Create `backend/app/services/__init__.py` — empty file
    4. Create `backend/app/schemas/__init__.py` — empty file

    AVOID:
    - Do NOT cache data to disk yet (keep it simple for now)
    - Do NOT add rate limiting (yfinance handles this internally)
    - Do NOT process or transform the data beyond basic cleaning — feature engineering is Plan 1.2
  </action>
  <verify>
    cd backend && python -c "from app.services.data_service import DataService; ds = DataService(); df = ds.fetch_stock_data('AAPL', '1mo'); print(f'Fetched {len(df)} rows for AAPL'); print(df.tail(3))"
  </verify>
  <done>
    - DataService.fetch_stock_data('AAPL') returns a DataFrame with OHLCV columns
    - DataService.validate_ticker('AAPL') returns True
    - DataService.validate_ticker('XYZXYZXYZ123') returns False
    - DataService.get_current_price('AAPL') returns a positive float
  </done>
</task>

## Success Criteria
- [ ] `backend/` directory exists with clean project structure
- [ ] FastAPI app starts without errors: `cd backend && uvicorn app.main:app`
- [ ] GET /api/health returns {"status": "healthy"}
- [ ] DataService successfully fetches AAPL historical data from yfinance
- [ ] Pydantic schemas validate correctly

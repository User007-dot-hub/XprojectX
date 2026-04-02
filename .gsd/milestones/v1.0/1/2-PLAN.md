---
phase: 1
plan: 2
wave: 1
---

# Plan 1.2: Feature Engineering

## Objective
Create the feature engineering pipeline that transforms raw OHLCV data into technical indicators used as ML features. This is the bridge between raw data (Plan 1.1) and the ML model (Plan 1.3).

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md
- backend/app/services/data_service.py (created in Plan 1.1)

## Tasks

<task type="auto">
  <name>Build technical indicator computation module</name>
  <files>
    backend/app/services/feature_service.py
  </files>
  <action>
    1. Create `backend/app/services/feature_service.py`:
       - Class `FeatureService` with methods:

         a. `compute_features(df: pd.DataFrame) -> pd.DataFrame`
            - Takes raw OHLCV DataFrame from DataService
            - Adds all technical indicator columns (calls internal methods below)
            - Drops rows with NaN values (from rolling windows)
            - Returns feature-enriched DataFrame

         b. Internal methods (called by compute_features):

            `_add_sma(df, windows=[5, 10, 20, 50])` — Simple Moving Averages
            - SMA_{window} = Close.rolling(window).mean()
            - Also add SMA ratio features: Close / SMA_{window}

            `_add_ema(df, windows=[12, 26])` — Exponential Moving Averages
            - EMA_{window} = Close.ewm(span=window).mean()

            `_add_rsi(df, window=14)` — Relative Strength Index
            - Calculate price changes (delta)
            - Separate gains and losses
            - RS = avg_gain / avg_loss (rolling 14)
            - RSI = 100 - (100 / (1 + RS))

            `_add_macd(df)` — MACD
            - MACD_line = EMA_12 - EMA_26
            - MACD_signal = MACD_line.ewm(span=9).mean()
            - MACD_histogram = MACD_line - MACD_signal

            `_add_bollinger_bands(df, window=20, num_std=2)` — Bollinger Bands
            - BB_middle = SMA_20
            - BB_upper = SMA_20 + (2 * rolling_std)
            - BB_lower = SMA_20 - (2 * rolling_std)
            - BB_position = (Close - BB_lower) / (BB_upper - BB_lower)

            `_add_volume_features(df)` — Volume indicators
            - Volume_SMA_20 = Volume.rolling(20).mean()
            - Volume_ratio = Volume / Volume_SMA_20

            `_add_price_features(df)` — Price-derived features
            - Daily_return = Close.pct_change()
            - Return_5d = Close.pct_change(5)
            - Return_10d = Close.pct_change(10)
            - High_Low_range = (High - Low) / Close
            - Close_Open_range = (Close - Open) / Open

         c. `create_target(df: pd.DataFrame, timeframe: str) -> pd.Series`
            - If timeframe == "1d": target = 1 if next day's close > today's close, else 0
            - If timeframe == "1w": target = 1 if close 5 trading days ahead > today's close, else 0
            - Returns a binary Series (0 = down, 1 = up)
            - The last row(s) will have NaN target (no future data) — this is expected

    AVOID:
    - Do NOT use any external TA library (ta-lib, ta, etc.) — compute everything with pandas/numpy
      WHY: Avoids complex C dependency installation issues (ta-lib is notoriously hard to install on Windows)
    - Do NOT normalize/scale features here — that's the ML pipeline's job (Plan 1.3)
    - Do NOT drop the target NaN rows here — the ML pipeline handles train/predict split
  </action>
  <verify>
    cd backend && python -c "
from app.services.data_service import DataService
from app.services.feature_service import FeatureService
ds = DataService()
fs = FeatureService()
df = ds.fetch_stock_data('AAPL', '1y')
featured = fs.compute_features(df)
print(f'Raw columns: {len(df.columns)}, Featured columns: {len(featured.columns)}')
print(f'Feature columns: {[c for c in featured.columns if c not in df.columns]}')
print(f'Shape: {featured.shape}')
print(f'NaN count: {featured.isna().sum().sum()}')
target = fs.create_target(featured, '1d')
print(f'Target distribution: {target.value_counts().to_dict()}')
"
  </verify>
  <done>
    - compute_features adds at least 20 new columns to the DataFrame
    - No NaN values remain in the feature DataFrame (after internal dropna)
    - All indicator values are reasonable (RSI between 0-100, BB_position roughly 0-1)
    - create_target returns a binary Series with roughly balanced 0/1 distribution
    - create_target handles both "1d" and "1w" timeframes
  </done>
</task>

## Success Criteria
- [ ] FeatureService.compute_features() transforms raw OHLCV into 20+ feature columns
- [ ] FeatureService.create_target() produces binary labels for both timeframes
- [ ] No NaN values in the feature output
- [ ] All computations use only pandas/numpy (no external TA libraries)

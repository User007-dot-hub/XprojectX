"""Feature engineering service for computing technical indicators."""

import pandas as pd
import numpy as np


class FeatureService:
    """
    Computes technical indicators from raw OHLCV data for ML model features.
    All computations use only pandas/numpy — no external TA libraries.
    """

    def compute_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform raw OHLCV DataFrame into feature-enriched DataFrame.

        Adds 20+ technical indicator columns including:
        - Simple Moving Averages (SMA) and ratios
        - Exponential Moving Averages (EMA)
        - RSI (Relative Strength Index)
        - MACD (Moving Average Convergence Divergence)
        - Bollinger Bands
        - Volume indicators
        - Price-derived features

        Args:
            df: DataFrame with columns: Open, High, Low, Close, Volume

        Returns:
            Feature-enriched DataFrame with NaN rows dropped
        """
        df = df.copy()

        self._add_sma(df)
        self._add_ema(df)
        self._add_rsi(df)
        self._add_macd(df)
        self._add_bollinger_bands(df)
        self._add_volume_features(df)
        self._add_price_features(df)

        # Drop rows with NaN values (from rolling windows)
        df = df.dropna()

        return df

    def create_target(self, df: pd.DataFrame, timeframe: str) -> pd.Series:
        """
        Create binary classification target: 1 = price goes up, 0 = price goes down.

        Args:
            df: Feature-enriched DataFrame (must have 'Close' column)
            timeframe: '1d' for next trading day, '1w' for next week (5 trading days)

        Returns:
            Binary Series (0 = down, 1 = up). Last row(s) will be NaN (no future data).
        """
        if timeframe == "1d":
            # Next day's close vs today's close
            future_close = df["Close"].shift(-1)
        elif timeframe == "1w":
            # Close 5 trading days ahead vs today's close
            future_close = df["Close"].shift(-5)
        else:
            raise ValueError(f"Invalid timeframe: {timeframe}. Must be '1d' or '1w'.")

        target = (future_close > df["Close"]).astype(float)
        # Last row(s) have no future data — mark as NaN
        target[future_close.isna()] = np.nan

        return target

    # ──────────────────────────────────────────────
    # Simple Moving Averages
    # ──────────────────────────────────────────────

    def _add_sma(self, df: pd.DataFrame, windows: list = None) -> None:
        """Add Simple Moving Averages and ratio features."""
        if windows is None:
            windows = [5, 10, 20, 50]

        for w in windows:
            df[f"SMA_{w}"] = df["Close"].rolling(window=w).mean()
            # Ratio: how far is current price from the SMA
            df[f"SMA_{w}_ratio"] = df["Close"] / df[f"SMA_{w}"]

    # ──────────────────────────────────────────────
    # Exponential Moving Averages
    # ──────────────────────────────────────────────

    def _add_ema(self, df: pd.DataFrame, windows: list = None) -> None:
        """Add Exponential Moving Averages."""
        if windows is None:
            windows = [12, 26]

        for w in windows:
            df[f"EMA_{w}"] = df["Close"].ewm(span=w, adjust=False).mean()

    # ──────────────────────────────────────────────
    # Relative Strength Index
    # ──────────────────────────────────────────────

    def _add_rsi(self, df: pd.DataFrame, window: int = 14) -> None:
        """
        Add RSI (Relative Strength Index).
        RSI = 100 - (100 / (1 + RS)) where RS = avg_gain / avg_loss
        """
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = (-delta).where(delta < 0, 0.0)

        avg_gain = gain.rolling(window=window, min_periods=window).mean()
        avg_loss = loss.rolling(window=window, min_periods=window).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)
        df["RSI"] = 100 - (100 / (1 + rs))

    # ──────────────────────────────────────────────
    # MACD
    # ──────────────────────────────────────────────

    def _add_macd(self, df: pd.DataFrame) -> None:
        """
        Add MACD (Moving Average Convergence Divergence).
        MACD Line = EMA_12 - EMA_26
        Signal Line = EMA_9 of MACD Line
        Histogram = MACD Line - Signal Line
        """
        ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
        ema_26 = df["Close"].ewm(span=26, adjust=False).mean()

        df["MACD_line"] = ema_12 - ema_26
        df["MACD_signal"] = df["MACD_line"].ewm(span=9, adjust=False).mean()
        df["MACD_histogram"] = df["MACD_line"] - df["MACD_signal"]

    # ──────────────────────────────────────────────
    # Bollinger Bands
    # ──────────────────────────────────────────────

    def _add_bollinger_bands(self, df: pd.DataFrame, window: int = 20, num_std: int = 2) -> None:
        """
        Add Bollinger Bands.
        Middle = SMA_20
        Upper = SMA_20 + 2 * rolling_std
        Lower = SMA_20 - 2 * rolling_std
        Position = (Close - Lower) / (Upper - Lower)
        """
        rolling_mean = df["Close"].rolling(window=window).mean()
        rolling_std = df["Close"].rolling(window=window).std()

        df["BB_middle"] = rolling_mean
        df["BB_upper"] = rolling_mean + (num_std * rolling_std)
        df["BB_lower"] = rolling_mean - (num_std * rolling_std)

        # Position within the bands (0 = at lower, 1 = at upper)
        band_width = df["BB_upper"] - df["BB_lower"]
        df["BB_position"] = (df["Close"] - df["BB_lower"]) / band_width.replace(0, np.nan)

    # ──────────────────────────────────────────────
    # Volume Features
    # ──────────────────────────────────────────────

    def _add_volume_features(self, df: pd.DataFrame) -> None:
        """Add volume-based indicators."""
        df["Volume_SMA_20"] = df["Volume"].rolling(window=20).mean()
        df["Volume_ratio"] = df["Volume"] / df["Volume_SMA_20"].replace(0, np.nan)

    # ──────────────────────────────────────────────
    # Price-Derived Features
    # ──────────────────────────────────────────────

    def _add_price_features(self, df: pd.DataFrame) -> None:
        """Add price-derived features (returns, ranges)."""
        # Daily return
        df["Daily_return"] = df["Close"].pct_change()

        # Multi-day returns
        df["Return_5d"] = df["Close"].pct_change(5)
        df["Return_10d"] = df["Close"].pct_change(10)

        # Intraday ranges
        df["High_Low_range"] = (df["High"] - df["Low"]) / df["Close"]
        df["Close_Open_range"] = (df["Close"] - df["Open"]) / df["Open"].replace(0, np.nan)

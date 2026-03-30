"""ML service for training and predicting stock price movement direction."""

import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score

from app.services.data_service import DataService
from app.services.feature_service import FeatureService


class MLService:
    """
    Machine learning service for stock price direction prediction.

    Uses a RandomForest classifier trained on technical indicators to predict
    whether a stock will move up or down over a given timeframe.

    Models are saved to disk per ticker/timeframe combination and loaded
    on demand for predictions.
    """

    # Columns that are NOT features (raw OHLCV + intermediate indicator values)
    NON_FEATURE_COLS = [
        "Open", "High", "Low", "Close", "Volume",
        "SMA_5", "SMA_10", "SMA_20", "SMA_50",
        "EMA_12", "EMA_26",
        "BB_middle", "BB_upper", "BB_lower",
        "Volume_SMA_20",
    ]

    def __init__(self, model_dir: str = "models"):
        """
        Initialize the ML service.

        Args:
            model_dir: Directory to save/load trained models
        """
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.data_service = DataService()
        self.feature_service = FeatureService()

    def train(self, ticker: str, timeframe: str) -> dict:
        """
        Train a RandomForest model for a specific ticker and timeframe.

        1. Fetches 2 years of historical data
        2. Computes technical indicator features
        3. Creates binary target (up/down)
        4. Trains with 80/20 time-series split (no shuffle)
        5. Saves model, scaler, and feature list to disk

        Args:
            ticker: US stock ticker symbol
            timeframe: '1d' or '1w'

        Returns:
            Dict with accuracy, precision, recall, train_size, test_size
        """
        # 1. Fetch data
        df = self.data_service.fetch_stock_data(ticker, period="2y")

        # 2. Compute features
        featured_df = self.feature_service.compute_features(df)

        # 3. Create target
        target = self.feature_service.create_target(featured_df, timeframe)

        # 4. Combine and drop NaN targets (last rows with no future data)
        featured_df["target"] = target
        featured_df = featured_df.dropna(subset=["target"])

        # 5. Split features and target
        feature_cols = [
            c for c in featured_df.columns
            if c not in self.NON_FEATURE_COLS and c != "target"
        ]
        X = featured_df[feature_cols].values
        y = featured_df["target"].values

        # 6. Time-series train/test split (NO shuffle — preserves temporal order)
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # 7. Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # 8. Train RandomForest
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
        )
        model.fit(X_train_scaled, y_train)

        # 9. Evaluate
        y_pred = model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)

        # 10. Save model, scaler, and feature columns
        prefix = self._get_prefix(ticker, timeframe)
        joblib.dump(model, os.path.join(self.model_dir, f"{prefix}_model.joblib"))
        joblib.dump(scaler, os.path.join(self.model_dir, f"{prefix}_scaler.joblib"))
        joblib.dump(feature_cols, os.path.join(self.model_dir, f"{prefix}_features.joblib"))
        joblib.dump(accuracy, os.path.join(self.model_dir, f"{prefix}_accuracy.joblib"))

        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "train_size": len(X_train),
            "test_size": len(X_test),
        }

    def predict(self, ticker: str, timeframe: str) -> dict:
        """
        Predict stock movement direction for the given ticker and timeframe.

        If no trained model exists, trains one first.

        Args:
            ticker: US stock ticker symbol
            timeframe: '1d' or '1w'

        Returns:
            Dict with prediction ('up'/'down'), confidence (0-1), model_accuracy
        """
        prefix = self._get_prefix(ticker, timeframe)
        model_path = os.path.join(self.model_dir, f"{prefix}_model.joblib")

        # Train if no model exists
        if not os.path.exists(model_path):
            self.train(ticker, timeframe)

        # Load model, scaler, feature columns, and accuracy
        model = joblib.load(os.path.join(self.model_dir, f"{prefix}_model.joblib"))
        scaler = joblib.load(os.path.join(self.model_dir, f"{prefix}_scaler.joblib"))
        feature_cols = joblib.load(os.path.join(self.model_dir, f"{prefix}_features.joblib"))
        model_accuracy = joblib.load(os.path.join(self.model_dir, f"{prefix}_accuracy.joblib"))

        # Fetch recent data and compute features
        df = self.data_service.fetch_stock_data(ticker, period="6mo")
        featured_df = self.feature_service.compute_features(df)

        # Take the last row (most recent trading day)
        latest = featured_df[feature_cols].iloc[[-1]].values

        # Scale and predict
        latest_scaled = scaler.transform(latest)
        prediction_class = model.predict(latest_scaled)[0]
        prediction_proba = model.predict_proba(latest_scaled)[0]

        # Get confidence (probability of the predicted class)
        confidence = float(np.max(prediction_proba))
        prediction = "up" if prediction_class == 1 else "down"

        return {
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "model_accuracy": round(float(model_accuracy), 4),
        }

    def model_exists(self, ticker: str, timeframe: str) -> bool:
        """Check if a trained model exists for the given ticker/timeframe."""
        prefix = self._get_prefix(ticker, timeframe)
        model_path = os.path.join(self.model_dir, f"{prefix}_model.joblib")
        return os.path.exists(model_path)

    def _get_prefix(self, ticker: str, timeframe: str) -> str:
        """Generate file prefix for model artifacts."""
        return f"{ticker.upper()}_{timeframe}"

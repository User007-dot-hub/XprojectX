"""Pydantic schemas for stock data and predictions."""

from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Dict, Any


class StockDataRequest(BaseModel):
    """Request schema for fetching stock data."""
    ticker: str = Field(..., description="US stock ticker symbol (e.g., AAPL, TSLA)")
    period: str = Field(default="2y", description="Data period (e.g., 1mo, 6mo, 1y, 2y)")


class PredictionRequest(BaseModel):
    """Request schema for stock prediction."""
    ticker: str = Field(..., description="US stock ticker symbol (e.g., AAPL, TSLA)")
    timeframe: Literal["1d", "1w"] = Field(
        ..., description="Prediction timeframe: '1d' for next trading day, '1w' for next week"
    )


class HistoricalPrice(BaseModel):
    """Single historical price data point."""
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class PredictionResponse(BaseModel):
    """Response schema for stock prediction."""
    ticker: str
    timeframe: str
    prediction: Literal["up", "down"]
    confidence: float = Field(..., ge=0, le=1, description="Model confidence (0-1)")
    current_price: float
    model_accuracy: float = Field(..., ge=0, le=1, description="Historical backtest accuracy")
    timestamp: str
    historical_prices: List[HistoricalPrice] = []


class RetrainRequest(BaseModel):
    """Request schema for model retraining."""
    ticker: str = Field(..., description="US stock ticker symbol")
    timeframe: Literal["1d", "1w"] = Field(..., description="Prediction timeframe")


class RetrainResponse(BaseModel):
    """Response schema for model retraining."""
    ticker: str
    timeframe: str
    accuracy: float
    precision: float
    recall: float
    train_size: int
    test_size: int
    message: str = "Model retrained successfully"


class StockInfoResponse(BaseModel):
    """Response schema for basic stock info."""
    ticker: str
    name: str
    current_price: float
    currency: str = "USD"
    exchange: str = ""


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str

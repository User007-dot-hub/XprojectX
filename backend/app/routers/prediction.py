"""Prediction API router — stock price movement predictions."""

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas.stock import (
    PredictionRequest,
    PredictionResponse,
    HistoricalPrice,
    RetrainRequest,
    RetrainResponse,
    StockInfoResponse,
)
from app.services.data_service import DataService
from app.services.ml_service import MLService

router = APIRouter(prefix="/api", tags=["prediction"])

data_service = DataService()
ml_service = MLService()


@router.post("/predict", response_model=PredictionResponse)
async def predict_stock(request: PredictionRequest):
    """
    Predict stock price movement direction (up or down).

    Accepts a ticker symbol and timeframe, returns a prediction with
    confidence score, current price, and historical price data for charting.
    """
    ticker = request.ticker.upper().strip()
    timeframe = request.timeframe

    # Validate ticker
    try:
        if not data_service.validate_ticker(ticker):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ticker symbol: '{ticker}'. Please enter a valid US stock ticker.",
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to validate ticker. Please check your internet connection and try again.",
        )

    # Get prediction
    try:
        result = ml_service.predict(ticker, timeframe)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}. Try retraining the model.",
        )

    # Get current price
    try:
        current_price = data_service.get_current_price(ticker)
    except Exception:
        current_price = 0.0

    # Get historical prices for chart (6 months)
    historical_prices = []
    try:
        hist_df = data_service.fetch_stock_data(ticker, period="6mo")
        for date, row in hist_df.iterrows():
            historical_prices.append(
                HistoricalPrice(
                    date=date.strftime("%Y-%m-%d"),
                    open=round(float(row["Open"]), 2),
                    high=round(float(row["High"]), 2),
                    low=round(float(row["Low"]), 2),
                    close=round(float(row["Close"]), 2),
                    volume=int(row["Volume"]),
                )
            )
    except Exception:
        pass  # Historical data is optional — prediction still works

    return PredictionResponse(
        ticker=ticker,
        timeframe=timeframe,
        prediction=result["prediction"],
        confidence=result["confidence"],
        current_price=round(current_price, 2),
        model_accuracy=result["model_accuracy"],
        timestamp=datetime.now(timezone.utc).isoformat(),
        historical_prices=historical_prices,
    )


@router.post("/retrain", response_model=RetrainResponse)
async def retrain_model(request: RetrainRequest):
    """
    Retrain the ML model for a specific ticker and timeframe.

    Fetches fresh data from yfinance and retrains the RandomForest classifier.
    Returns training metrics including accuracy, precision, and recall.
    """
    ticker = request.ticker.upper().strip()
    timeframe = request.timeframe

    # Validate ticker
    try:
        if not data_service.validate_ticker(ticker):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ticker symbol: '{ticker}'.",
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Unable to validate ticker. Check your connection.",
        )

    # Retrain model
    try:
        metrics = ml_service.train(ticker, timeframe)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Retraining failed: {str(e)}",
        )

    return RetrainResponse(
        ticker=ticker,
        timeframe=timeframe,
        accuracy=metrics["accuracy"],
        precision=metrics["precision"],
        recall=metrics["recall"],
        train_size=metrics["train_size"],
        test_size=metrics["test_size"],
    )


@router.get("/stock/{ticker}", response_model=StockInfoResponse)
async def get_stock_info(ticker: str):
    """
    Get basic stock information for a ticker symbol.

    Returns the stock name, current price, currency, and exchange.
    Useful for ticker validation in the UI.
    """
    ticker = ticker.upper().strip()

    try:
        info = data_service.get_stock_info(ticker)
        return StockInfoResponse(**info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch stock info: {str(e)}",
        )

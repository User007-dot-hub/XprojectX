"""Data service for fetching stock data via yfinance."""

import yfinance as yf
import pandas as pd
from typing import Optional


class DataService:
    """Service for fetching and validating US stock data using yfinance."""

    def fetch_stock_data(self, ticker: str, period: str = "2y") -> pd.DataFrame:
        """
        Fetch historical OHLCV data for a given stock ticker.

        Args:
            ticker: US stock ticker symbol (e.g., 'AAPL', 'TSLA')
            period: Data period - valid values: 1mo, 3mo, 6mo, 1y, 2y, 5y

        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume

        Raises:
            ValueError: If ticker returns no data (invalid ticker or no trading history)
        """
        try:
            df = yf.download(ticker, period=period, progress=False, auto_adjust=True)

            if df.empty:
                raise ValueError(
                    f"No data returned for ticker '{ticker}'. "
                    "Please verify the ticker symbol is valid."
                )

            # Handle multi-level columns from yfinance
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Ensure we have the expected columns
            expected_cols = ["Open", "High", "Low", "Close", "Volume"]
            missing = [c for c in expected_cols if c not in df.columns]
            if missing:
                raise ValueError(
                    f"Missing expected columns: {missing}. Got: {list(df.columns)}"
                )

            # Keep only OHLCV columns and drop any rows with NaN
            df = df[expected_cols].dropna()

            return df

        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to fetch data for '{ticker}': {str(e)}")

    def validate_ticker(self, ticker: str) -> bool:
        """
        Check if a ticker symbol is valid by attempting to fetch its info.

        Args:
            ticker: US stock ticker symbol

        Returns:
            True if valid, False otherwise
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            # Check if we got meaningful data back
            return info is not None and info.get("regularMarketPrice") is not None
        except Exception:
            return False

    def get_current_price(self, ticker: str) -> float:
        """
        Get the most recent closing price for a stock.

        Args:
            ticker: US stock ticker symbol

        Returns:
            Most recent closing price as a float

        Raises:
            ValueError: If unable to fetch current price
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if hist.empty:
                raise ValueError(f"No recent price data for '{ticker}'")
            return float(hist["Close"].iloc[-1])
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Failed to get current price for '{ticker}': {str(e)}")

    def get_stock_info(self, ticker: str) -> dict:
        """
        Get basic stock information.

        Args:
            ticker: US stock ticker symbol

        Returns:
            Dict with name, current_price, currency, exchange
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "ticker": ticker.upper(),
                "name": info.get("shortName", info.get("longName", ticker)),
                "current_price": info.get("regularMarketPrice", 0.0),
                "currency": info.get("currency", "USD"),
                "exchange": info.get("exchange", ""),
            }
        except Exception as e:
            raise ValueError(f"Failed to get info for '{ticker}': {str(e)}")

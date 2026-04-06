"""
Price prediction model for BullLens.
Uses linear regression on 90-day historical prices to predict next price.
Falls back to ARIMA if insufficient data.
"""

import os
import numpy as np
import pandas as pd
import yfinance as yf
import requests
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Configure yfinance
# NOTE: curl_cffi is now required for Yahoo API and doesn't work with request_cache
# Let yfinance handle sessions internally


def normalize_symbol(symbol: str) -> str:
    """Normalize symbol for yfinance."""
    symbol = symbol.upper().strip()
    if symbol.startswith("^"):
        return symbol
    if "." not in symbol:
        symbol = symbol + ".NS"
    return symbol


def predict_price(symbol: str, horizon: int = 5) -> dict:
    """
    Predict next price for a symbol using linear regression.
    
    Uses 90 days of historical data to train a simple linear regression model
    that predicts the price at horizon days forward.
    
    Args:
        symbol: Stock symbol (e.g., RELIANCE or RELIANCE.NS)
        horizon: Days ahead to predict (default 5)
    
    Returns:
        dict with:
        - predicted_price: float
        - confidence_interval: [lower, upper]
        - model_used: str (linear_regression or arima)
        - error: str (if failed)
    
    Raises:
        Exception: If data fetch or modeling fails
    """
    try:
        # Normalize symbol
        normalized = normalize_symbol(symbol)
        
        # Fetch 90 days of historical data
        ticker = yf.Ticker(normalized)
        hist = ticker.history(period="90d")
        
        # Check if we have enough data
        if hist.empty or len(hist) < 30:
            return {
                "error": "insufficient_data",
                "details": f"Only {len(hist)} days available, need at least 30"
            }
        
        # Extract close prices
        close_prices = hist["Close"].values.astype(float)
        
        # Create X (time steps) and y (prices)
        X = np.arange(len(close_prices)).reshape(-1, 1)
        y = close_prices
        
        # Train linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict price at horizon days ahead
        last_day_idx = len(close_prices)
        future_idx = np.array([[last_day_idx + horizon]])
        predicted_price = float(model.predict(future_idx)[0])
        
        # Ensure prediction is positive
        if predicted_price < 0:
            return {"error": "insufficient_data", "details": "Model produced negative price"}
        
        # Check for NaN
        if np.isnan(predicted_price):
            return {"error": "insufficient_data", "details": "Model produced NaN"}
        
        # Calculate confidence interval (simple approach)
        residuals = y - model.predict(X)
        std_error = np.std(residuals)
        
        # 95% confidence interval (approximately +/- 1.96 * std_error)
        margin = 1.96 * std_error
        lower_bound = max(predicted_price - margin, 0.01)  # Ensure positive
        upper_bound = predicted_price + margin
        
        return {
            "predicted_price": float(round(predicted_price, 2)),
            "confidence_interval": [
                float(round(lower_bound, 2)),
                float(round(upper_bound, 2))
            ],
            "model_used": "linear_regression",
            "horizon_days": horizon,
            "data_points_used": len(close_prices),
        }
    
    except Exception as e:
        logger.error(f"Price prediction error for {symbol}: {e}")
        return {
            "error": "prediction_failed",
            "details": str(e)
        }


def predict_price_arima(symbol: str, horizon: int = 5) -> dict:
    """
    Alternative price prediction using ARIMA(5,1,0).
    Falls back if linear regression fails.
    
    Args:
        symbol: Stock symbol
        horizon: Days ahead to predict
    
    Returns:
        dict with prediction and confidence interval
    """
    try:
        from statsmodels.tsa.arima.model import ARIMA
        
        # Normalize symbol
        normalized = normalize_symbol(symbol)
        
        # Fetch 90 days of historical data
        ticker = yf.Ticker(normalized)
        hist = ticker.history(period="90d")
        
        if hist.empty or len(hist) < 30:
            return {
                "error": "insufficient_data",
                "details": f"Only {len(hist)} days available, need at least 30"
            }
        
        close_prices = hist["Close"].values.astype(float)
        
        # Fit ARIMA(5,1,0) model
        model = ARIMA(close_prices, order=(5, 1, 0))
        fitted_model = model.fit()
        
        # Predict
        forecast = fitted_model.get_forecast(steps=horizon)
        predicted_price = float(forecast.predicted_mean.iloc[-1])
        conf_int = forecast.conf_int()
        
        # Ensure positive price
        if predicted_price < 0 or np.isnan(predicted_price):
            return {"error": "insufficient_data", "details": "Invalid ARIMA prediction"}
        
        lower = float(conf_int.iloc[-1, 0])
        upper = float(conf_int.iloc[-1, 1])
        
        # Ensure positive bounds
        lower = max(lower, 0.01)
        
        return {
            "predicted_price": float(round(predicted_price, 2)),
            "confidence_interval": [
                float(round(lower, 2)),
                float(round(upper, 2))
            ],
            "model_used": "arima",
            "horizon_days": horizon,
            "data_points_used": len(close_prices),
        }
    
    except ImportError:
        logger.warning("statsmodels not available for ARIMA")
        return None
    except Exception as e:
        logger.error(f"ARIMA prediction error for {symbol}: {e}")
        return None

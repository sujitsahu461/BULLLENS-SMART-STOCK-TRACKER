"""
Stock data and watchlist routes for BullLens FastAPI backend.

Provides endpoints for:
- GET /stock-data/{symbol} - Historical OHLCV data from yfinance
- GET /watchlist - User's full watchlist with live prices
- POST /add-watchlist - Add stock to watchlist
- DELETE /remove-watchlist/{id} - Remove stock from watchlist
"""

import os
import yfinance as yf
import requests_cache
from fastapi import APIRouter, HTTPException, status, Cookie
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import logging
import pandas as pd

try:
    from ..database import get_db_cursor
except ImportError:  # pragma: no cover - script execution fallback
    from database import get_db_cursor

router = APIRouter()
logger = logging.getLogger(__name__)

# Resolve archive path from environment
ARCHIVE_DIR = os.getenv(
    "ARCHIVE_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "archive"))
)

# Configure yfinance settings
# NOTE: requests_cache doesn't work with curl_cffi (used by yfinance for Yahoo API)
# Let yfinance handle caching internally via requests library
YF_CACHE_EXPIRE = int(os.getenv("YFINANCE_CACHE_EXPIRE", 3600))
YF_TIMEOUT = int(os.getenv("YFINANCE_TIMEOUT", 10))
yf_session = None  # Disabled: curl_cffi doesn't work with request_cache sessions


# ============================================================================
# Pydantic Models
# ============================================================================

class AddWatchlistRequest(BaseModel):
    symbol: str
    company_name: Optional[str] = None
    exchange: Optional[str] = "NSE"


# ============================================================================
# Helper Functions
# ============================================================================

def normalize_symbol(symbol: str) -> str:
    """Normalize symbol for yfinance (append .NS for NSE if not present)."""
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    symbol = symbol.upper().strip()
    if not symbol.endswith(".NS") and not symbol.endswith(".BO"):
        symbol = f"{symbol}.NS"
    return symbol


def get_yfinance_data(symbol: str, period: str = "3mo"):
    """
    Fetch historical OHLCV data from yfinance.
    
    Returns:
        dict with symbol, latest_price, change_pct, and history
    
    Raises:
        HTTPException: If data fetch fails
    """
    try:
        normalized = normalize_symbol(symbol)
        # Don't pass session - yfinance needs curl_cffi and doesn't work with request_cache sessions
        ticker = yf.Ticker(normalized)
        hist = ticker.history(period=period)
        
        # Drop rows missing critical data (e.g., market holidays)
        hist = hist.dropna(subset=['Close', 'Open'])
        
        if hist.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No data found for symbol {symbol}"
            )
        
        # Get latest data
        latest = hist.iloc[-1]
        previous_close = hist.iloc[-2]["Close"] if len(hist) > 1 else latest["Close"]
        
        try:
            change_pct = ((float(latest["Close"]) - float(previous_close)) / float(previous_close) * 100) if float(previous_close) > 0 else 0.0
        except Exception:
            change_pct = 0.0
            
        # Format history
        history = []
        for date, row in hist.iterrows():
            history.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]) if pd.notna(row["Volume"]) else 0,
            })
        
        return {
            "symbol": symbol.upper(),
            "latest_price": round(float(latest["Close"]), 2),
            "change_pct": round(change_pct, 2),
            "history": history
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"yfinance error for {symbol}: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to fetch data for symbol {symbol}: {str(e)}"
        )


# ============================================================================
# Live Market Endpoints
# ============================================================================

@router.get("/stock-data/{symbol}")
async def get_stock_data(symbol: str, period: str = "3mo"):
    """
    Fetch historical OHLCV data for a symbol.
    
    Args:
        symbol: Stock symbol (e.g., RELIANCE, TCS, INFY)
        period: Period string (1mo, 3mo, 6mo, 1y, default 3mo)
    
    Returns:
        Historical OHLCV data with latest price and change percentage
    """
    return get_yfinance_data(symbol, period)


@router.get("/watchlist")
async def get_watchlist(session_user_id: int | None = Cookie(default=None)):
    """
    Get user's watchlist with live prices from yfinance.
    
    Args:
        session_user_id: User ID from session cookie
    
    Returns:
        List of watchlist entries with live price data
    """
    if not session_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        user_id = int(session_user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    
    try:
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT 
                    w.watchlist_id as id,
                    s.symbol,
                    s.company_name,
                    w.added_at
                FROM watchlist w
                JOIN stocks s ON w.stock_id = s.stock_id
                WHERE w.user_id = %s
                ORDER BY w.added_at DESC
            """, (user_id,))
            
            rows = cursor.fetchall()
            
            # Enrich with live data
            result = []
            for row in rows:
                try:
                    yf_data = get_yfinance_data(row["symbol"])
                    row["latest_price"] = yf_data["latest_price"]
                    row["change_pct"] = yf_data["change_pct"]
                    row["domain"] = ""
                except HTTPException:
                    # Fallback to 0 if yfinance fails for this symbol
                    row["latest_price"] = 0
                    row["change_pct"] = 0
                    row["domain"] = ""
                
                result.append(row)
            
            return result
    
    except Exception as e:
        logger.error(f"Watchlist error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch watchlist"
        )


@router.post("/add-watchlist", status_code=status.HTTP_201_CREATED)
async def add_watchlist(request: AddWatchlistRequest, session_user_id: int | None = Cookie(default=None)):
    """
    Add a stock to user's watchlist.
    
    Validates symbol exists on yfinance before inserting.
    
    Args:
        request: AddWatchlistRequest with symbol and optional company_name
        session_user_id: User ID from session cookie
    
    Returns:
        Watchlist entry details with stock_id and watchlist_id
    """
    if not session_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        user_id = int(session_user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    if not request.symbol:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Symbol is required"
        )
    
    symbol = request.symbol.upper().strip()
    company_name = request.company_name or symbol
    
    # Validate symbol exists on yfinance
    try:
        yf_data = get_yfinance_data(symbol)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol {symbol} not found on NSE"
        )
    
    try:
        with get_db_cursor(commit=True) as cursor:
            # Check for duplicate
            cursor.execute(
                "SELECT watchlist_id FROM watchlist WHERE user_id = %s AND stock_id = (SELECT stock_id FROM stocks WHERE symbol = %s)",
                (user_id, symbol)
            )
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"{symbol} is already in your watchlist"
                )
            
            # Insert or get stock
            cursor.execute(
                "SELECT stock_id FROM stocks WHERE symbol = %s",
                (symbol,)
            )
            stock_row = cursor.fetchone()
            
            if not stock_row:
                cursor.execute(
                    "INSERT INTO stocks (symbol, company_name, exchange) VALUES (%s, %s, %s)",
                    (symbol, company_name, request.exchange or "NSE")
                )
                stock_id = cursor.lastrowid
            else:
                stock_id = stock_row["stock_id"]
            
            # Insert watchlist entry
            cursor.execute(
                "INSERT INTO watchlist (user_id, stock_id) VALUES (%s, %s)",
                (user_id, stock_id)
            )
            entry_id = cursor.lastrowid
            
            # Enrich response with live data
            try:
                yf_data = get_yfinance_data(symbol)
                latest_price = yf_data["latest_price"]
                change_pct = yf_data["change_pct"]
            except HTTPException:
                latest_price = 0
                change_pct = 0
            
            return {
                "id": entry_id,
                "symbol": symbol,
                "company_name": company_name,
                "latest_price": latest_price,
                "change_pct": change_pct,
                "domain": ""
            }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Add watchlist error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add to watchlist"
        )


@router.get("/quick-picks")
async def get_quick_picks():
    """
    Fetch current values and percentage changes for major NSE indices.
    
    Returns:
        Dict with index symbols as keys and {current, pct_change, history} as values
    """
    indices = {
        "^NSEI":    "NIFTY 50",
        "^NSEBANK": "BANK NIFTY",
        "^CNXIT":   "NIFTY IT",
        "^CNXFMCG": "NIFTY FMCG",
    }
    result = {}
    for sym in indices:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="5d")
            if hist.empty or len(hist) < 2:
                continue
            current = float(hist["Close"].iloc[-1])
            prev    = float(hist["Close"].iloc[-2])
            pct_change = round((current - prev) / prev * 100, 2) if prev else 0
            history = [round(float(v), 2) for v in hist["Close"].tolist()]
            result[sym] = {
                "name": indices[sym],
                "current": round(current, 2),
                "pct_change": pct_change,
                "history": history,
            }
        except Exception as e:
            logger.warning(f"Could not fetch index {sym}: {e}")
    return result


@router.get("/gainers-losers")
async def get_gainers_losers():
    """
    Return top NSE gainers and losers from a curated list of popular stocks.
    
    Returns:
        Dict with 'gainers' and 'losers' lists
    """
    TRACK_SYMBOLS = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "WIPRO.NS",
        "ICICIBANK.NS", "BAJFINANCE.NS", "HINDUNILVR.NS", "MARUTI.NS",
        "SUNPHARMA.NS", "LT.NS", "KOTAKBANK.NS", "SBIN.NS", "AXISBANK.NS",
        "TATAMOTORS.NS"
    ]
    rows = []
    for sym in TRACK_SYMBOLS:
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="2d")
            if hist.empty or len(hist) < 2:
                continue
            close  = float(hist["Close"].iloc[-1])
            prev   = float(hist["Close"].iloc[-2])
            pct    = round((close - prev) / prev * 100, 2) if prev else 0
            rows.append({
                "stock":      sym.replace(".NS", ""),
                "close":      round(close, 2),
                "change_pct": pct,
            })
        except Exception as e:
            logger.warning(f"Could not fetch {sym}: {e}")

    rows.sort(key=lambda r: r["change_pct"], reverse=True)
    gainers = [r for r in rows if r["change_pct"] >= 0][:5]
    losers  = sorted([r for r in rows if r["change_pct"] < 0], key=lambda r: r["change_pct"])[:5]
    return {"gainers": gainers, "losers": losers}


@router.delete("/remove-watchlist/{watchlist_id}")
async def remove_watchlist(watchlist_id: int, session_user_id: int | None = Cookie(default=None)):
    """
    Remove a stock from user's watchlist.
    
    Verifies row ownership before deleting.
    
    Args:
        watchlist_id: Watchlist entry ID
        session_user_id: User ID from session cookie
    
    Returns:
        Status message
    
    Raises:
        HTTPException 401: Not authenticated
        HTTPException 403: Row belongs to another user
        HTTPException 404: Row not found
    """
    if not session_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        user_id = int(session_user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session"
        )
    
    try:
        with get_db_cursor(commit=True) as cursor:
            # Verify ownership
            cursor.execute(
                "SELECT user_id FROM watchlist WHERE watchlist_id = %s",
                (watchlist_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Watchlist entry not found"
                )
            
            if row["user_id"] != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden: This entry belongs to another user"
                )
            
            # Delete
            cursor.execute(
                "DELETE FROM watchlist WHERE watchlist_id = %s",
                (watchlist_id,)
            )
            
            return {"status": "ok", "message": f"Watchlist entry {watchlist_id} removed"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Watchlist remove error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove from watchlist"
        )

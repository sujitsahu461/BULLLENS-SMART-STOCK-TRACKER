# BullLens Dataset & Scenario Guide

## 📊 DATASETS USED

### 1. **Stock Universe**
- **File**: `archive/Companies_list.csv`
- **Contains**: 1,384 NSE stocks
- **Sample symbols**: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, WIPRO, ADANIPOWER, MARUTI

### 2. **Historical Stock Data**
- **Location**: `archive/HISTORICAL_DATA/HISTORICAL_DATA/`
- **Format**: 1,385 CSV files (one per stock)
- **Each file named**: `{SYMBOL}_data.csv`
- **Columns**: Date, Open, High, Low, Close, Adj_Close, Volume
- **Data span**: 2009 onwards
- **Example**: `archive/HISTORICAL_DATA/HISTORICAL_DATA/RELIANCE_data.csv`

### 3. **Training Data**
- **File**: `archive/stocks_df.csv`
- **Used for**: ML model training (volatility & price prediction)

### 4. **Index Data**
- **Files**: `nse_indexes.csv`, `indexes_df.csv`
- **Used for**: Market overview and index tracking

---

## ✅ SCENARIOS THAT WILL RUN (Success Cases)

### Stock Data Loading
| Scenario | Symbol | Result | Why |
|----------|--------|--------|-----|
| **Valid Stock (Archive)** | RELIANCE | ✅ SUCCESS | Has local CSV data from 2009+ |
| **Valid Stock (API)** | INFY | ✅ SUCCESS | yfinance returns real-time data |
| **Valid Stock (API)** | TCS | ✅ SUCCESS | Yahoo Finance has ticker |
| **Valid Stock (API)** | MARUTI | ✅ SUCCESS | Local CSV + yfinance available |
| **Known NSE Stock** | ADANIPOWER | ✅ SUCCESS | In Companies_list.csv |

### ML Predictions
| Scenario | Requirements | Result | Why |
|----------|--------------|--------|-----|
| **Volatility Predict** | ≥30 days history | ✅ SUCCESS | Sufficient OHLCV data + trained model |
| **Price Predict** | ≥90 days history | ✅ SUCCESS | ML model requires 3+ months |
| **Model Available** | Artifact exists | ✅ SUCCESS | `ml_model/artifacts/vol_model_h5.joblib` loaded |

### Watchlist Operations
| Scenario | Requirements | Result | Why |
|----------|--------------|--------|-----|
| **Add Valid Symbol** | Symbol in list | ✅ SUCCESS | Creates watchlist entry |
| **Load Watchlist** | User authenticated | ✅ SUCCESS | Retrieves stored symbols |
| **Remove from List** | Valid entry ID | ✅ SUCCESS | Deletes watchlist entry |

---

## ❌ SCENARIOS THAT WILL FAIL (Error Cases)

### Stock Data Loading Failures
| Scenario | Symbol | Status | Error Message | Why |
|----------|--------|--------|---------------|-----|
| **Invalid Symbol** | `INVALID_SYM_XYZ` | 🔴 400 | "No data found for symbol INVALID_SYM_XYZ.NS" | Not in NSE, yfinance returns empty |
| **Non-existent Stock** | `NOSUCHSTOCK` | 🔴 400 | "No data found for symbol NOSUCHSTOCK.NS" | No local CSV, yfinance fails |
| **Typo Symbol** | `TCSSS` (typo) | 🔴 400 | "No data found for symbol TCSSS.NS" | Doesn't exist in market |
| **Delisted Stock** | `OLDDELISTED` | 🔴 400 | "No data found for symbol..." | Removed from NSE |
| **Empty Symbol** | `` (blank) | 🔴 400 | "Symbol cannot be empty" | Validation error |

### ML Prediction Failures
| Scenario | Reason | Status | Error Message | Why |
|----------|--------|--------|---------------|-----|
| **Insufficient Data** | <30 days history | 🔴 503 | "insufficient_data: only X days available, need at least 30" | Can't compute volatility |
| **Invalid Symbol** | Not in markets | 🔴 503 | "failed_to_fetch_data: no_history" | No data source |
| **Model Not Trained** | Missing artifact | 🔴 422 | "Model not trained. Train with POST /ml/volatility-train first." | Binary file missing |
| **NaN Features** | Bad data | 🔴 503 | "no_valid_features: all feature values are NaN" | Corrupted OHLCV |

### Data Loading Errors
| Scenario | Cause | Status | Error | Why |
|----------|-------|--------|-------|-----|
| **Offline (No API)** | Network down | 🔴 503 | Falls back to local CSV | yfinance unreachable |
| **CSV Corrupted** | File damaged | 🔴 503 | "failed_to_fetch_data" | Can't parse CSV |
| **Empty DataFrame** | No rows in CSV | 🔴 400 | "No data found for symbol" | File exists but empty |

### Authentication/Permission Failures
| Scenario | Requirement | Status | Error | Why |
|----------|-------------|--------|-------|-----|
| **Not Logged In** | session_user_id | 🔴 401 | "Not authenticated" | Cookie missing |
| **Invalid Session** | Valid session | 🔴 401 | "Invalid session" | Session expired/invalid |

---

## 🧪 QUICK TEST SCENARIOS

### Will Definitely Work ✅
```python
# These symbols have full historical data
symbols_working = [
    "RELIANCE",      # Major - has CSV from 2009
    "TCS",           # Major - has CSV + live API
    "INFY",          # Major - has CSV + live API
    "WIPRO",         # Major - has CSV + live API
    "HDFCBANK",      # Major - has CSV + live API
    "ADANIPOWER",    # Power sector - has CSV + live API
    "MARUTI"         # Auto sector - has CSV + live API
]
```

### Will Definitely Fail ❌
```python
# These symbols don't exist in NSE
symbols_failing = [
    "INVALID_SYM",        # Not a real symbol
    "NOSUCHSTOCK",        # Made up
    "XYZ123",             # Random text
    "BADSTOCK",           # Nonsense
    "THISNEVEREXISTED",   # Never in NSE
    "",                   # Empty string
    "123",                # Numbers only
]
```

### Will Fail for Prediction Only 🔴
```python
# Exist but prediction may fail (insufficient data, etc.)
# New stocks with <30 days of data
# Stocks delisted recently
# Stocks with trading halts (no volume data)
```

---

## 📈 ERROR FLOW DIAGRAM

```
User enters symbol
    ↓
┌─────────────────────────────┐
│ Normalize (add .NS suffix)  │
└──────────┬──────────────────┘
           ↓
        ✓ VALID FORMAT? 
      /           \
    YES           NO → ❌ "Symbol cannot be empty"
    ↓
┌──────────────────────────────┐
│ Try yfinance API             │
└──────────┬───────────────────┘
           ↓
     ✓ DATA FOUND?
    /            \
  YES            NO → Try local CSV
   ↓                      ↓
RETURN DATA          ✓ FOUND?
                    /      \
                  YES      NO → ❌ "No data found for symbol X"
                   ↓
            RETURN DATA

For Predictions:
     ↓
  ✓ ≥30 days?
  /          \
YES          NO → ❌ "insufficient_data: only X days, need 30"
 ↓
✓ Model exists?
/            \
YES          NO → ❌ "Model not trained. Call training endpoint"
 ↓
RUN ML MODEL
```

---

## 🔑 Key Files & Locations

| Component | File Path | Status |
|-----------|-----------|--------|
| Stock List | `archive/Companies_list.csv` | ✅ Available |
| Historical Data | `archive/HISTORICAL_DATA/HISTORICAL_DATA/` | ✅ Available (1,385 files) |
| ML Training Data | `archive/stocks_df.csv` | ✅ Available |
| Volatility Model | `bulllens/ml_model/artifacts/vol_model_h5.joblib` | ✅ Trained |
| Price Model | `bulllens/ml_model/artifacts/` | ✅ Available |
| Data Loading Logic | `bulllens/routes/stock_routes.py` | ✅ Working |
| ML Inference | `bulllens/ml_model/risk_model.py` | ✅ Working |

---

## 💡 Testing Tips

### To Test Success Scenarios
```bash
# Stock data loading (will work)
GET /api/stock-data/RELIANCE.NS
GET /api/stock-data/TCS.NS
GET /api/stock-data/INFY.NS

# Volatility prediction (will work - has trained model)
POST /ml/volatility-predict
Body: {"symbol": "RELIANCE", "horizon": 5}

# Watchlist (will work if authenticated)
GET /api/watchlist
POST /api/add-watchlist {"symbol": "TCS.NS", ...}
```

### To Test Error Scenarios
```bash
# Invalid symbol (will fail)
GET /api/stock-data/NOSUCHSTOCK.NS
→ Returns: 400 - "No data found for symbol NOSUCHSTOCK.NS"

# Invalid prediction symbol (will fail)
POST /ml/volatility-predict
Body: {"symbol": "INVALID_SYM", "horizon": 5}
→ Returns: 503 - "failed_to_fetch_data: no_history"

# Not authenticated (will fail)
GET /api/watchlist
→ Returns: 401 - "Not authenticated"
```

---

## 📋 Summary Table

| Category | Scenario | Status | Reason |
|----------|----------|--------|--------|
| **Data** | 1,384 stocks available | ✅ Available | Companies_list.csv |
| **Data** | Historical data 2009+ | ✅ Available | Full archive |
| **API** | yfinance integration | ✅ Working | Real-time fallback |
| **Cache** | Local CSV fallback | ✅ Working | Offline support |
| **ML** | Volatility model | ✅ Trained | Artifact present |
| **ML** | Price model | ✅ Trained | Artifact present |
| **Error** | Invalid symbols | ❌ Error 400 | Not in NSE |
| **Error** | Insufficient data | ❌ Error 503 | <30 days history |
| **Error** | Not authenticated | ❌ Error 401 | Missing session |

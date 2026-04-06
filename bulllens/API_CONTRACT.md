# BullLens API Contract

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Content-Type:** `application/json`  
**Session Management:** Cookies expire on browser close

---

## 1. Authentication Endpoints

### POST /login
Authenticate user and create session.

**Request:**
```json
{
  "username": "string (required)",
  "password": "string (required)"
}
```

**Response: 200 OK**
```json
{
  "status": "ok",
  "username": "string",
  "user_id": "integer"
}
```

**Response: 401 Unauthorized**
```json
{
  "detail": "Invalid username or password"
}
```

**Session Cookies Set:**
- `session_user_id`: Httponly, expires on browser close
- `session_username`: Accessible to JS, expires on browser close

---

### POST /logout
Clear session cookies.

**Request:** No body

**Response: 200 OK**
```json
{
  "status": "ok",
  "message": "Logged out"
}
```

---

### POST /register
Register a new user account.

**Request:**
```json
{
  "username": "string (required, 2-50 chars)",
  "email": "string (required, valid email)",
  "password": "string (required, min 6 chars)"
}
```

**Response: 201 Created**
```json
{
  "status": "ok",
  "message": "Account created successfully",
  "user_id": "integer",
  "username": "string"
}
```

**Response: 409 Conflict**
```json
{
  "detail": "Username already exists" | "Email already exists"
}
```

---

### GET /me
Get current authenticated user profile.

**Query Parameters:**
- `username`: Retrieved from `session_username` cookie

**Response: 200 OK**
```json
{
  "user_id": "integer",
  "username": "string",
  "email": "string"
}
```

**Response: 401 Unauthorized**
```json
{
  "detail": "Not authenticated"
}
```

---

## 2. Stock Data Endpoints

### GET /api/stock-data/{symbol}
Fetch historical OHLCV data for a symbol.

**Path Parameters:**
- `symbol`: Stock symbol (e.g., `RELIANCE`, `TCS`, `INFY`)

**Query Parameters:**
- `period`: Optional period string (`1mo`, `3mo`, `6mo`, `1y`, default `3mo`)

**Response: 200 OK**
```json
{
  "symbol": "string (uppercase)",
  "latest_price": "number (float, 2 decimals)",
  "change_pct": "number (float, 2 decimals)",
  "history": [
    {
      "date": "string (YYYY-MM-DD)",
      "open": "number (float, 2 decimals)",
      "high": "number (float, 2 decimals)",
      "low": "number (float, 2 decimals)",
      "close": "number (float, 2 decimals)",
      "volume": "integer"
    }
  ]
}
```

**Response: 400 Bad Request**
```json
{
  "detail": "string describing error (e.g., 'No data found for symbol RELIANCE')"
}
```

**Notes:**
- Symbols are normalized (appends `.NS` for NSE unless already present)
- History array sorted chronologically (oldest to newest)
- All prices in INR
- Volume is daily trading volume

---

## 3. Watchlist Endpoints

### GET /api/watchlist
Get user's watchlist with live prices.

**Query Parameters:**
- `user_id`: Required, from session

**Response: 200 OK**
```json
[
  {
    "watchlist_id": "integer",
    "symbol": "string",
    "company_name": "string",
    "latest_price": "number (float, 2 decimals)",
    "change_pct": "number (float, 2 decimals)",
    "added_at": "string (ISO datetime)"
  }
]
```

**Response: 500 Internal Server Error**
```json
{
  "detail": "Failed to fetch watchlist"
}
```

**Notes:**
- Returns empty array if no stocks in watchlist
- `latest_price` and `change_pct` are fetched live from yfinance on each request
- Sorted by `added_at` descending (most recent first)

---

### POST /api/add-watchlist
Add a stock to watchlist.

**Query Parameters:**
- `user_id`: Required, from session

**Request:**
```json
{
  "symbol": "string (required, e.g., 'RELIANCE')",
  "company_name": "string (optional, defaults to symbol)",
  "exchange": "string (optional, defaults to 'NSE')"
}
```

**Response: 201 Created**
```json
{
  "watchlist_id": "integer",
  "stock_id": "integer",
  "symbol": "string",
  "company_name": "string"
}
```

**Response: 400 Bad Request**
```json
{
  "detail": "Symbol {symbol} not found on NSE"
}
```

**Response: 409 Conflict**
```json
{
  "detail": "{symbol} is already in your watchlist"
}
```

**Notes:**
- Validates symbol exists on yfinance before adding
- Prevents duplicate entries per user
- Symbol normalized automatically

---

### DELETE /api/remove-watchlist/{watchlist_id}
Remove stock from watchlist.

**Path Parameters:**
- `watchlist_id`: Watchlist entry ID

**Query Parameters:**
- `user_id`: Required, from session

**Response: 200 OK**
```json
{
  "status": "ok",
  "message": "Watchlist entry {watchlist_id} removed"
}
```

**Response: 403 Forbidden**
```json
{
  "detail": "Forbidden: This entry belongs to another user"
}
```

**Response: 404 Not Found**
```json
{
  "detail": "Watchlist entry not found"
}
```

**Notes:**
- Verifies user ownership before deleting
- Returns 403 if user_id doesn't match

---

## 4. ML Endpoints

### POST /ml/volatility-predict
Predict stock volatility for given horizon.

**Request:**
```json
{
  "symbol": "string (required, e.g., 'RELIANCE')",
  "horizon": "integer (optional, default 5, range 2-60)"
}
```

**Response: 200 OK**
```json
{
  "symbol": "string",
  "horizon": "integer",
  "predicted_volatility": "number (float, 4 decimals)",
  "cv_score": "number (float, 4 decimals)",
  "unit": "percentage"
}
```

**Response: 400 Bad Request**
```json
{
  "detail": "Horizon must be between 2 and 60 days"
}
```

**Response: 422 Unprocessable Entity**
```json
{
  "detail": "Model not trained. Train with POST /ml/volatility-train first."
}
```

**Response: 503 Service Unavailable**
```json
{
  "detail": "string describing data fetch error"
}
```

**Notes:**
- `predicted_volatility` is daily volatility estimate (%)
- `cv_score` is cross-validation MAE from training
- Model must be trained first via the train endpoint
- Features: 10-day log returns, momentum (5/10-day), rolling volatility (5/10/20-day)

---

### POST /ml/volatility-train
Train/retrain volatility model.

**Query Parameters:**
- `horizon`: Optional integer (default 5, range 2-60)

**Response: 200 OK**
```json
{
  "status": "ok",
  "horizon": "integer",
  "metrics": {
    "cv_mae": "number (float)",
    "cv_mae_std": "number (float)",
    "horizon": "integer",
    "features": ["list of feature names"]
  }
}
```

**Response: 400 Bad Request**
```json
{
  "detail": "Horizon must be between 2 and 60 days"
}
```

**Response: 500 Internal Server Error**
```json
{
  "detail": "string describing training error"
}
```

**Notes:**
- Training uses 5-fold time-series cross-validation
- Uses 500 RandomForest estimators, max_depth 10
- Persists model to `ml/artifacts/vol_model_h{horizon}.joblib`
- Takes 10-30 seconds depending on data

---

### POST /ml/price-predict
Predict next stock price.

**Request:**
```json
{
  "symbol": "string (required, e.g., 'RELIANCE')",
  "horizon": "integer (optional, default 5)"
}
```

**Response: 200 OK**
```json
{
  "symbol": "string",
  "predicted_price": "number (float, 2 decimals)",
  "confidence_interval": ["number (lower, 2 decimals)", "number (upper, 2 decimals)"],
  "horizon_days": "integer",
  "model_used": "string ('linear_regression' or 'arima')"
}
```

**Response: 400 Bad Request**
```json
{
  "detail": "insufficient_data" | "prediction_failed error message"
}
```

**Response: 503 Service Unavailable**
```json
{
  "detail": "string describing data fetch or model error"
}
```

**Notes:**
- Uses 90 days of historical data
- Requires minimum 30 data points
- Returns NaN/negative as error (never fabricated values)
- 95% confidence interval based on residual std deviation
- Falls back to ARIMA(5,1,0) if linear regression fails

---

### POST /ml/vision-predict
Run YOLO vision model on image.

**Request (Multipart Form):**
```
file: <binary image file (PNG, JPG)>
```

**OR Request (JSON Base64):**
```json
{
  "image_data": "string (base64 or 'data:image/png;base64,...')"
}
```

**Response: 200 OK**
```json
{
  "status": "ok",
  "detections": "integer (count)",
  "inference_time_ms": "number (float)",
  "detections_list": [
    {
      "label": "string",
      "confidence": "number (float, 0-1)",
      "bbox": {
        "x1": "number (float)",
        "y1": "number (float)",
        "x2": "number (float)",
        "y2": "number (float)"
      }
    }
  ]
}
```

**Response: 400 Bad Request**
```json
{
  "detail": "No image provided. Use 'file' upload or 'image_data' base64."
}
```

```json
{
  "detail": "Invalid base64 image"
}
```

**Response: 413 Payload Too Large**
```json
{
  "detail": "Image too large (max 5MB)"
}
```

**Response: 503 Service Unavailable**
```json
{
  "detail": "YOLO model weights not found. Download with: pip install --upgrade ultralytics && python -c \"from ultralytics import YOLO; YOLO('yolov8n.pt')\""
}
```

**Notes:**
- Accepts multipart file upload OR base64 JSON body (choose one)
- Max file size 5MB
- Returns bounding boxes in pixel coordinates
- `inference_time_ms` includes model load time on first call
- YOLO model: YOLOv8 nano (yolov8n.pt)

---

## 5. Health Check

### GET /health
Check API status.

**Response: 200 OK**
```json
{
  "status": "healthy",
  "service": "BullLens API"
}
```

---

## 6. Root Endpoint

### GET /
Serve index.html or welcome message.

**Response: 200 OK**
- HTML file if `templates/index.html` exists
- Otherwise JSON: `{"status": "ok", "message": "BullLens API is running"}`

---

## Error Response Format

All errors follow this format:

**4xx Client Errors:**
```json
{
  "detail": "string describing error"
}
```

**5xx Server Errors:**
```json
{
  "detail": "string describing error"
}
```

**Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad request (invalid data, missing data, failed validation)
- `401`: Unauthorized (invalid credentials, not authenticated)
- `403`: Forbidden (permission denied, wrong user)
- `404`: Not found
- `409`: Conflict (duplicate entry)
- `413`: Payload too large
- `422`: Unprocessable entity (model not trained, etc.)
- `500`: Internal server error
- `503`: Service unavailable (external service down, model weights missing)

---

## Authentication Flow

1. User calls `POST /login` with credentials
2. Server validates bcrypt password hash
3. Server sets two session cookies:
   - `session_user_id`: Httponly cookie (not accessible to JS)
   - `session_username`: Regular cookie (accessible to JS for UI display)
4. Both cookies expire on browser close (no max_age set)
5. Subsequent requests include these cookies automatically
6. Extract `user_id` and `username` from cookies on server side

---

## Configuration via .env

```
UVICORN_ENV=development|production
DEBUG=True|False
SECRET_KEY=<your-secret>
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=bulllens_db
DEMO_USERNAME=demo
DEMO_PASSWORD=demo1234
ML_ARTIFACTS_DIR=ml/artifacts
YFINANCE_CACHE_EXPIRE=3600
```

---

## Database Schema

```sql
-- Users
CREATE TABLE users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Stocks
CREATE TABLE stocks (
  stock_id INT PRIMARY KEY AUTO_INCREMENT,
  symbol VARCHAR(30) UNIQUE NOT NULL,
  company_name VARCHAR(150) NOT NULL,
  exchange VARCHAR(30) DEFAULT 'NSE',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Watchlist
CREATE TABLE watchlist (
  watchlist_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  stock_id INT NOT NULL,
  added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(user_id, stock_id),
  FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
  FOREIGN KEY(stock_id) REFERENCES stocks(stock_id) ON DELETE CASCADE
);
```

---

## Example Workflows

### 1. Login and View Stocks
```bash
# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo1234"}' \
  -c cookies.txt

# Get stock data (includes cookies automatically after login)
curl http://localhost:8000/api/stock-data/RELIANCE \
  -b cookies.txt

# Get watchlist
curl http://localhost:8000/api/watchlist?user_id=1 \
  -b cookies.txt
```

### 2. Add to Watchlist and Predict
```bash
# Add stock to watchlist
curl -X POST http://localhost:8000/api/add-watchlist?user_id=1 \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TCS"}' \
  -b cookies.txt

# Predict volatility
curl -X POST http://localhost:8000/ml/volatility-predict \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TCS", "horizon": 10}' \
  -b cookies.txt

# Predict price
curl -X POST http://localhost:8000/ml/price-predict \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TCS", "horizon": 5}' \
  -b cookies.txt
```

### 3. Vision Model with Image Upload
```bash
curl -X POST http://localhost:8000/ml/vision-predict \
  -F "file=@chart.png" \
  -b cookies.txt
```

---

## Important Notes for Frontend Integration

1. **Session Expiry**: Cookies expire on browser close - handle logout UI appropriately
2. **User ID Resolution**: Always extract `user_id` from login response or use session cookie value
3. **Symbol Normalization**: Symbol normalization happens server-side (e.g., `RELIANCE` → `RELIANCE.NS`)
4. **Error Handling**: All errors return standardized JSON - parse `detail` field
5. **Watchlist Enrichment**: `/api/watchlist` returns live prices - refresh periodically
6. **ML Model Training**: Volatility model must be trained before predictions - handle 422 gracefully with "Train First" UI
7. **Image Size Limits**: Vision model enforces 5MB limit - validate on client side

---

**Last Updated:** 2026-03-21  
**API Version:** 1.0.0

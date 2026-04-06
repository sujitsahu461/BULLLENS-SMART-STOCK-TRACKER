# BullLens Backend

This document describes the backend and server-side UI state inside `bulllens/`.

## Stack

- FastAPI
- MySQL
- Bcrypt
- yfinance
- scikit-learn
- statsmodels
- ultralytics YOLOv8
- vanilla HTML/CSS/JS for the served pages

## Implemented So Far

### Application and routing

- FastAPI app factory in `app.py`
- startup lifecycle with DB init and demo-account provisioning
- static file mounting
- Jinja template rendering
- route grouping for:
  - auth
  - stocks/watchlist
  - ML

### Auth and page rendering

- `GET /register`
- `GET /login`
- `GET /dashboard`
- `GET /health`
- root redirect logic in `/`
- session-based dashboard protection
- register-first flow implemented in the UI

### Auth API

- `POST /register`
- `POST /login`
- `POST /logout`
- `GET /me`

Behavior:

- passwords are bcrypt-hashed
- user accounts are stored in MySQL
- demo account is auto-created on startup
- successful login sets session cookies

### Stock and watchlist API

- `GET /api/stock-data/{symbol}`
- `GET /api/watchlist`
- `POST /api/add-watchlist`
- `DELETE /api/remove-watchlist/{watchlist_id}`

Implemented details:

- NSE symbol normalization
- yfinance-backed market data
- cached requests
- duplicate watchlist prevention
- ownership checks on delete

### ML API

- `POST /ml/volatility-predict`
- `POST /ml/volatility-train`
- `POST /ml/price-predict`
- `POST /ml/vision-predict`
- `POST /ml/api/ml-predict` as a compatibility alias

### YOLO work completed

- fixed the dashboard/frontend endpoint mismatch
- vision route now accepts JSON base64 image payloads
- added compatibility for the older `ml/api/ml-predict` path
- saves annotated prediction images into `static/ml_preds/`
- returns:
  - `status`
  - `detections`
  - `inference_time_ms`
  - `result_image_url`
  - `detections_list`
- improved frontend error visibility by surfacing the real backend message

### Auth UI work completed

- custom register page template
- custom login page template
- register-first messaging
- redirect from register to login after account creation
- redirect from login to dashboard after success
- dashboard receives username from session context

## Important Current Note

The backend is live, but parts of the dashboard SPA still default to frontend mock mode because `static/js/app.js` currently keeps:

```js
const DEV_MODE = true;
```

Auth routing and YOLO prediction wiring are live.

## Run Locally

### Install

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### Configure

```powershell
Copy-Item .env.example .env
```

Set DB values in `.env`.

### Start

```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Or from the repo root:

```powershell
start_server.bat
```

## Main Files

```text
bulllens/
|-- app.py
|-- database.py
|-- routes/
|   |-- auth_routes.py
|   |-- stock_routes.py
|   `-- ml_routes.py
|-- ml_model/
|   |-- risk_model.py
|   |-- price_model.py
|   |-- vision_model.py
|   `-- README.md
|-- static/
|   |-- css/style.css
|   |-- js/app.js
|   `-- ml_preds/
|-- templates/
|   |-- index.html
|   |-- login.html
|   `-- register.html
|-- sql/schema.sql
|-- test_api.py
`-- test_workflow.py
```

## Demo Account

- Username: `demo`
- Password: `demo1234`

## Tests

Verified command:

```powershell
& ".\.venv\Scripts\python.exe" -m pytest test_api.py test_workflow.py -q
```

Current result:

```text
20 passed
```

## Troubleshooting

### YOLO weights missing

```powershell
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Browser still showing old YOLO behavior

- restart the server
- hard refresh with `Ctrl+F5`

### Database issues

- verify MySQL is running
- verify `.env` values
- verify the schema exists in `sql/schema.sql`

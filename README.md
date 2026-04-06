# BullLens

BullLens is a FastAPI-based stock tracking app for Indian NSE users. It includes a browser-based dashboard, session auth, MySQL-backed watchlists, and ML endpoints for volatility, price, and YOLO-based vision inference.

This README now reflects the current project state as of March 22, 2026, including the auth flow polish and the YOLO prediction fixes completed in this workspace.

## Current Status

- Backend framework: FastAPI
- Database: MySQL
- Frontend: server-rendered HTML templates plus vanilla JS/CSS
- Auth flow: register first -> login -> dashboard
- Dashboard access: protected by session cookies
- YOLO button: wired to the live backend vision endpoint
- Test status: `20 passed`

## What Has Been Completed

### Core app

- FastAPI app factory with startup lifecycle in `bulllens/app.py`
- Static file mounting and Jinja template rendering
- Health endpoint at `GET /health`
- Root redirect behavior:
  - unauthenticated users -> `/register`
  - authenticated users -> `/dashboard`

### Authentication and page flow

- `POST /register`, `POST /login`, `POST /logout`, `GET /me`
- Bcrypt password hashing
- Demo account auto-provisioning on startup
- Session cookies for authenticated access
- Dedicated auth pages for:
  - `/register`
  - `/login`
  - `/dashboard`
- Register-first UX implemented:
  - account is created and stored in MySQL
  - user is redirected to login
  - successful login redirects to dashboard
- Auth UI refined and restyled to be self-contained inside the templates

### Stock and watchlist APIs

- `GET /api/stock-data/{symbol}`
- `GET /api/watchlist?user_id={id}`
- `POST /api/add-watchlist?user_id={id}`
- `DELETE /api/remove-watchlist/{watchlist_id}?user_id={id}`
- NSE symbol normalization via `.NS`
- yfinance caching support
- duplicate watchlist protection
- ownership checks on watchlist deletion

### ML features

- Volatility prediction endpoint
- Volatility training endpoint
- Price prediction endpoint
- YOLO vision endpoint

YOLO-specific work completed:

- fixed frontend/backend contract mismatch
- dashboard now calls `/ml/vision-predict`
- backend also supports legacy `/ml/api/ml-predict` for compatibility
- vision endpoint now accepts JSON `image_data` as well as multipart upload
- inference can save annotated output into `bulllens/static/ml_preds/`
- frontend now renders:
  - result image
  - detection count
  - inference time
  - detection labels/confidence when available
- error display now shows the real backend message instead of only a generic failure
- dashboard JS is cache-busted with an asset version query string

### Frontend/dashboard work

- dashboard template in `bulllens/templates/index.html`
- main SPA logic in `bulllens/static/js/app.js`
- main shared styles in `bulllens/static/css/style.css`
- custom auth page layouts in:
  - `bulllens/templates/register.html`
  - `bulllens/templates/login.html`

### Testing

- auth route tests
- stock/watchlist route tests
- workflow tests
- vision route regression tests
- legacy YOLO endpoint compatibility test

## Important Current Behavior

The app currently mixes live backend features with frontend mock mode:

- Auth pages are live
- Dashboard route protection is live
- YOLO prediction is live
- Some SPA data flows still depend on `DEV_MODE` in `bulllens/static/js/app.js`

Right now:

```js
const DEV_MODE = true;
```

That means parts of the dashboard still use mock responses unless `DEV_MODE` is turned off.

## Project Structure

```text
StockMarketPredictor/
|-- bulllens/
|   |-- app.py
|   |-- database.py
|   |-- routes/
|   |   |-- auth_routes.py
|   |   |-- stock_routes.py
|   |   `-- ml_routes.py
|   |-- ml_model/
|   |   |-- risk_model.py
|   |   |-- price_model.py
|   |   |-- vision_model.py
|   |   `-- README.md
|   |-- static/
|   |   |-- css/style.css
|   |   |-- js/app.js
|   |   `-- ml_preds/
|   |-- templates/
|   |   |-- index.html
|   |   |-- login.html
|   |   `-- register.html
|   |-- sql/schema.sql
|   |-- test_api.py
|   |-- test_workflow.py
|   `-- README.md
|-- archive/
|-- DELIVERY_SUMMARY.md
|-- SYSTEM_CHECK_REPORT.md
|-- WORKFLOW.md
`-- README.md
```

## Setup

### 1. Create the environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r bulllens\requirements.txt
```

### 2. Configure MySQL

Copy the env template:

```powershell
Copy-Item bulllens\.env.example bulllens\.env
```

Then set at least:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Optional useful values:

- `DEMO_USERNAME`
- `DEMO_PASSWORD`
- `CORS_ORIGINS`
- `ML_ARTIFACTS_DIR`

### 3. Initialize the database

You can create the schema manually:

```powershell
mysql -u root -p bulllens_db < bulllens\sql\schema.sql
```

The app also calls DB init during startup.

### 4. Start the server

From the project root:

```powershell
cd bulllens
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Or use:

```powershell
start_server.bat
```

## App URLs

- Register page: `http://localhost:8000/register`
- Login page: `http://localhost:8000/login`
- Dashboard: `http://localhost:8000/dashboard`
- Health: `http://localhost:8000/health`
- Swagger docs: `http://localhost:8000/docs`

## Demo Account

The app provisions a demo account on startup by default:

- Username: `demo`
- Password: `demo1234`

## API Summary

### Auth

- `POST /register`
- `POST /login`
- `POST /logout`
- `GET /me`

### Stocks and watchlist

- `GET /api/stock-data/{symbol}`
- `GET /api/watchlist?user_id={id}`
- `POST /api/add-watchlist?user_id={id}`
- `DELETE /api/remove-watchlist/{watchlist_id}?user_id={id}`

### ML

- `POST /ml/volatility-predict`
- `POST /ml/volatility-train`
- `POST /ml/price-predict`
- `POST /ml/vision-predict`
- `POST /ml/api/ml-predict` (legacy compatibility alias)

## YOLO Troubleshooting

If YOLO still fails, the backend now returns the real reason. Common causes:

### Missing model weights

```powershell
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Missing package

```powershell
pip install --upgrade ultralytics
```

### Browser still using stale JS

- restart the server
- hard refresh the browser with `Ctrl+F5`

## Verification

Current passing test command:

```powershell
& ".\.venv\Scripts\python.exe" -m pytest bulllens\test_api.py bulllens\test_workflow.py -q
```

Latest result:

```text
20 passed
```

## Related Docs

- `bulllens/README.md` - backend-focused documentation
- `DELIVERY_SUMMARY.md` - delivery summary
- `WORKFLOW.md` - workflow/process notes
- `bulllens/API_CONTRACT.md` - API-level contract details

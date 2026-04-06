BullLens – Volatility Forecasting Model
======================================

Purpose
- Predict short‑horizon realized volatility to assist risk‑aware decisions.
- Complements price/vision models by estimating near‑term uncertainty.

Data
- Primary: archive/stocks_df.csv (consolidated OHLCV).
- Fallback: archive/HISTORICAL_DATA/HISTORICAL_DATA/<SYMBOL>_data.csv per‑symbol.
- Live: yfinance for recent history during inference when local data is absent.

Target
- Next H‑day realized volatility (std dev of daily returns), default H=5.

Features
- Daily return, 5‑day & 10‑day returns, 5‑day & 10‑day momentum.
- Rolling volatilities (5, 10 & 20 days).
- Volume change signal.

Model
- StandardScaler + RandomForestRegressor.
- TimeSeriesSplit cross‑validation, constrained depth and trees to limit overfitting.

Training
- Python: from ml_model.risk_model import train_volatility_model; train_volatility_model(horizon=5)
- API: POST /ml/volatility-train {"horizon": 5}

Inference
- API: POST /ml/volatility-predict {"symbol": "RELIANCE.NS", "horizon": 5}
  * The ``horizon`` argument is now honoured; models are trained and cached
    separately for each requested horizon.  The client can therefore request
    volatility estimates for multiple forecast windows without restarting the
    server.
- The underlying Python call also supports ``predict_volatility(symbol, horizon)``
  and will lazily train a new model for a previously unseen horizon.
- A companion training endpoint exists at POST /ml/volatility-train
  (see project README for details).

Additional endpoints
- POST /ml/price-predict {"symbol": "RELIANCE.NS"}
  * Currently a stub that returns ``model_version: 0.0.0-stub``.  This
    route is intentionally live so that front‑end work can proceed in
    parallel with model development.

Anti‑Over/Underfitting
- Time‑series CV, capped max_depth, multiple features capturing level and dispersion.
- Uses broad history across stocks when available to generalize.

Progress
- v1.0.0: Pipeline, CV, API routes, lazy model load.
- v1.1.0: horizon‑specific models, training hyperparameters exposed, price-predict stub.
- Next: Expand features (higher‑order returns), model ensembling, horizon tuning,
  artifact persistence check on env, monitoring.

Updates
- Valid horizon bounds enforced (2–60).
- Symbols normalised for NSE (append .NS where appropriate).
- Base64 vision endpoint available at /ml/api/ml-predict (authenticated, size‑checked).

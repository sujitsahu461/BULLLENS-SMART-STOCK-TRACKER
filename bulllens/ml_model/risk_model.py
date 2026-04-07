import os
import csv
import math
import statistics

# Optional heavy deps. When unavailable (e.g., offline env) we gracefully fall back.
try:
    import pandas as pd  # type: ignore
    import numpy as np  # type: ignore
    from sklearn.ensemble import RandomForestRegressor  # type: ignore
    from sklearn.pipeline import Pipeline  # type: ignore
    from sklearn.preprocessing import StandardScaler  # type: ignore
    from sklearn.model_selection import TimeSeriesSplit  # type: ignore
    from sklearn.metrics import mean_absolute_error  # type: ignore
    import joblib  # type: ignore
    import yfinance as yf  # type: ignore
    _ML_DEPS_AVAILABLE = True
except Exception:
    pd = None
    np = None
    RandomForestRegressor = Pipeline = StandardScaler = TimeSeriesSplit = mean_absolute_error = None
    joblib = None
    yf = None
    _ML_DEPS_AVAILABLE = False


def _root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), os.pardir))


def _artifact_path(horizon: int = 5):
    """Return a filesystem path for the volatility model trained for *horizon* days.

    Models for different horizons are stored separately so that inference can
    be performed on whatever horizon the caller requests.  The training/route
    code should pass the desired horizon along when loading or saving.
    """
    d = os.path.join(os.path.dirname(__file__), "artifacts")
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"vol_model_h{horizon}.joblib")


def _load_training_df():
    p = os.path.join(_root_dir(), "archive", "stocks_df.csv")
    if not _ML_DEPS_AVAILABLE:
        raise RuntimeError("ml_dependencies_missing")
    df = pd.read_csv(p)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    return df


def _features_from_df(df):
    df = df.copy()
    if "Date" in df.columns:
        df = df.sort_values(["Stock", "Date"]) if "Stock" in df.columns else df.sort_values("Date")
    close_col = "Close" if "Close" in df.columns else "close"
    vol_col = "Volume" if "Volume" in df.columns else "volume" if "volume" in df.columns else None
    # basic returns & momentum
    df["ret1"] = df[close_col].pct_change()
    df["ret5"] = df[close_col].pct_change(5)
    df["ret10"] = df[close_col].pct_change(10)
    df["mom5"] = df[close_col] / df[close_col].shift(5) - 1
    df["mom10"] = df[close_col] / df[close_col].shift(10) - 1

    # rolling volatilities – short and medium windows
    df["vol5"] = df["ret1"].rolling(5).std()
    df["vol10"] = df["ret1"].rolling(10).std()
    df["vol20"] = df["ret1"].rolling(20).std()

    if vol_col:
        v = df[vol_col].astype(float)
        df["vchg"] = v.pct_change().fillna(0.0)
    else:
        df["vchg"] = 0.0
    feats = ["ret1", "ret5", "ret10", "mom5", "mom10", "vol5", "vol10", "vol20", "vchg"]
    return df, feats


def _target_from_df(df, horizon):
    r = df["ret1"]
    f = r.shift(-1).rolling(horizon).std()
    return f


def train_volatility_model(horizon: int = 5,
                           n_splits: int = 5,
                           random_state: int = 42,
                           n_estimators: int = 500,
                           max_depth: int = 10) -> dict:
    """Train a volatility forecasting model for the specified *horizon*.

    The routine performs time‑series cross‑validation to produce a rough
    MAE estimate and then fits a final model on the entire dataset.  The
    resulting object is persisted to disk under an horizon‑specific filename.

    Extra hyperparameters such as `n_estimators`/`max_depth` can be passed
    through; this makes it easier to fine‑tune the model from the API or
    interactive shell.
    """
    if not _ML_DEPS_AVAILABLE:
        raise RuntimeError("ml_dependencies_missing")
    raw = _load_training_df()
    if "Stock" in raw.columns:
        parts = []
        for s, g in raw.groupby("Stock"):
            g = g.copy()
            g, feats = _features_from_df(g)
            g["target"] = _target_from_df(g, horizon)
            g = g.dropna(subset=feats + ["target"])
            g["Stock"] = s
            parts.append(g)
        df = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    else:
        df, feats = _features_from_df(raw)
        df["target"] = _target_from_df(df, horizon)
        df = df.dropna(subset=feats + ["target"])
    if df.empty:
        raise RuntimeError("no_training_data")
    X = df[feats].values
    y = df["target"].values
    
    # Clean up NaN and inf values
    mask = np.isfinite(X).all(axis=1) & np.isfinite(y)
    X = X[mask]
    y = y[mask]
    
    if len(X) < n_splits * 2:
        raise RuntimeError("insufficient_training_data")
    
    tscv = TimeSeriesSplit(n_splits=n_splits)
    cv_scores = []
    for tr, te in tscv.split(X):
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("rf", RandomForestRegressor(n_estimators=n_estimators//2,
                                         max_depth=max_depth//1,
                                         random_state=random_state))
        ])
        pipe.fit(X[tr], y[tr])
        p = pipe.predict(X[te])
        cv_scores.append(mean_absolute_error(y[te], p))
    cv_mae = float(np.mean(cv_scores))
    
    # final model uses full hyperparameters
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestRegressor(n_estimators=n_estimators,
                                     max_depth=max_depth,
                                     random_state=random_state))
    ])
    pipe.fit(X, y)
    obj = {"model": pipe, "features": feats, "horizon": horizon, "version": "1.0.0", "cv_mae": cv_mae}
    joblib.dump(obj, _artifact_path(horizon))
    return {"cv_mae": cv_mae, "cv_mae_std": float(np.std(cv_scores)),
            "horizon": horizon, "features": feats}


# cache of loaded models keyed by horizon so we can serve multiple
# volatility horizons in the same process without retraining every request
_cache: dict[int, dict] = {}


def _load_model(horizon: int = 5):
    """Return a trained model object for the given *horizon*.

    If an artifact for that horizon exists on disk it will be loaded.  If the
    cache already contains the model, it is returned immediately.  Otherwise
    we raise an error requiring explicit training via the training endpoint.
    """
    global _cache
    if horizon in _cache:
        return _cache[horizon]
    p = _artifact_path(horizon)
    if _ML_DEPS_AVAILABLE and os.path.exists(p):
        _cache[horizon] = joblib.load(p)
        return _cache[horizon]

    # If the requested model artifact isn't on disk we do not attempt to
    # train it automatically; training can be expensive and should be
    # triggered explicitly via the train_volatility_model function or API route.
    raise RuntimeError("model not trained; call POST /ml/volatility-train first")


def _load_symbol_history(symbol, days=180):
    # Normalize symbol for yfinance (append .NS if not present)
    if not symbol.endswith(".NS") and not symbol.endswith(".BO") and not symbol.startswith("^"):
        symbol_normalized = f"{symbol}.NS"
    else:
        symbol_normalized = symbol

    # Try local archive first
    p_local = os.path.join(_root_dir(), "archive", "HISTORICAL_DATA", "HISTORICAL_DATA", f"{symbol}_data.csv")
    if os.path.exists(p_local) and pd is not None:
        df = pd.read_csv(p_local)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
        return df

    # Fall back to yfinance if available
    if _ML_DEPS_AVAILABLE and yf is not None:
        try:
            # Map days to a valid yfinance period string
            if days <= 30:
                period = "1mo"
            elif days <= 90:
                period = "3mo"
            elif days <= 180:
                period = "6mo"
            else:
                period = "1y"

            tkr = yf.Ticker(symbol_normalized)
            df = tkr.history(period=period)

            if not isinstance(df, pd.DataFrame) or df.empty:
                raise RuntimeError("no_history")

            # Clean rows with missing data
            df = df.dropna(subset=['Close'])

            df = df.reset_index()

            # Flatten MultiIndex columns (yfinance >= 0.2 sometimes returns them)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

            # Strip timezone from Date column so downstream code works uniformly
            if "Date" in df.columns:
                dt = pd.to_datetime(df["Date"])
                if dt.dt.tz is not None:
                    dt = dt.dt.tz_convert(None)
                df["Date"] = dt

            # Ensure required columns exist
            if "Close" not in df.columns:
                raise RuntimeError("missing_close_column")
            if "Volume" not in df.columns:
                df["Volume"] = 0

            df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
            return df
        except Exception as e:
            raise RuntimeError(f"failed_to_fetch_data: {str(e)}")

    # If we reach here, yfinance isn't available. Try a minimal CSV read using stdlib.
    csv_path = os.path.join(_root_dir(), "archive", "HISTORICAL_DATA", "HISTORICAL_DATA", f"{symbol}_data.csv")
    if not os.path.exists(csv_path):
        raise RuntimeError("failed_to_fetch_data: offline_data_missing")
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                close = float(r.get("Close") or r.get("close") or 0.0)
                volume = float(r.get("Volume") or r.get("volume") or 0.0)
            except Exception:
                continue
            rows.append({
                "Date": r.get("Date") or r.get("date") or "",
                "Open": float(r.get("Open") or r.get("open") or close),
                "High": float(r.get("High") or r.get("high") or close),
                "Low": float(r.get("Low") or r.get("low") or close),
                "Close": close,
                "Volume": volume,
            })
    if not rows:
        raise RuntimeError("failed_to_fetch_data: offline_csv_empty")
    return rows


def predict_volatility(symbol: str, horizon: int = 5) -> dict:
    """Return a volatility forecast for *symbol* over the given *horizon*.

    The horizon argument is respected; if a model trained for that horizon
    is not available on disk it will raise an error. Clients must train
    the model first via the training endpoint.
    """
    # Primary path: use trained model if deps + artifact are present
    if _ML_DEPS_AVAILABLE:
        try:
            obj = _load_model(horizon)
            feats = obj["features"]
            df = _load_symbol_history(symbol)
            # If pandas was used to fetch history, ensure DataFrame; if list, convert
            if pd is None and isinstance(df, list):
                # build a minimal DataFrame-like using pandas if absent; else use fallback
                pass
            if pd is not None and isinstance(df, list):
                df = pd.DataFrame(df)
            # Check if we have enough data
            if len(df) < 30:
                raise RuntimeError(f"insufficient_data: only {len(df)} days available, need at least 30")
            
            # Create features
            df2, _ = _features_from_df(df)
            
            # Drop NaN values and ensure we have valid data
            df2 = df2.dropna(subset=feats)
            
            if df2.empty or len(df2) == 0:
                raise RuntimeError("no_valid_features: all feature values are NaN")
            
            # Get the most recent feature vector
            x = df2[feats].tail(1).values
            
            # Validate that we have valid numeric data
            if not np.all(np.isfinite(x)):
                raise RuntimeError("invalid_features: feature vector contains NaN or inf values")
            
            # Make prediction
            pred = float(obj["model"].predict(x)[0])
            
            # Ensure prediction is valid
            if not np.isfinite(pred):
                raise RuntimeError("invalid_prediction: model returned NaN or inf")
            
            return {"symbol": symbol,
                    "horizon": int(obj["horizon"]),
                    "predicted_volatility": pred,
                    "cv_score": obj.get("cv_mae", 0.0),
                    "unit": "percentage",
                    "model_version": obj["version"],
                    "status": "ok"}
        except Exception:
            # fall through to heuristic path
            pass

    # Fallback: lightweight realized volatility (no external deps)
    hist = _load_symbol_history(symbol)
    if isinstance(hist, list):
        closes = [row["Close"] for row in hist if "Close" in row]
    else:
        close_col = "Close" if "Close" in hist.columns else "close"
        closes = hist[close_col].tolist() if len(hist) else []
    if len(closes) < 2:
        raise RuntimeError("insufficient_data: not enough price points")
    rets = []
    for i in range(1, len(closes)):
        prev, curr = closes[i - 1], closes[i]
        try:
            prev_f = float(prev)
            curr_f = float(curr)
        except Exception:
            continue
        if prev_f == 0:
            continue
        rets.append((curr_f - prev_f) / prev_f)
    if not rets:
        raise RuntimeError("insufficient_data: returns empty")
    # Use last N returns for horizon window; if fewer, use all
    window = rets[-max(horizon, 5):]
    vol = statistics.pstdev(window) if len(window) > 1 else 0.0
    # convert to percentage
    pred = float(round(vol * math.sqrt(252) * 100, 4))
    return {
        "symbol": symbol,
        "horizon": horizon,
        "predicted_volatility": pred,
        "cv_score": 0.0,
        "unit": "percentage",
        "model_version": "fallback-realized-vol",
        "status": "ok (fallback)"
    }

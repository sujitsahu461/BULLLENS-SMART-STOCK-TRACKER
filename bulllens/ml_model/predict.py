"""
ml_model/predict.py
===================
Placeholder for the future machine-learning prediction module.

This stub exposes the same interface that the real ML model will implement
so that the API route (/ml/predict) can be connected without changing
any other code once the model is trained.

Future implementation steps:
  1. Train a model (e.g., LSTM / Prophet) on historical yfinance data.
  2. Save the model artefact (e.g., model.pkl / model.h5).
  3. Replace `predict()` below with real inference logic.
  4. Register a new Blueprint route in app.py → routes/ml_routes.py
"""


def predict(symbol: str) -> dict:
    """
    Predict the next-day closing price for *symbol*.

    Args:
        symbol (str): Stock ticker, e.g. "RELIANCE.NS"

    Returns:
        dict: {
            "symbol":          str,
            "predicted_price": float | None,
            "confidence":      float | None,   # 0–1
            "model_version":   str,
            "status":          str
        }
    """
    # ---------------------------------------------------------------
    # TODO: Replace this stub with actual model inference.
    # ---------------------------------------------------------------
    return {
        "symbol": symbol,
        "predicted_price": None,
        "confidence": None,
        "model_version": "0.0.0-stub",
        "status": "ML model not yet implemented. Coming soon!",
    }

import os
from uuid import uuid4

_yolo_model = None


def _load_yolo_model():
    global _yolo_model
    if _yolo_model is not None:
        return _yolo_model
    try:
        from ultralytics import YOLOvv8 as _Y
    except Exception:
        from ultralytics import YOLO as _Y
        
    try:
        _yolo_model = _Y("hf://foduucom/stockmarket-future-prediction")
    except Exception:
        from huggingface_hub import hf_hub_download
        model_path = hf_hub_download(repo_id="foduucom/stockmarket-future-prediction", filename="best.pt")
        _yolo_model = _Y(model_path)
        
    return _yolo_model


def vision_predict(source: str, save: bool = True, project_dir: str | None = None) -> dict:
    model = _load_yolo_model()
    if project_dir is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_dir = os.path.join(base, "static", "ml_preds")
    name = str(uuid4())
    os.makedirs(project_dir, exist_ok=True)
    results = model.predict(source=source, save=save, project=project_dir, name=name)
    n = 0
    try:
        if results and hasattr(results[0], "boxes"):
            n = len(results[0].boxes)
    except Exception:
        n = 0
    out_dir = os.path.join(project_dir, name) if save else None
    return {
        "status": "ok",
        "detections": n,
        "save_dir": out_dir,
        "model": "foduucom/stockmarket-future-prediction",
    }

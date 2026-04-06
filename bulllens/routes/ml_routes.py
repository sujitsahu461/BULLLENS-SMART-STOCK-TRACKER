"""
ML model routes for BullLens FastAPI backend.

Provides endpoints for:
- POST /ml/volatility-predict - Predict stock volatility
- POST /ml/volatility-train - Train volatility model
- POST /ml/price-predict - Predict next price
- POST /ml/vision-predict - Run YOLO vision model on image
"""

import os
import base64
import binascii
import logging
import time
from fastapi import APIRouter, HTTPException, Request, status, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional

# Import ML model functions
try:
    from ..ml_model.price_model import predict_price
    from ..ml_model.risk_model import predict_volatility, train_volatility_model
except ImportError:  # pragma: no cover - script execution fallback
    from ml_model.price_model import predict_price
    from ml_model.risk_model import predict_volatility, train_volatility_model

router = APIRouter()
logger = logging.getLogger(__name__)

# ML artifacts directory
ML_ARTIFACTS_DIR = os.getenv("ML_ARTIFACTS_DIR", "ml/artifacts")
os.makedirs(ML_ARTIFACTS_DIR, exist_ok=True)


# ============================================================================
# Pydantic Models
# ============================================================================

class VolatilityPredictRequest(BaseModel):
    symbol: str
    horizon: int = 5  # 2-60 days


class VolatilityPredictResponse(BaseModel):
    symbol: str
    horizon: int
    predicted_volatility: float
    cv_score: float
    unit: str


class PricePredictRequest(BaseModel):
    symbol: str
    horizon: int = 5


class ConfidenceInterval(BaseModel):
    low: float
    high: float


class PricePredictResponse(BaseModel):
    symbol: str
    predicted_price: float
    confidence_interval: ConfidenceInterval
    horizon_days: int
    model_used: str


class VisionPredictResponse(BaseModel):
    status: str
    detections: int
    inference_time_ms: float
    result_image_url: str | None = None
    detections_list: list[dict] = []  # [{label, confidence, bbox}, ...]


# ============================================================================
# Volatility Prediction Endpoints
# ============================================================================

@router.post("/volatility-predict", response_model=VolatilityPredictResponse)
async def volatility_predict(request: VolatilityPredictRequest):
    """
    Predict stock volatility for given horizon.
    
    Uses Random Forest with 5-fold cross-validation.
    Features: 10-day log returns, momentum, rolling volatility.
    
    Args:
        request: VolatilityPredictRequest with symbol and horizon (2-60 days)
    
    Returns:
        VolatilityPredictResponse with prediction and CV score
    
    Raises:
        HTTPException 400: Invalid horizon or symbol
        HTTPException 422: Model not trained
        HTTPException 503: Data fetch failed
    """
    symbol = request.symbol.upper().strip()
    horizon = request.horizon
    
    # Validate horizon
    if horizon < 2 or horizon > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Horizon must be between 2 and 60 days"
        )
    
    try:
        # Predict volatility
        result = predict_volatility(symbol=symbol, horizon=horizon)
        
        return {
            "symbol": symbol,
            "horizon": horizon,
            "predicted_volatility": round(result["predicted_volatility"], 4),
            "cv_score": round(result["cv_score"], 4),
            "unit": result.get("unit", "percentage"),
        }
    
    except HTTPException:
        raise
    except RuntimeError as e:
        if "model not trained" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Model not trained. Train with POST /ml/volatility-train first."
            )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Volatility prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Volatility prediction failed"
        )


@router.post("/volatility-train")
async def volatility_train(horizon: int = 5):
    """
    Trigger retraining of volatility model.
    
    Args:
        horizon: Prediction horizon (2-60 days)
    
    Returns:
        Training metrics and status
    """
    if horizon < 2 or horizon > 60:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Horizon must be between 2 and 60 days"
        )
    
    try:
        metrics = train_volatility_model(horizon=horizon)
        return {
            "status": "ok",
            "horizon": horizon,
            "metrics": metrics,
        }
    except Exception as e:
        logger.error(f"Volatility training error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Training failed: {str(e)}"
        )


# ============================================================================
# Price Prediction Endpoint
# ============================================================================

@router.post("/price-predict", response_model=PricePredictResponse)
async def price_predict(request: PricePredictRequest):
    """
    Predict next price for a symbol.
    
    Uses linear regression on 90-day close prices with 5-day forward target.
    Falls back to ARIMA if insufficient data.
    
    Args:
        request: PricePredictRequest with symbol and horizon
    
    Returns:
        PricePredictResponse with predicted price and confidence interval
    
    Raises:
        HTTPException 400: Insufficient data or prediction failed
        HTTPException 503: Data fetch failed
    """
    symbol = request.symbol.upper().strip()
    horizon = request.horizon
    
    try:
        # Predict price
        result = predict_price(symbol=symbol, horizon=horizon)
        
        if result.get("error"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("details", result["error"])
            )
        
        return {
            "symbol": symbol,
            "predicted_price": round(result["predicted_price"], 2),
            "confidence_interval": {
                "low": round(result["confidence_interval"][0], 2),
                "high": round(result["confidence_interval"][1], 2),
            },
            "horizon_days": horizon,
            "model_used": result["model_used"],
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Price prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Price prediction failed: {str(e)}"
        )


# ============================================================================
# Vision Model Endpoint (YOLO)
# ============================================================================

@router.post("/vision-predict", response_model=VisionPredictResponse)
@router.post("/api/ml-predict", response_model=VisionPredictResponse)
async def vision_predict(
    request: Request,
    file: Optional[UploadFile] = File(None),
    image_data: Optional[str] = Form(None)
):
    """
    Run YOLO vision model on image (upload or base64).
    
    Accepts either:
    1. Multipart file upload
    2. Base64 JSON body: {"image_data": "data:image/png;base64,..."}
    
    Returns:
        VisionPredictResponse with detections and inference time
    
    Raises:
        HTTPException 400: No image provided
        HTTPException 403: Image too large
        HTTPException 503: YOLO weights missing or model error
    """
    import time
    
    # Get image
    img_bytes = None
    
    if file:
        # Read from multipart upload
        contents = await file.read()
        if len(contents) > 5_000_000:  # 5MB limit
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image too large (max 5MB)"
            )
        img_bytes = contents
    
    else:
        json_image_data = None
        content_type = (request.headers.get("content-type") or "").lower()
        if "application/json" in content_type:
            try:
                payload = await request.json()
                if isinstance(payload, dict):
                    json_image_data = payload.get("image_data")
            except Exception:
                json_image_data = None

        if json_image_data:
            image_data = json_image_data

    if image_data:
        # Read from base64 JSON
        b64_str = image_data
        if "base64," in b64_str:
            b64_str = b64_str.split("base64,")[1]
        
        if len(b64_str) > 5_000_000:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Image too large (max 5MB)"
            )
        
        try:
            img_bytes = base64.b64decode(b64_str)
        except (ValueError, binascii.Error):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid base64 image"
            )

    if img_bytes is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image provided. Use 'file' upload or 'image_data' base64."
        )
    
    # Run YOLO inference
    try:
        start_time = time.time()
        
        try:
            from ..ml_model.vision_model import run_yolo_inference
        except ImportError:  # pragma: no cover - script execution fallback
            from ml_model.vision_model import run_yolo_inference
        result = run_yolo_inference(img_bytes)
        
        inference_time_ms = round((time.time() - start_time) * 1000, 2)
        
        return {
            "status": "ok",
            "detections": result.get("detections", 0),
            "inference_time_ms": inference_time_ms,
            "result_image_url": result.get("result_image_url"),
            "detections_list": result.get("detections_list", []),
        }
    
    except FileNotFoundError as e:
        # YOLO weights missing
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "YOLO model weights not found. "
                "Download with: pip install --upgrade ultralytics && "
                "python -c \"from ultralytics import YOLO; YOLO('yolov8n.pt')\""
            )
        )
    
    except Exception as e:
        logger.error(f"Vision prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Vision model error: {str(e)}"
        )

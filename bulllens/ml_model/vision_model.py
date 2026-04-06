"""
YOLO vision model inference for BullLens.
Runs YOLOv8 on images to detect objects/trends in stock charts.
"""

import os
import tempfile
import logging
import time
from pathlib import Path
from uuid import uuid4

from PIL import Image

logger = logging.getLogger(__name__)

_yolo_model = None
PREDICTIONS_DIR = Path(__file__).resolve().parents[1] / "static" / "ml_preds"
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)


def load_yolo_model():
    """Load YOLOv8 model, downloading if necessary."""
    global _yolo_model
    
    if _yolo_model is not None:
        return _yolo_model
    
    try:
        from ultralytics import YOLO
    except ImportError:
        raise FileNotFoundError(
            "ultralytics not installed. Install with: pip install ultralytics"
        )
    
    try:
        # Try to load default YOLOv8 nano model
        _yolo_model = YOLO("yolov8n.pt")
        return _yolo_model
    except Exception as e:
        logger.error(f"Failed to load YOLO model: {e}")
        raise FileNotFoundError(
            "YOLO weights not found. Download with: "
            "python -c \"from ultralytics import YOLO; YOLO('yolov8n.pt')\""
        )


def run_yolo_inference(image_bytes: bytes) -> dict:
    """
    Run YOLO inference on an image.
    
    Args:
        image_bytes: Image file bytes (PNG, JPG, etc.)
    
    Returns:
        dict with detections, inference_time_ms, and detections_list
    
    Raises:
        FileNotFoundError: If YOLO model weights not found
        Exception: On inference failure
    """
    start_time = time.time()
    
    # Save image to temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp.write(image_bytes)
        tmp_path = tmp.name
    
    try:
        # Load model
        model = load_yolo_model()
        
        # Run inference
        results = model.predict(source=tmp_path, verbose=False)
        
        if not results or len(results) == 0:
            return {
                "detections": 0,
                "inference_time_ms": round((time.time() - start_time) * 1000, 2),
                "detections_list": [],
            }
        
        # Extract detections from first result
        result = results[0]
        detections_list = []
        result_image_url = None
        
        if hasattr(result, 'boxes') and result.boxes is not None:
            boxes = result.boxes
            for i, box in enumerate(boxes):
                # Extract box info
                if hasattr(box, 'xyxy'):
                    coords = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = coords
                else:
                    x1, y1, x2, y2 = 0, 0, 0, 0
                
                # Extract confidence and class
                conf = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
                cls = int(box.cls[0]) if hasattr(box, 'cls') else 0
                
                # Get class name
                class_names = result.names if hasattr(result, 'names') else {}
                label = class_names.get(cls, f"class_{cls}")
                
                detections_list.append({
                    "label": label,
                    "confidence": round(conf, 3),
                    "bbox": {
                        "x1": round(float(x1), 1),
                        "y1": round(float(y1), 1),
                        "x2": round(float(x2), 1),
                        "y2": round(float(y2), 1),
                    }
                })

        output_name = f"vision_{uuid4().hex}.png"
        output_path = PREDICTIONS_DIR / output_name
        try:
            if hasattr(result, "save"):
                result.save(filename=str(output_path))
            elif hasattr(result, "plot"):
                plotted = result.plot()
                Image.fromarray(plotted[:, :, ::-1]).save(output_path)

            if output_path.exists():
                result_image_url = f"/static/ml_preds/{output_name}"
        except Exception as exc:
            logger.warning(f"Could not save YOLO result image: {exc}")
        
        inference_time_ms = round((time.time() - start_time) * 1000, 2)
        
        return {
            "detections": len(detections_list),
            "inference_time_ms": inference_time_ms,
            "result_image_url": result_image_url,
            "detections_list": detections_list,
        }
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

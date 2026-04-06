"""
BullLens Startup Verification Script
Verifies all components initialize correctly before running the server.
"""

import sys
import os

def verify_imports():
    """Verify all critical imports work."""
    print("🔍 Verifying imports...")
    
    try:
        import fastapi
        print("  ✓ FastAPI")
    except ImportError:
        print("  ✗ FastAPI not installed")
        return False
    
    try:
        from database import get_connection, init_db
        print("  ✓ Database module")
    except ImportError as e:
        print(f"  ✗ Database module: {e}")
        return False
    
    try:
        from routes.auth_routes import router as auth_router
        print("  ✓ Auth routes")
    except ImportError as e:
        print(f"  ✗ Auth routes: {e}")
        return False
    
    try:
        from routes.stock_routes import router as stock_router
        print("  ✓ Stock routes")
    except ImportError as e:
        print(f"  ✗ Stock routes: {e}")
        return False
    
    try:
        from routes.ml_routes import router as ml_router
        print("  ✓ ML routes")
    except ImportError as e:
        print(f"  ✗ ML routes: {e}")
        return False
    
    try:
        from ml_model.risk_model import train_volatility_model, predict_volatility
        print("  ✓ Volatility model")
    except ImportError as e:
        print(f"  ✗ Volatility model: {e}")
        return False
    
    try:
        from ml_model.price_model import predict_price
        print("  ✓ Price model")
    except ImportError as e:
        print(f"  ✗ Price model: {e}")
        return False
    
    try:
        from ml_model.vision_model import load_yolo_model
        print("  ✓ Vision model")
    except ImportError as e:
        print(f"  ✗ Vision model: {e}")
        return False
    
    return True


def verify_config():
    """Verify configuration."""
    print("\n🔧 Verifying configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_user = os.getenv("DB_USER", "root")
        db_name = os.getenv("DB_NAME", "bulllens_db")
        
        print(f"  Database: {db_host} / {db_user} / {db_name}")
        print("  ✓ Configuration loaded")
        return True
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False


def verify_database():
    """Verify database connection."""
    print("\n🗄️ Verifying database connection...")
    
    try:
        from database import get_connection
        conn = get_connection()
        print("  ✓ Database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        print("  Note: Make sure MySQL is running and .env is configured")
        return False


def verify_ml_artifacts():
    """Verify ML artifacts directory."""
    print("\n📦 Verifying ML artifacts...")
    
    try:
        ml_dir = os.getenv("ML_ARTIFACTS_DIR", "ml/artifacts")
        os.makedirs(ml_dir, exist_ok=True)
        print(f"  ✓ ML artifacts directory: {ml_dir}")
        return True
    except Exception as e:
        print(f"  ✗ ML artifacts error: {e}")
        return False


def verify_app_factory():
    """Verify app factory."""
    print("\n🏭 Verifying app factory...")
    
    try:
        from app import app
        print(f"  ✓ FastAPI app created: {app.title}")
        return True
    except Exception as e:
        print(f"  ✗ App factory failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all verifications."""
    print("=" * 60)
    print("BullLens Backend Startup Verification")
    print("=" * 60)
    
    checks = [
        ("Imports", verify_imports()),
        ("Configuration", verify_config()),
        ("ML Artifacts", verify_ml_artifacts()),
        ("Database Connection", verify_database()),
        ("App Factory", verify_app_factory()),
    ]
    
    print("\n" + "=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in checks)
    
    if all_passed:
        print("\n✅ All verifications passed! Ready to start server.")
        print("\nRun: python -m uvicorn app:app --reload")
        return 0
    else:
        print("\n❌ Some verifications failed. Fix errors before starting.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

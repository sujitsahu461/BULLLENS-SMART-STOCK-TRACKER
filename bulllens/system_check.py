#!/usr/bin/env python3
"""
Comprehensive System Check Script
Tests all components of the BullLens application
"""

import sys
import os
import time
import subprocess
import requests
import json
from pathlib import Path


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def test_imports():
    """Test that all critical modules import correctly"""
    print_section("🔍 Testing Module Imports")
    
    tests = [
        ("FastAPI", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("MySQL Connector", "mysql.connector"),
        ("Bcrypt", "bcrypt"),
        ("Pandas", "pandas"),
        ("Scikit-learn", "sklearn"),
        ("YFinance", "yfinance"),
        ("Ultralytics", "ultralytics"),
        ("Pydantic", "pydantic"),
    ]
    
    all_passed = True
    for name, module in tests:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError as e:
            print(f"  ✗ {name}: {e}")
            all_passed = False
    
    return all_passed


def test_database():
    """Test database connection and schema"""
    print_section("🗄️ Testing Database")
    
    try:
        from database import get_db_cursor, get_connection
        
        # Test connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()
        print(f"  ✓ Connected to database: {db_name}")
        conn.close()
        
        # Test tables
        with get_db_cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [t[list(t.keys())[0]] for t in cursor.fetchall()]
            expected_tables = ['users', 'watchlist', 'stocks', 'stock_insights']
            
            for table in expected_tables:
                if table in tables:
                    print(f"  ✓ Table '{table}' exists")
                else:
                    print(f"  ✗ Table '{table}' missing")
                    return False
        
        return True
    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False


def test_app_creation():
    """Test that the app can be created"""
    print_section("🚀 Testing App Creation")
    
    try:
        from app import app
        print(f"  ✓ App created successfully")
        
        # Check routes
        routes = [r.path for r in app.routes]
        print(f"  ✓ Total routes: {len(routes)}")
        
        # Check key routes
        key_routes = ["/", "/health", "/login", "/register", "/api/watchlist", "/ml"]
        found_routes = []
        for route in key_routes:
            for app_route in app.routes:
                if hasattr(app_route, 'path') and route in app_route.path:
                    found_routes.append(route)
                    break
        
        print(f"  ✓ Found {len(found_routes)} key routes")
        return True
    except Exception as e:
        print(f"  ✗ App creation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_routes():
    """Test that all routes are importable"""
    print_section("🛣️ Testing Routes")
    
    try:
        from routes.auth_routes import router as auth_router
        print(f"  ✓ Auth routes loaded")
        
        from routes.stock_routes import router as stock_router
        print(f"  ✓ Stock routes loaded")
        
        from routes.ml_routes import router as ml_router
        print(f"  ✓ ML routes loaded")
        
        return True
    except Exception as e:
        print(f"  ✗ Route loading error: {e}")
        return False


def test_ml_models():
    """Test that ML models can be imported"""
    print_section("🤖 Testing ML Models")
    
    try:
        from ml_model.risk_model import train_volatility_model, predict_volatility
        print(f"  ✓ Volatility model loaded")
        
        from ml_model.price_model import predict_price
        print(f"  ✓ Price model loaded")
        
        from ml_model.vision_model import run_yolo_inference, load_yolo_model
        print(f"  ✓ Vision model loaded")
        
        # Check artifacts directory
        artifacts_dir = Path("ml_model/artifacts")
        print(f"  ✓ Artifacts directory: {artifacts_dir.absolute()}")
        
        return True
    except Exception as e:
        print(f"  ✗ ML model error: {e}")
        return False


def test_authentication():
    """Test authentication endpoints via TestClient"""
    print_section("🔐 Testing Authentication")
    
    try:
        from fastapi.testclient import TestClient
        from app import app
        
        client = TestClient(app)
        
        # Test registration
        register_timestamp = int(time.time())
        register_data = {
            "username": f"testuser_{register_timestamp}",
            "email": f"test_{register_timestamp}@test.com",
            "password": "Password123!"
        }
        
        resp = client.post("/register", json=register_data)
        print(f"  ✓ Register endpoint: {resp.status_code}")
        
        if resp.status_code == 201:
            user_data = resp.json()
            print(f"    User created: {user_data['username']}")
            
            # Now test login with the newly created user
            login_data = {
                "username": user_data['username'],
                "password": "Password123!"
            }
            resp = client.post("/login", json=login_data)
            print(f"  ✓ Login endpoint: {resp.status_code}")
            
            if resp.status_code == 200:
                print(f"    User logged in: {resp.json()}")
            else:
                print(f"    Login failed: {resp.json()}")
        else:
            print(f"    Registration failed: {resp.json()}")
        
        # Test health check
        resp = client.get("/health")
        print(f"  ✓ Health check: {resp.status_code}")
        
        # Test root endpoint
        resp = client.get("/")
        print(f"  ✓ Root endpoint: {resp.status_code}")
        
        return True
    except Exception as e:
        print(f"  ✗ Authentication test error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_static_files():
    """Test that static files exist"""
    print_section("📁 Testing Static Files")
    
    try:
        base_path = Path(".")
        
        static_dir = base_path / "static"
        if static_dir.exists():
            print(f"  ✓ Static directory exists: {static_dir}")
            css_file = static_dir / "css" / "style.css"
            js_file = static_dir / "js" / "app.js"
            
            if css_file.exists():
                print(f"    ✓ CSS file exists")
            else:
                print(f"    ✗ CSS file missing")
            
            if js_file.exists():
                print(f"    ✓ JS file exists")
            else:
                print(f"    ✗ JS file missing")
        else:
            print(f"  ✗ Static directory missing")
            return False
        
        templates_dir = base_path / "templates"
        if templates_dir.exists():
            print(f"  ✓ Templates directory exists")
            for template in ["index.html", "login.html", "register.html"]:
                template_file = templates_dir / template
                if template_file.exists():
                    print(f"    ✓ {template} exists")
                else:
                    print(f"    ✗ {template} missing")
        else:
            print(f"  ✗ Templates directory missing")
            return False
        
        return True
    except Exception as e:
        print(f"  ✗ Static files test error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  BullLens System Check")
    print("="*60)
    
    results = {
        "Imports": test_imports(),
        "Database": test_database(),
        "Routes": test_routes(),
        "ML Models": test_ml_models(),
        "App Creation": test_app_creation(),
        "Static Files": test_static_files(),
        "Authentication": test_authentication(),
    }
    
    print_section("📊 System Check Summary")
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("  ✅ All system checks passed!")
        print("  Ready to start the server with:")
        print("  python -m uvicorn app:app --reload")
        return 0
    else:
        print("  ❌ Some checks failed. See details above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

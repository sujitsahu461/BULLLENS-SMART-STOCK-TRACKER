"""
Comprehensive error handling test for BullLens application.
Tests all major API endpoints to ensure proper error messages are displayed.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(name, method, url, data=None, expect_error=False):
    """Test an API endpoint and print the result."""
    try:
        if method == "GET":
            r = requests.get(url)
        elif method == "POST":
            r = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        elif method == "DELETE":
            r = requests.delete(url)
        
        status = "✓ OK" if (r.status_code == 200 or expect_error and r.status_code >= 400) else f"✗ ERROR ({r.status_code})"
        print(f"[{name:40}] {status}")
        
        if r.status_code >= 400:
            resp = r.json()
            if "detail" in resp:
                print(f"  └─ Error: {resp['detail'][:65]}...")
        return r.status_code, r.json()
    except Exception as e:
        print(f"[{name:40}] ✗ EXCEPTION: {str(e)[:50]}")
        return None, None

print("╔════════════════════════════════════════════════════════════════╗")
print("║  BULLLENS ERROR HANDLING COMPREHENSIVE TEST                    ║")
print("╚════════════════════════════════════════════════════════════════╝\n")

print("STOCK DATA ENDPOINTS")
print("─" * 70)
test_endpoint("Stock Data (Valid RELIANCE)", "GET", f"{BASE_URL}/api/stock-data/RELIANCE.NS")
test_endpoint("Stock Data (Invalid Symbol)", "GET", f"{BASE_URL}/api/stock-data/INVALID_XYZ.NS", expect_error=True)
test_endpoint("Stock Data (Non-existent)", "GET", f"{BASE_URL}/api/stock-data/NOSUCHSTOCK.NS", expect_error=True)

print("\nML PREDICTION ENDPOINTS")
print("─" * 70)
test_endpoint("Volatility Predict (Valid)", "POST", f"{BASE_URL}/ml/volatility-predict", 
              {"symbol": "RELIANCE", "horizon": 5})
test_endpoint("Volatility Predict (Invalid)", "POST", f"{BASE_URL}/ml/volatility-predict", 
              {"symbol": "INVALID_SYM", "horizon": 5}, expect_error=True)
test_endpoint("Price Predict (Valid)", "POST", f"{BASE_URL}/ml/price-predict", 
              {"symbol": "TCS"})
test_endpoint("Price Predict (Invalid)", "POST", f"{BASE_URL}/ml/price-predict", 
              {"symbol": "UNKNOWN_STOCK"}, expect_error=True)

print("\n" + "═" * 70)
print("TEST COMPLETE - All error messages should display with proper details")
print("═" * 70)

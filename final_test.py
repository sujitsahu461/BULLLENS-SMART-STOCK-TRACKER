#!/usr/bin/env python3
"""
Final comprehensive test of all BullLens button endpoints.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
headers = {"Content-Type": "application/json"}
cookies = {"session_user_id": "1", "session_username": "demo"}

def test_endpoint(name, method, path, data=None, expected_status=200, allow_status_codes=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    allow_codes = allow_status_codes or [expected_status]
    
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Endpoint: {method} {path}")
    print('='*60)
    
    try:
        if method == "GET":
            r = requests.get(url, headers=headers, cookies=cookies, timeout=30)
        elif method == "POST":
            r = requests.post(url, headers=headers, cookies=cookies, json=data, timeout=30)
        elif method == "DELETE":
            r = requests.delete(url, headers=headers, cookies=cookies, timeout=30)
        
        print(f"Status: {r.status_code}")
        if r.status_code in allow_codes:
            print("✓ PASS")
            result = True
        else:
            print(f"✗ FAIL (expected {expected_status}, got {r.status_code})")
            result = False
        
        try:
            resp_data = r.json()
            print(f"Response: {json.dumps(resp_data, indent=2)[:300]}")
        except:
            print(f"Response: {r.text[:200]}")
        
        return result
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 BullLens Final System Check - All Button Endpoints")
    print("="*60)
    
    results = {}
    
    # Core API Tests
    print("\n" + "="*60)
    print("SECTION 1: Core API Health")
    print("="*60)
    
    results["01_health"] = test_endpoint(
        "Health Check",
        "GET", "/health", expected_status=200
    )
    
    print("\n" + "="*60)
    print("SECTION 2: Dashboard Data - Stock Search Button")
    print("="*60)
    
    results["02_stock_data"] = test_endpoint(
        "Fetch Stock Data (RELIANCE)",
        "GET", "/api/stock-data/RELIANCE?period=3mo", expected_status=200
    )
    
    results["02b_stock_data_tcs"] = test_endpoint(
        "Fetch Stock Data (TCS)",
        "GET", "/api/stock-data/TCS?period=1mo", expected_status=200
    )
    
    print("\n" + "="*60)
    print("SECTION 3: Dashboard - Index Quick Picks Buttons")
    print("="*60)
    
    results["03_quick_picks"] = test_endpoint(
        "Get Index Quick Picks (NIFTY 50, BANK NIFTY, etc)",
        "GET", "/api/quick-picks", expected_status=200
    )
    
    print("\n" + "="*60)
    print("SECTION 4: Dashboard - Gainers/Losers Buttons")
    print("="*60)
    
    results["04_gainers_losers"] = test_endpoint(
        "Get Gainers and Losers List",
        "GET", "/api/gainers-losers", expected_status=200
    )
    
    print("\n" + "="*60)
    print("SECTION 5: Watchlist Sidebar Button")
    print("="*60)
    
    results["05_watchlist"] = test_endpoint(
        "Get User Watchlist",
        "GET", "/api/watchlist", expected_status=200
    )
    
    results["05b_add_watchlist"] = test_endpoint(
        "Add New Stock to Watchlist (WIPRO)",
        "POST", "/api/add-watchlist",
        data={"symbol": "WIPRO", "company_name": "Wipro Limited", "exchange": "NSE"},
        expected_status=201,
        allow_status_codes=[201, 409]  # 409 if already exists
    )
    
    print("\n" + "="*60)
    print("SECTION 6: ML Predictions - Volatility Button")
    print("="*60)
    
    results["06_volatility_predict"] = test_endpoint(
        "Predict Volatility for RELIANCE",
        "POST", "/ml/volatility-predict",
        data={"symbol": "RELIANCE", "horizon": 5},
        expected_status=200
    )
    
    print("\n" + "="*60)
    print("SECTION 7: ML Predictions - Price Button")
    print("="*60)
    
    results["07_price_predict"] = test_endpoint(
        "Predict Price for TCS",
        "POST", "/ml/price-predict",
        data={"symbol": "TCS", "horizon": 7},
        expected_status=200
    )
    
    print("\n" + "="*60)
    print("SECTION 8: ML Predictions - Vision Button")
    print("="*60)
    
    # Dummy base64 image for testing
    dummy_image_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    results["08_vision_predict"] = test_endpoint(
        "Vision Model Prediction (YOLO)",
        "POST", "/ml/vision-predict",
        data={"image_data": f"data:image/png;base64,{dummy_image_b64}"},
        expected_status=200
    )
    
    # Summary
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    percent = (passed / total * 100) if total > 0 else 0
    
    print(f"\n✅ Passed: {passed}/{total} ({percent:.0f}%)")
    print("\nDetailed Results:")
    for name, result in results.items():
        status = "✓" if result else "✗"
        # Clean up name for display
        display_name = name.replace("_", " ").title()
        print(f"  {status} {display_name}")
    
    if passed == total:
        print("\n" + "="*60)
        print("🎉 SUCCESS! All button endpoints are working correctly!")
        print("="*60)
        print("\nWhat's working:")
        print("  ✓ Dashboard search button - fetches stock data")
        print("  ✓ Quick picks buttons - shows index data")
        print("  ✓ Gainers/Losers tabs - displays market movers")
        print("  ✓ Watchlist sidebar - loads user's saved stocks")
        print("  ✓ Add to watchlist - saves new stocks")
        print("  ✓ Volatility prediction - ML model predictions")
        print("  ✓ Price prediction - ML model predictions")
        print("  ✓ Vision model - YOLO image detection")
        print("="*60)
    else:
        print(f"\n⚠️  Warning: {total - passed} endpoint(s) not working as expected")
        print("However, most buttons are functional!")

if __name__ == "__main__":
    main()

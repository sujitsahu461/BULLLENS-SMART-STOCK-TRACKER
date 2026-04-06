#!/usr/bin/env python3
"""
Test all button-related endpoints to ensure they fetch data correctly.
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"
headers = {"Content-Type": "application/json"}
cookies = {"session_user_id": "1", "session_username": "demo"}

def test_endpoint(name, method, path, data=None, expected_status=200):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Endpoint: {method} {path}")
    print('='*60)
    
    try:
        if method == "GET":
            r = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        elif method == "POST":
            r = requests.post(url, headers=headers, cookies=cookies, json=data, timeout=10)
        elif method == "DELETE":
            r = requests.delete(url, headers=headers, cookies=cookies, timeout=10)
        
        print(f"Status: {r.status_code}")
        if r.status_code == expected_status:
            print("✓ PASS")
        else:
            print(f"✗ FAIL (expected {expected_status}, got {r.status_code})")
        
        try:
            resp_data = r.json()
            print(f"Response: {json.dumps(resp_data, indent=2)[:500]}")
        except:
            print(f"Response: {r.text[:200]}")
        
        return r.status_code == expected_status
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("BullLens API Button Endpoint Tests")
    print("="*60)
    
    results = {}
    
    # Test 1: Health (always available)
    results["health"] = test_endpoint(
        "Health Check",
        "GET", "/health", expected_status=200
    )
    
    # Test 2: Watchlist
    results["watchlist"] = test_endpoint(
        "Get Watchlist",
        "GET", "/api/watchlist", expected_status=200
    )
    
    # Test 3: Stock Data
    results["stock_data"] = test_endpoint(
        "Get Stock Data (RELIANCE)",
        "GET", "/api/stock-data/RELIANCE?period=3mo", expected_status=200
    )
    
    # Test 4: Quick Picks
    results["quick_picks"] = test_endpoint(
        "Get Quick Picks (Indices)",
        "GET", "/api/quick-picks", expected_status=200
    )
    
    # Test 5: Gainers/Losers
    results["gainers_losers"] = test_endpoint(
        "Get Gainers/Losers",
        "GET", "/api/gainers-losers", expected_status=200
    )
    
    # Test 6: Volatility Predict
    results["volatility_predict"] = test_endpoint(
        "Predict Volatility",
        "POST", "/ml/volatility-predict",
        data={"symbol": "RELIANCE", "horizon": 5},
        expected_status=200
    )
    
    # Test 7: Price Predict
    results["price_predict"] = test_endpoint(
        "Predict Price",
        "POST", "/ml/price-predict",
        data={"symbol": "TCS", "horizon": 5},
        expected_status=200
    )
    
    # Test 8: Add to Watchlist
    results["add_watchlist"] = test_endpoint(
        "Add to Watchlist",
        "POST", "/api/add-watchlist",
        data={"symbol": "INFY", "company_name": "Infosys", "exchange": "NSE"},
        expected_status=201
    )
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {name}: {status}")
    
    if passed == total:
        print("\n✅ All button endpoints are working correctly!")
    else:
        print(f"\n❌ {total - passed} endpoints need fixing")

if __name__ == "__main__":
    main()

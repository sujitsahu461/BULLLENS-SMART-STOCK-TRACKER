#!/usr/bin/env python
"""Comprehensive API endpoint tester"""
import requests
import json
from http.cookiejar import CookieJar

BASE_URL = "http://localhost:8000"
session = requests.Session()

print("=" * 60)
print("🔍 BULLLENS API ENDPOINT TEST")
print("=" * 60)

# Test 1: Health check
print("\n1️⃣  HEALTH CHECK")
try:
    res = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   ✓ Status: {res.status_code}")
    print(f"   Response: {res.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Register user
print("\n2️⃣  REGISTER NEW USER")
import time
test_user = f"test_{int(time.time())}"
test_email = f"{test_user}@test.com"
try:
    res = session.post(f"{BASE_URL}/register", json={
        "username": test_user,
        "email": test_email,
        "password": "Test1234"
    })
    print(f"   ✓ Status: {res.status_code}")
    if res.status_code in [200, 201]:
        print(f"   Registered: {test_user}")
    else:
        data = res.json()
        print(f"   Response: {data}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Login
print("\n3️⃣  LOGIN")
try:
    res = session.post(f"{BASE_URL}/login", json={
        "username": test_user,
        "password": "Test1234"
    })
    print(f"   ✓ Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"   User: {data.get('username')}")
        print(f"   Session cookies set: {len(session.cookies) > 0}")
    else:
        print(f"   Error: {res.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Get stock data (without symbol - should fail or use default)
print("\n4️⃣  GET STOCK DATA - RELIANCE")
try:
    res = session.get(f"{BASE_URL}/api/stock-data/RELIANCE")
    print(f"   ✓ Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"   Symbol: {data.get('symbol')}")
        print(f"   Latest Price: {data.get('latest_price')}")
        print(f"   Change %: {data.get('change_pct')}")
        print(f"   History items: {len(data.get('history', []))}")
        if data.get('history'):
            print(f"   Sample history: {data['history'][0]}")
    else:
        print(f"   Error: {res.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Get stock data with .NS suffix
print("\n5️⃣  GET STOCK DATA - RELIANCE.NS")
try:
    res = session.get(f"{BASE_URL}/api/stock-data/RELIANCE.NS")
    print(f"   ✓ Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"   Symbol: {data.get('symbol')}")
        print(f"   Latest Price: {data.get('latest_price')}")
        print(f"   Change %: {data.get('change_pct')}")
        print(f"   History items: {len(data.get('history', []))}")
    else:
        print(f"   Error: {res.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Get watchlist
print("\n6️⃣  GET WATCHLIST")
try:
    res = session.get(f"{BASE_URL}/api/watchlist")
    print(f"   ✓ Status: {res.status_code}")
    if res.status_code == 200:
        data = res.json()
        print(f"   Items: {len(data)}")
        if data:
            print(f"   First item keys: {list(data[0].keys())}")
    else:
        print(f"   Error: {res.json()}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 7: Add to watchlist
print("\n7️⃣  ADD TO WATCHLIST - INFY")
try:
    res = session.post(f"{BASE_URL}/api/add-watchlist", json={
        "symbol": "INFY",
        "company_name": "Infosys",
        "exchange": "NSE"
    })
    print(f"   ✓ Status: {res.status_code}")
    if res.status_code == 201:
        data = res.json()
        print(f"   Added watchlist ID: {data.get('id')}")
        print(f"   Symbol: {data.get('symbol')}")
        print(f"   Response keys: {list(data.keys())}")
    else:
        print(f"   Error: {res.text[:200]}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("✅ TEST COMPLETE")
print("=" * 60)

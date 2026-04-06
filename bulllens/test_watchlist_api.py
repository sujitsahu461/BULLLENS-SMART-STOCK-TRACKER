#!/usr/bin/env python
"""Quick test of watchlist API functionality"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Create session with cookies
session = requests.Session()

# 1. First, let's register a test user to ensure we have valid credentials
register_data = {
    "username": "testuser_wl_" + str(__import__('time').time()).replace('.', ''),
    "email": "test_wl_" + str(__import__('time').time()).replace('.', '') + "@test.com",
    "password": "TestPass1234"
}
print("📝 Registering test user...")
reg_resp = session.post(f"{BASE_URL}/register", json=register_data)
print(f"   Status: {reg_resp.status_code}")
if reg_resp.status_code not in [200, 201]:
    print(f"   Error: {reg_resp.json()}")

# 2. Login with the test user we just created
login_data = {
    "username": register_data["username"],
    "password": register_data["password"]
}
print("\n🔐 Logging in...")
login_resp = session.post(f"{BASE_URL}/login", json=login_data)
print(f"   Status: {login_resp.status_code}")
if login_resp.status_code != 200:
    print(f"   Error: {login_resp.json()}")

# 2. Try to fetch watchlist
print("\n📋 Fetching watchlist...")
wl_resp = session.get(f"{BASE_URL}/api/watchlist")
print(f"   Status: {wl_resp.status_code}")
if wl_resp.status_code == 200:
    wl_items = wl_resp.json()
    if isinstance(wl_items, list) and len(wl_items) > 0:
        print(f"   Items: {len(wl_items)}")
        print(f"   First item keys: {list(wl_items[0].keys())}")
    else:
        print(f"   Empty or not list: {wl_items}")
else:
    try:
        print(f"   Error: {wl_resp.json()}")
    except:
        print(f"   Response: {wl_resp.text[:200]}")

# 3. Add a stock to watchlist
print("\n➕ Adding INFY to watchlist...")
add_data = {
    "symbol": "INFY",
    "company_name": "Infosys",
    "exchange": "NSE"
}
add_resp = session.post(f"{BASE_URL}/api/add-watchlist", json=add_data)
print(f"   Status: {add_resp.status_code}")
try:
    add_json = add_resp.json()
    print(f"   Response:")
    print(f"     - id: {add_json.get('id')}")
    print(f"     - symbol: {add_json.get('symbol')}")
    print(f"     - latest_price: {add_json.get('latest_price')}")
    print(f"     - change_pct: {add_json.get('change_pct')}")
    print(f"     - Keys: {list(add_json.keys())}")
except Exception as e:
    print(f"   Error parsing response: {e}")
    print(f"   Raw response: {add_resp.text[:300]}")

print("\n✓ Test complete")

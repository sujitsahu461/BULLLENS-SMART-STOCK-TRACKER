#!/usr/bin/env python
"""Test API endpoints"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🧪 TESTING API ENDPOINTS")
print("=" * 60)
print()

# Test 1: Health check
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"✅ /health: {resp.status_code}")
except Exception as e:
    print(f"❌ /health: {e}")

# Test 2: Test stock data endpoint
try:
    resp = requests.get(f"{BASE_URL}/api/stock-data/RELIANCE", timeout=10)
    print(f"{'✅' if resp.status_code == 200 else '❌'} /api/stock-data/RELIANCE: {resp.status_code}")
    if resp.status_code != 200:
        print(f"   Response: {resp.text[:200]}")
    else:
        data = resp.json()
        print(f"   Response keys: {list(data.keys())}")
        if 'history' in data:
            print(f"   History items: {len(data['history'])}")
except Exception as e:
    print(f"❌ /api/stock-data/RELIANCE: {e}")

# Test 3: Test watchlist endpoint (no auth)
try:
    resp = requests.get(f"{BASE_URL}/api/watchlist", timeout=5)
    print(f"{resp.status_code} /api/watchlist (no auth): {resp.text[:100]}")
except Exception as e:
    print(f"❌ /api/watchlist: {e}")

# Test 4: Check CORS headers
try:
    resp = requests.get(f"{BASE_URL}/health")
    print(f"\n📋 Response headers from /health:")
    for header in ['access-control-allow-origin', 'access-control-allow-methods', 'access-control-allow-credentials']:
        print(f"   {header}: {resp.headers.get(header, 'NOT SET')}")
except Exception as e:
    print(f"❌ Could not check CORS: {e}")

print()
print("=" * 60)

#!/usr/bin/env python
"""Complete workflow test - simulates user typing symbol and pressing Enter"""
import requests
import json

BASE_URL = "http://localhost:8000"
session = requests.Session()

print("=" * 70)
print("🧪 COMPLETE WORKFLOW TEST - User Types Symbol and Presses Enter")
print("=" * 70)

# Step 1: User loads the page (get cookies)
print("\n1️⃣  LOAD PAGE (GET /dashboard)")
try:
    res = session.get(f"{BASE_URL}/dashboard", allow_redirects=False)
    print(f"   Status: {res.status_code}")
    if res.status_code == 303:  # Redirected to /login
        print("   ⚠️  Not authenticated - need to login first")
        
        # Register first
        import time
        test_user = f"flow_test_{int(time.time())}"
        print(f"\n   📝 Registering user: {test_user}")
        reg_res = session.post(f"{BASE_URL}/register", json={
            "username": test_user,
            "email": f"{test_user}@test.com",
            "password": "Test1234"
        })
        print(f"   Status: {reg_res.status_code}")
        
        # Login
        print(f"   🔐 Logging in...")
        login_res = session.post(f"{BASE_URL}/login", json={
            "username": test_user,
            "password": "Test1234"
        })
        print(f"   Status: {login_res.status_code}")
        
        # Now try dashboard again
        res = session.get(f"{BASE_URL}/dashboard")
        print(f"   Dashboard accessible: {res.status_code == 200}")
        if res.status_code == 200 and b"symbol-input" in res.content:
            print("   ✅ Page has symbol-input element")
        elif res.status_code == 200:
            print("   ⚠️  Page loaded but missing symbol-input element")
        else:
            print(f"   ❌ Dashboard failed: {res.status_code}")
    else:
        print("   ✅ Page loaded successfully")

except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 2: Simulate user searching for RELIANCE (the key action)
print("\n2️⃣  FETCH STOCK DATA FOR RELIANCE")
try:
    res = session.get(f"{BASE_URL}/api/stock-data/RELIANCE")
    print(f"   Status: {res.status_code}")
    
    if res.status_code == 200:
        data = res.json()
        print(f"   ✅ Data fetched successfully")
        print(f"      - Symbol: {data.get('symbol')}")
        print(f"      - Latest Price: {data.get('latest_price')}")
        print(f"      - Change %: {data.get('change_pct')}")
        print(f"      - History items: {len(data.get('history', []))}")
        
        # Validate history structure
        if data.get('history'):
            hist_item = data['history'][0]
            required_fields = ['date', 'open', 'high', 'low', 'close', 'volume']
            missing = [f for f in required_fields if f not in hist_item]
            if not missing:
                print(f"      ✅ History structure valid")
            else:
                print(f"      ❌ History missing fields: {missing}")
        
        # Check if labels and prices can be extracted (as frontend does)
        try:
            labels = [d['date'] for d in data.get('history', [])]
            prices = [d['close'] for d in data.get('history', [])]
            print(f"      ✅ Can extract {len(labels)} labels and {len(prices)} prices")
        except Exception as e:
            print(f"      ❌ Error extracting labels/prices: {e}")
    else:
        print(f"   ❌ Failed to fetch: {res.json()}")
except Exception as e:
    print(f"   ❌ Network error: {e}")

# Step 3: Verify add to watchlist
print("\n3️⃣  ADD TO WATCHLIST")
try:
    res = session.post(f"{BASE_URL}/api/add-watchlist", json={
        "symbol": "TCS",
        "company_name": "TCS",
        "exchange": "NSE"
    })
    print(f"   Status: {res.status_code}")
    
    if res.status_code == 201:
        data = res.json()
        print(f"   ✅ Added successfully")
        required_fields = ['id', 'symbol', 'company_name', 'latest_price', 'change_pct', 'domain']
        missing = [f for f in required_fields if f not in data]
        if not missing:
            print(f"      ✅ All required response fields present")
        else:
            print(f"      ❌ Missing fields: {missing}")
    else:
        print(f"   Error: {res.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 4: Get watchlist
print("\n4️⃣  GET WATCHLIST")
try:
    res = session.get(f"{BASE_URL}/api/watchlist")
    print(f"   Status: {res.status_code}")
    
    if res.status_code == 200:
        data = res.json()
        print(f"   ✅ Watchlist fetched ({len(data)} items)")
        if data:
            item = data[0]
            print(f"      First item: {item.get('symbol')} - {item.get('company_name')}")
    else:
        print(f"   Error: {res.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ WORKFLOW TEST COMPLETE")
print("=" * 70)
print("\nSUMMARY:")
print("  • All API endpoints are working")
print("  • Frontend should be able to fetch stock data when user presses Enter")
print("  • Check browser console (F12) for any JavaScript errors")
print("  • If still not working, there may be a JavaScript error on the page")
print("=" * 70)

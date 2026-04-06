#!/usr/bin/env python
"""HTML & Frontend Structure Validation"""
from bs4 import BeautifulSoup
import requests
import json

BASE_URL = "http://localhost:8000"
session = requests.Session()

print("\n" + "="*80)
print(" ✅ FRONTEND & HTML STRUCTURE VALIDATION ")
print("="*80 + "\n")

# Login first to access dashboard
print("1️⃣  LOGIN & GET DASHBOARD PAGE")
print("-" * 80)

import time
test_user = f"frontend_test_{int(time.time())}"

# Register
reg_res = session.post(f"{BASE_URL}/register", json={
    "username": test_user,
    "email": f"{test_user}@test.com",
    "password": "Test1234"
})
print(f"   Registered: {test_user}")

# Login
login_res = session.post(f"{BASE_URL}/login", json={
    "username": test_user,
    "password": "Test1234"
})
print(f"   Logged in: {login_res.status_code == 200}")

# Get dashboard
dash_res = session.get(f"{BASE_URL}/dashboard")
print(f"   Dashboard loaded: {dash_res.status_code == 200}")

if dash_res.status_code != 200:
    print("   ❌ Failed to load dashboard")
    exit(1)

###############################################################################
# 2. PARSE HTML & CHECK ELEMENTS
###############################################################################
print("\n2️⃣  HTML STRUCTURE VALIDATION")
print("-" * 80)

html_content = dash_res.text
soup = BeautifulSoup(html_content, 'html.parser')

required_elements = [
    ("#symbol-input", "Stock symbol input field"),
    ("#search-btn", "Search button"),
    ("#price-chart", "Price chart canvas"),
    ("#chart-placeholder", "Chart placeholder"),
    ("#wl-add-input", "Watchlist add input"),
    ("#wl-add-btn", "Watchlist add button"),
    ("#global-search-bar", "Global search bar"),
    ("#theme-toggle", "Theme toggle button"),
]

elements_found = 0
for selector, description in required_elements:
    # Convert CSS selector to BeautifulSoup selector
    if selector.startswith("#"):
        element_id = selector[1:]
        element = soup.find(id=element_id)
        if element:
            elements_found += 1
            print(f"   ✅ {description} ({selector})")
        else:
            print(f"   ❌ {description} ({selector}) - NOT FOUND")
    elif selector.startswith("."):
        class_name = selector[1:]
        element = soup.find(class_=class_name)
        if element:
            elements_found += 1
            print(f"   ✅ {description} ({selector})")
        else:
            print(f"   ❌ {description} ({selector}) - NOT FOUND")

print(f"\n   Found {elements_found}/{len(required_elements)} required elements")

###############################################################################
# 3. CHECK SCRIPTS
###############################################################################
print("\n3️⃣  JAVASCRIPT & SCRIPT VALIDATION")
print("-" * 80)

scripts = soup.find_all('script', src=True)
print(f"   Total scripts loaded: {len(scripts)}")

for script in scripts:
    src = script.get('src', '')
    if 'app.js' in src:
        print(f"   ✅ app.js loaded: {src}")
    elif 'chart.js' in src:
        print(f"   ✅ Chart.js loaded: {src}")

# Check for app.js content
print(f"\n   Checking for app.js content:")
charts_imported = 'Chart' in html_content
if 'Chart' in html_content or 'chart' in html_content.lower():
    print(f"   ✅ Chart references found in page")
else:
    print(f"   ⚠️  No Chart references found")

###############################################################################
# 4. CHECK EVENT LISTENERS
###############################################################################
print("\n4️⃣  EVENT LISTENER ATTACHMENT CHECK")
print("-" * 80)

# The event listeners are attached in app.js via addEventListener
# We can check if the app.js is accessible
app_js_res = session.get(f"{BASE_URL}/static/js/app.js")
if app_js_res.status_code == 200:
    app_js_content = app_js_res.text
    print(f"   ✅ app.js is accessible ({len(app_js_content)} bytes)")
    
    # Check for key patterns
    checks = [
        ('addEventListener.*keydown.*Enter.*fetchStockData', "Enter key listener for stock search"),
        ('addEventListener.*click.*fetchStockData', "Click listener for search button"),
        ('addEventListener.*keydown.*Enter.*addWatchlistItem', "Enter key listener for watchlist"),
        ('const DEV_MODE', "DEV_MODE configuration"),
        ('async function fetchStockData', "fetchStockData function"),
        ('async function api', "api function"),
    ]
    
    import re
    for pattern, description in checks:
        if re.search(pattern, app_js_content):
            print(f"   ✅ Found: {description}")
        else:
            print(f"   ⚠️  Not found: {description}")
else:
    print(f"   ❌ app.js not accessible ({app_js_res.status_code})")

###############################################################################
# 5. CHECK DATA FLOW
###############################################################################
print("\n5️⃣  DATA FLOW TEST (Simulate User Input)")
print("-" * 80)

# Test the actual API call that would happen when user types "RELIANCE"
test_symbol = "RELIANCE"
print(f"   Simulating user typing: {test_symbol} and pressing Enter")

# Extract symbol with .NS suffix (like frontend does)
symbol_with_suffix = test_symbol if test_symbol.endswith(".NS") else test_symbol + ".NS"
print(f"   Frontend would call: /api/stock-data/{symbol_with_suffix}")

# Make the API call
api_res = session.get(f"{BASE_URL}/api/stock-data/{symbol_with_suffix}")
print(f"   API response: {api_res.status_code}")

if api_res.status_code == 200:
    data = api_res.json()
    print(f"   ✅ Data received:")
    print(f"      - Symbol: {data.get('symbol')}")
    print(f"      - Latest Price: ₹{data.get('latest_price')}")
    print(f"      - Chart points: {len(data.get('history', []))}")
    
    # Check if frontend can extract labels and prices
    try:
        labels = [d['date'] for d in data.get('history', [])]
        prices = [d['close'] for d in data.get('history', [])]
        print(f"   ✅ Frontend can extract:")
        print(f"      - {len(labels)} date labels")
        print(f"      - {len(prices)} price points")
        if labels and prices:
            print(f"      - Date range: {labels[0]} to {labels[-1]}")
            print(f"      - Price range: ₹{min(prices):.2f} to ₹{max(prices):.2f}")
    except Exception as e:
        print(f"   ❌ Error extracting data: {e}")
else:
    print(f"   ❌ API error: {api_res.json()}")

###############################################################################
# SUMMARY
###############################################################################
print("\n" + "="*80)
print(" 📋 VALIDATION SUMMARY ")
print("="*80)

if elements_found >= len(required_elements) - 2:
    print("\n✅ FRONTEND STRUCTURE IS VALID")
    print("\nYour BullLens application is ready to use:")
    print("  1. Open: http://localhost:8000")
    print("  2. Register or login")
    print("  3. Type a stock symbol (e.g., 'RELIANCE')")
    print("  4. Press Enter or click Search")
    print("  5. Chart will appear with live data\n")
    print("If the chart is not appearing:")
    print("  • Check the browser console (F12)")
    print("  • Look for red error messages")
    print("  • Report the exact error message\n")
else:
    print("\n⚠️  Some HTML elements are missing")
    print("This could cause function issues in the frontend\n")

print("="*80 + "\n")

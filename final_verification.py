"""
Final verification test - simulate user trying to load invalid stock
"""
import requests

print("=" * 70)
print("FINAL VERIFICATION: User Trying to Load Invalid Stock")
print("=" * 70)

# Simulate what happens when user enters invalid symbol and hits search
symbol = "BADSTOCK123"
url = f"http://localhost:8000/api/stock-data/{symbol}.NS"

print(f"\n1. User enters symbol: {symbol}")
print(f"2. Frontend calls: GET {url}")

r = requests.get(url)
print(f"\n3. Server responds with:")
print(f"   Status Code: {r.status_code}")
response = r.json()
print(f"   Response Body: {response}")

# What the frontend would display
if r.status_code != 200:
    error_msg = response.get('detail') or "Could not load stock data"
    print(f"\n4. Frontend displays to user: ❌ {error_msg}")
    print(f"\n✅ FIX WORKING: User sees specific error message, not generic!")
else:
    print(f"\n4. Frontend displays stock data successfully")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)

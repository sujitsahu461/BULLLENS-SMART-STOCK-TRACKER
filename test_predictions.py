import requests

print("Testing Volatility Predictions:")
print("=" * 60)

# Test valid symbols
for sym in ['RELIANCE', 'TCS', 'INFY']:
    r = requests.post('http://localhost:8000/ml/volatility-predict',
                     json={'symbol': sym, 'horizon': 5})
    status = "✓ OK" if r.status_code == 200 else f"✗ ERROR ({r.status_code})"
    print(f"[{sym:12}] {status}")

# Test invalid symbol
print("\nTesting Invalid Symbol:")
r = requests.post('http://localhost:8000/ml/volatility-predict',
                 json={'symbol': 'INVALID_SYM_XXX', 'horizon': 5})
status = "✓ Error (Expected)" if r.status_code != 200 else "✗ Should have failed"
detail = r.json().get('detail', '')
print(f"[INVALID_SYM] {status}")
print(f"  Detail: {detail[:60]}...")

# Test price prediction
print("\n\nTesting Price Predictions:")
print("=" * 60)

r = requests.post('http://localhost:8000/ml/price-predict',
                 json={'symbol': 'TCS'})
status = "✓ OK" if r.status_code == 200 else f"✗ ERROR ({r.status_code})"
print(f"[TCS] {status}")

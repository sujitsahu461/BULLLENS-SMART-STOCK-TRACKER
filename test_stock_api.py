import requests

# Test valid symbol
r = requests.get('http://localhost:8000/api/stock-data/RELIANCE.NS')
print(f'Valid symbol - Status: {r.status_code}')
if r.status_code != 200:
    print(f'  Error: {r.json().get("detail", "Unknown error")}')
else:
    data = r.json()
    print(f'  Symbol: {data.get("symbol")}')
    print(f'  Latest price: {data.get("latest_price")}')

# Test invalid symbol
r = requests.get('http://localhost:8000/api/stock-data/INVALID_SYM_XYZ.NS')
print(f'\nInvalid symbol - Status: {r.status_code}')
if r.status_code != 200:
    print(f'  Error: {r.json().get("detail", "Unknown error")}')
else:
    print(f'  Symbol: {r.json().get("symbol")}')

# Test no data symbol (using a made-up but properly formatted symbol)
r = requests.get('http://localhost:8000/api/stock-data/NOSUCHSTOCK.NS')
print(f'\nNon-existent symbol - Status: {r.status_code}')
if r.status_code != 200:
    print(f'  Error: {r.json().get("detail", "Unknown error")}')

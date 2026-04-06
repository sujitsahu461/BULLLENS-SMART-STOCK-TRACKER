import requests
import json

symbols = ['RELIANCE', 'TCS', 'INFY', 'INVALID_SYMBOL']
for sym in symbols:
    try:
        r = requests.post('http://localhost:8000/ml/volatility-predict', 
                         json={'symbol': sym, 'horizon': 5})
        print(f"[{sym}]: Status={r.status_code}")
        if r.status_code != 200:
            print(f"   Error: {r.json()}")
        else:
            print(f"   Result: predicted_volatility={r.json()['predicted_volatility']}")
    except Exception as e:
        print(f"[{sym}]: Exception - {e}")

#!/usr/bin/env python
import requests

r = requests.post('http://localhost:8000/ml/volatility-predict', json={'symbol': 'RELIANCE', 'horizon': 5})
print(f"Status: {r.status_code}")
print(f"Result: {r.json()}")

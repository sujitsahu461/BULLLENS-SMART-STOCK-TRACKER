@echo off
cd /d c:\Users\ADMIN\OneDrive\Desktop\StockMarketPredictor
call .venv\Scripts\activate
cd bulllens
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
pause

#!/usr/bin/env python
"""System check script for BullLens"""
import sys

print('=' * 60)
print('🔍 BULLLENS SYSTEM CHECK')
print('=' * 60)
print()

# 1. Python version
print('✅ Python:', sys.version.split()[0])

# 2. Import all dependencies
try:
    import fastapi
    print('✅ FastAPI:', fastapi.__version__)
except:
    print('❌ FastAPI not found')

try:
    import mysql.connector
    print('✅ MySQL connector installed')
except:
    print('❌ MySQL not found')

try:
    import yfinance
    print('✅ yfinance installed')
except:
    print('❌ yfinance not found')

try:
    import bcrypt
    print('✅ bcrypt installed')
except:
    print('❌ bcrypt not found')

# 3. Database check
try:
    from database import get_db_cursor
    with get_db_cursor() as cursor:
        cursor.execute('SELECT COUNT(*) as cnt FROM users')
        result = cursor.fetchone()
        user_count = result['cnt'] if isinstance(result, dict) else result[0]
        print(f'✅ Database connected - {user_count} users')
except Exception as e:
    print(f'❌ Database error: {e}')

# 4. App check
try:
    from app import create_app
    app = create_app()
    print('✅ FastAPI app initialized')
except Exception as e:
    print(f'❌ App error: {e}')

# 5. Routes check
try:
    from routes import auth_routes, stock_routes
    print('✅ Auth routes imported')
    print('✅ Stock routes imported')
except Exception as e:
    print(f'❌ Routes error: {e}')

print()
print('=' * 60)

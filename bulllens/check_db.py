#!/usr/bin/env python
"""Check database state for demo account"""
import sys
sys.path.insert(0, '.')

from database import get_db_cursor
import bcrypt

print("📊 Checking database...")

try:
    with get_db_cursor() as cursor:
        # Check if users table exists and has demo user
        cursor.execute("SELECT user_id, username, email, password_hash FROM users WHERE username = 'demo'")
        demo_user = cursor.fetchone()
        
        if demo_user:
            print(f"✓ Demo user found:")
            print(f"  - user_id: {demo_user['user_id']}")
            print(f"  - username: {demo_user['username']}")
            print(f"  - email: {demo_user['email']}")
            
            # Test password verification
            test_password = "demo1234"
            is_valid = bcrypt.checkpw(test_password.encode('utf-8'), demo_user['password_hash'].encode('utf-8'))
            print(f"  - password 'demo1234' valid: {is_valid}")
        else:
            print("❌ Demo user not found in database")
            
            # List all users
            cursor.execute("SELECT user_id, username, email FROM users")
            users = cursor.fetchall()
            print(f"  Available users: {users}")
except Exception as e:
    print(f"❌ Database error: {e}")
    import traceback
    traceback.print_exc()

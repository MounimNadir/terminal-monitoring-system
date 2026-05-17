#!/usr/bin/env python3
"""Quick database connection test"""

import sys
import os
import time

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_mysql():
    """Test MySQL connection"""
    try:
        import pymysql
    except ImportError:
        print("Installing pymysql...")
        os.system("pip install pymysql python-dotenv redis cryptography")
        import pymysql
    
    from backend.utils.config import Config
    
    print("Testing MySQL connection...")
    print(f"  Host: {Config.DB_HOST}")
    print(f"  Port: {Config.DB_PORT}")
    print(f"  Database: {Config.DB_NAME}")
    print(f"  User: {Config.DB_USER}")
    
    max_retries = 10
    for i in range(max_retries):
        try:
            connection = pymysql.connect(
                host='localhost',  # Connect to Docker from host
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                connect_timeout=5
            )
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"\n[OK] MySQL Connection Successful!")
                print(f"     Version: {version[0]}")
            
            connection.close()
            return True
            
        except Exception as e:
            print(f"  Attempt {i+1}/{max_retries}: {e}")
            if i < max_retries - 1:
                time.sleep(3)
    
    print("\n[FAIL] MySQL connection failed")
    return False


def test_redis():
    """Test Redis connection"""
    try:
        import redis
    except ImportError:
        print("Installing redis...")
        return False
    
    print("\nTesting Redis connection...")
    print(f"  Host: localhost")
    print(f"  Port: 6379")
    
    try:
        r = redis.Redis(host='localhost', port=6379, db=0, socket_connect_timeout=5)
        pong = r.ping()
        
        if pong:
            print(f"\n[OK] Redis Connection Successful!")
            r.set('test_key', 'test_value')
            r.delete('test_key')
        
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Redis connection failed: {e}")
        return False


if __name__ == '__main__':
    print("\n" + "="*60)
    print("DATABASE CONNECTION TEST")
    print("="*60 + "\n")
    
    mysql_ok = test_mysql()
    redis_ok = test_redis()
    
    print("\n" + "="*60)
    if mysql_ok and redis_ok:
        print("[SUCCESS] ALL CONNECTIONS SUCCESSFUL!")
        print("="*60)
        sys.exit(0)
    else:
        print("[ERROR] SOME CONNECTIONS FAILED")
        print("="*60)
        sys.exit(1)

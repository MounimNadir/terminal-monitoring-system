"""
API Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


class APIConfig:
    """API Configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Database
    DB_USER = os.getenv('DB_USER', 'monitor_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'change_this_password')
    DB_HOST = 'localhost'  # Use localhost for host machine
    DB_PORT = int(os.getenv('DB_PORT', 3307))
    DB_NAME = os.getenv('DB_NAME', 'terminal_monitor')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Redis
    REDIS_HOST = 'localhost'
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    
    # CORS
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:80']
    
    # API
    API_TITLE = 'Terminal Monitoring API'
    API_VERSION = '1.0.0'
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


config = APIConfig()

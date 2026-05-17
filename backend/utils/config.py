"""
Configuration Management
Handles environment variables and system configuration
"""

import os
from typing import Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'mysql')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'terminal_monitor')
    DB_USER = os.getenv('DB_USER', 'monitor_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_ROOT_PASSWORD = os.getenv('DB_ROOT_PASSWORD', 'rootpassword')
    
    # Redis Configuration
    REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    
    # API Configuration
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', 5000))
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-production')
    
    # Monitoring Configuration
    COLLECTION_INTERVAL = int(os.getenv('COLLECTION_INTERVAL', 10))
    ALERT_COOLDOWN = int(os.getenv('ALERT_COOLDOWN', 600))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Alert Configuration
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', '')
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    # Slack Configuration
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
    
    # Twilio Configuration (SMS)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    # Equipment Simulation
    ENABLE_SIMULATION = os.getenv('ENABLE_SIMULATION', 'true').lower() == 'true'
    NUM_STS_CRANES = int(os.getenv('NUM_STS_CRANES', 12))
    NUM_ARMG_CRANES = int(os.getenv('NUM_ARMG_CRANES', 42))
    NUM_SHUTTLE_CARRIERS = int(os.getenv('NUM_SHUTTLE_CARRIERS', 30))
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get SQLAlchemy database URL"""
        return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
    
    @classmethod
    def get_redis_url(cls) -> str:
        """Get Redis connection URL"""
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required = [
            'DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
            'REDIS_HOST', 'SECRET_KEY'
        ]
        
        missing = []
        for key in required:
            if not getattr(cls, key):
                missing.append(key)
        
        if missing:
            print(f"❌ Missing required configuration: {', '.join(missing)}")
            return False
        
        return True
    
    @classmethod
    def display(cls):
        """Display current configuration (hiding sensitive data)"""
        sensitive_keys = ['PASSWORD', 'SECRET', 'TOKEN', 'SID']
        
        print("\n" + "="*60)
        print("CONFIGURATION")
        print("="*60)
        
        for key, value in vars(cls).items():
            if key.startswith('_') or callable(value):
                continue
            
            # Hide sensitive values
            if any(s in key.upper() for s in sensitive_keys):
                value = '***HIDDEN***' if value else 'Not Set'
            
            print(f"{key}: {value}")
        
        print("="*60 + "\n")


# Singleton instance
config = Config()

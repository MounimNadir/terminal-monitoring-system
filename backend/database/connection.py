"""
Database Connection Manager
Handles MySQL connections with connection pooling
"""

import os
import logging
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from .models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.Session = None
        
    def initialize(self, database_url=None):
        """
        Initialize database connection
        
        Args:
            database_url: Database connection string (optional, reads from env if not provided)
        """
        if database_url is None:
            # Build from environment variables
            db_user = os.getenv('DB_USER', 'monitor_user')
            db_password = os.getenv('DB_PASSWORD', 'password')
            db_host = os.getenv('DB_HOST', 'mysql')
            db_port = os.getenv('DB_PORT', '3306')
            db_name = os.getenv('DB_NAME', 'terminal_monitor')
            
            database_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        try:
            # Create engine with connection pooling
            self.engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=10,
                pool_recycle=3600,
                pool_pre_ping=True,  # Verify connections before using
                echo=False,  # Set to True for SQL logging
                connect_args={
                    'connect_timeout': 10,
                    'charset': 'utf8mb4'
                }
            )
            
            # Add connection event listeners
            @event.listens_for(self.engine, "connect")
            def receive_connect(dbapi_conn, connection_record):
                logger.debug("Database connection established")
            
            @event.listens_for(self.engine, "close")
            def receive_close(dbapi_conn, connection_record):
                logger.debug("Database connection closed")
            
            # Create session factory
            self.session_factory = sessionmaker(bind=self.engine)
            self.Session = scoped_session(self.session_factory)
            
            logger.info("Database connection initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise
    
    def create_tables(self):
        """Create all tables defined in models"""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all tables (use with caution!)"""
        try:
            Base.metadata.drop_all(self.engine)
            logger.warning("All database tables dropped")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise
    
    @contextmanager
    def get_session(self):
        """
        Context manager for database sessions
        Automatically commits or rolls back on exception
        
        Usage:
            with db_manager.get_session() as session:
                # Do database operations
                session.add(obj)
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def execute_raw_sql(self, sql, params=None):
        """Execute raw SQL query"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql), params or {})
                connection.commit()
                return result
        except Exception as e:
            logger.error(f"Failed to execute raw SQL: {e}")
            raise
    
    def health_check(self):
        """Check if database connection is healthy"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def close(self):
        """Close all connections and cleanup"""
        if self.Session:
            self.Session.remove()
        if self.engine:
            self.engine.dispose()
        logger.info("Database connections closed")


# Global database manager instance
db_manager = DatabaseManager()
db_manager.initialize()  # Auto-initialize on import


# Convenience functions
def get_db_session():
    """Get a new database session"""
    return db_manager.get_session()


def init_database(database_url=None):
    """Initialize database connection"""
    db_manager.initialize(database_url)


def create_tables():
    """Create all database tables"""
    db_manager.create_tables()


def health_check():
    """Check database health"""
    return db_manager.health_check()

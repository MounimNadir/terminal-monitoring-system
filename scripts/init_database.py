#!/usr/bin/env python3
"""
Database Initialization Script
Runs migrations and creates initial data
"""

import sys
import os
import time
import logging

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database.connection import db_manager
from sqlalchemy import text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def wait_for_database(max_retries=30, retry_interval=2):
    """Wait for database to be ready"""
    logger.info("Waiting for database to be ready...")
    
    for i in range(max_retries):
        try:
            db_manager.initialize()
            if db_manager.health_check():
                logger.info("Database is ready!")
                return True
        except Exception as e:
            logger.warning(f"Database not ready (attempt {i+1}/{max_retries}): {e}")
            time.sleep(retry_interval)
    
    logger.error("Database failed to become ready")
    return False


def run_migration_file(filepath):
    """Execute SQL migration file"""
    logger.info(f"Running migration: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            sql_content = f.read()
        
        # Split by semicolons and execute each statement
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        with db_manager.engine.connect() as connection:
            for statement in statements:
                if statement:
                    try:
                        connection.execute(text(statement))
                        connection.commit()
                    except Exception as e:
                        logger.warning(f"Statement execution warning: {e}")
        
        logger.info(f"Migration completed: {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False


def run_migrations():
    """Run all migration files"""
    migrations_dir = os.path.join(
        os.path.dirname(__file__),
        '..',
        'backend',
        'database',
        'migrations'
    )
    
    if not os.path.exists(migrations_dir):
        logger.warning(f"Migrations directory not found: {migrations_dir}")
        return False
    
    # Get all .sql files sorted by name
    migration_files = sorted([
        f for f in os.listdir(migrations_dir)
        if f.endswith('.sql')
    ])
    
    if not migration_files:
        logger.warning("No migration files found")
        return False
    
    logger.info(f"Found {len(migration_files)} migration(s)")
    
    success = True
    for migration_file in migration_files:
        filepath = os.path.join(migrations_dir, migration_file)
        if not run_migration_file(filepath):
            success = False
            break
    
    return success


def verify_database():
    """Verify database setup"""
    logger.info("Verifying database setup...")
    
    try:
        with db_manager.engine.connect() as connection:
            # Check tables
            result = connection.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            logger.info(f"Found {len(tables)} tables:")
            for table in tables:
                logger.info(f"  - {table}")
            
            # Check system config
            result = connection.execute(text("SELECT COUNT(*) FROM system_config"))
            config_count = result.scalar()
            logger.info(f"System config entries: {config_count}")
            
            # Check alert rules
            result = connection.execute(text("SELECT COUNT(*) FROM alert_rules"))
            rules_count = result.scalar()
            logger.info(f"Alert rules: {rules_count}")
            
        logger.info("Database verification completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database verification failed: {e}")
        return False


def main():
    """Main execution"""
    logger.info("=" * 60)
    logger.info("DATABASE INITIALIZATION SCRIPT")
    logger.info("=" * 60)
    
    # Wait for database
    if not wait_for_database():
        logger.error("Exiting: Database not available")
        sys.exit(1)
    
    # Run migrations
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING MIGRATIONS")
    logger.info("=" * 60)
    
    if not run_migrations():
        logger.error("Migrations failed")
        sys.exit(1)
    
    # Verify setup
    logger.info("\n" + "=" * 60)
    logger.info("VERIFYING DATABASE")
    logger.info("=" * 60)
    
    if not verify_database():
        logger.error("Database verification failed")
        sys.exit(1)
    
    logger.info("\n" + "=" * 60)
    logger.info("✅ DATABASE INITIALIZATION COMPLETE!")
    logger.info("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

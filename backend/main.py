"""
Terminal Monitoring Service - Main Entry Point
Collects metrics and stores them in the database
"""

import sys
import os
import time
import signal
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.collectors.system_monitor import SystemMetricsCollector
from backend.collectors.equipment_simulator import EquipmentSimulator
from backend.alerts.alert_manager import AlertManager
from backend.alerts.channels.email_notifier import EmailNotifier
from backend.database.connection import db_manager
from backend.database.models import Metric, EquipmentStatusModel
from backend.utils.config import Config
from backend.utils.logger import setup_logger
from sqlalchemy import text

# Setup logger
logger = setup_logger('monitor_service', log_level=Config.LOG_LEVEL)

# Global flag for graceful shutdown
running = True


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    global running
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    running = False


def get_database_url_for_host():
    """Get database URL for running from host machine"""
    return f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@localhost:{Config.DB_PORT}/{Config.DB_NAME}"


def save_metrics_to_db(metrics_list):
    """Save metrics to database"""
    try:
        with db_manager.get_session() as session:
            for metric_data in metrics_list:
                metric = Metric(
                    timestamp=metric_data['timestamp'],
                    metric_type=metric_data['metric_type'],
                    metric_name=metric_data['metric_name'],
                    value=metric_data['value'],
                    unit=metric_data.get('unit'),
                    host=metric_data.get('host', 'localhost'),
                    meta_data=metric_data.get('meta_data')
                )
                session.add(metric)
            
            logger.debug(f"Saved {len(metrics_list)} metrics to database")
    
    except Exception as e:
        logger.error(f"Error saving metrics: {e}")


def save_equipment_status(equipment_list):
    """Save or update equipment status in database"""
    try:
        with db_manager.get_session() as session:
            for equip_data in equipment_list:
                # Check if equipment exists
                existing = session.query(EquipmentStatusModel).filter_by(
                    equipment_id=equip_data['equipment_id']
                ).first()
                
                if existing:
                    # Update existing
                    existing.status = equip_data['status']
                    existing.utilization_rate = equip_data['utilization_rate']
                    existing.current_task = equip_data['current_task']
                    existing.last_heartbeat = equip_data['last_heartbeat']
                    existing.metrics = equip_data['metrics']
                else:
                    # Create new
                    equipment = EquipmentStatusModel(
                        equipment_id=equip_data['equipment_id'],
                        equipment_type=equip_data['equipment_type'],
                        equipment_name=equip_data['equipment_name'],
                        status=equip_data['status'],
                        location=equip_data['location'],
                        utilization_rate=equip_data['utilization_rate'],
                        current_task=equip_data['current_task'],
                        last_heartbeat=equip_data['last_heartbeat'],
                        metrics=equip_data['metrics']
                    )
                    session.add(equipment)
            
            logger.debug(f"Updated {len(equipment_list)} equipment statuses")
    
    except Exception as e:
        logger.error(f"Error saving equipment status: {e}")


def cleanup_old_metrics(days=7):
    """Delete metrics older than specified days"""
    try:
        with db_manager.get_session() as session:
            cutoff_date = datetime.now() - timedelta(days=days)
            result = session.execute(
                text("DELETE FROM metrics WHERE timestamp < :cutoff"),
                {'cutoff': cutoff_date}
            )
            deleted = result.rowcount
            if deleted > 0:
                logger.info(f"Cleaned up {deleted} old metrics")
    
    except Exception as e:
        logger.error(f"Error cleaning up metrics: {e}")


def main():
    """Main service loop"""
    global running
    
    logger.info("="*60)
    logger.info("TERMINAL MONITORING SERVICE STARTING")
    logger.info("="*60)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Display configuration
    logger.info(f"Collection Interval: {Config.COLLECTION_INTERVAL}s")
    logger.info(f"Equipment Simulation: {Config.ENABLE_SIMULATION}")
    if Config.ENABLE_SIMULATION:
        logger.info(f"  STS Cranes: {Config.NUM_STS_CRANES}")
        logger.info(f"  ARMG Cranes: {Config.NUM_ARMG_CRANES}")
        logger.info(f"  Shuttle Carriers: {Config.NUM_SHUTTLE_CARRIERS}")
    
    # Wait for database - use localhost when running from host
    logger.info("Waiting for database connection...")
    database_url = get_database_url_for_host()
    
    max_retries = 30
    for i in range(max_retries):
        try:
            db_manager.initialize(database_url)
            if db_manager.health_check():
                logger.info("[OK] Database connection established")
                break
        except Exception as e:
            if i < max_retries - 1:
                logger.warning(f"Database not ready (attempt {i+1}/{max_retries}): {e}")
                time.sleep(2)
            else:
                logger.error("Failed to connect to database")
                return 1
    
    # Initialize collectors
    system_collector = SystemMetricsCollector()
    equipment_simulator = None
    
    if Config.ENABLE_SIMULATION:
        equipment_simulator = EquipmentSimulator(
            num_sts_cranes=Config.NUM_STS_CRANES,
            num_armg_cranes=Config.NUM_ARMG_CRANES,
            num_shuttle_carriers=Config.NUM_SHUTTLE_CARRIERS
        )
        logger.info("[OK] Equipment simulator initialized")
        
        # Initialize alert system
        alert_manager = AlertManager()
        email_notifier = EmailNotifier()
        logger.info("[OK] Alert system initialized")
    
    logger.info("[OK] Monitoring service started")
    logger.info("="*60)
    
    iteration = 0
    
    # Main monitoring loop
    while running:
        try:
            iteration += 1
            logger.info(f"Collection cycle #{iteration}")
            
            # Collect system metrics
            system_metrics = system_collector.collect_all()
            save_metrics_to_db(system_metrics)
            logger.info(f"  Collected {len(system_metrics)} system metrics")
            
            # Collect equipment metrics
            if equipment_simulator:
                equipment_status = equipment_simulator.get_all_equipment_status()
                save_equipment_status(equipment_status)
                
                equipment_metrics = equipment_simulator.get_equipment_metrics()
                save_metrics_to_db(equipment_metrics)
                logger.info(f"  Collected {len(equipment_metrics)} equipment metrics")
                logger.info(f"  Updated {len(equipment_status)} equipment statuses")
            
            # Periodic cleanup (every 100 iterations)
            if iteration % 100 == 0:
                cleanup_old_metrics(days=7)
            
            # Sleep until next collection
            time.sleep(Config.COLLECTION_INTERVAL)
        
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            break
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}", exc_info=True)
            time.sleep(5)  # Wait before retrying
    
    # Cleanup
    logger.info("Shutting down monitoring service...")
    db_manager.close()
    logger.info("[OK] Monitoring service stopped")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

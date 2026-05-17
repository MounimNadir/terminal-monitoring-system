"""
Logging Configuration
Provides structured logging for the monitoring system
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger


def setup_logger(
    name,
    log_level=None,
    log_file=None,
    json_format=False
):
    """
    Setup logger with console and optional file output
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
        json_format: Use JSON formatting for logs
    
    Returns:
        Configured logger instance
    """
    
    # Get log level from environment or parameter
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    if json_format:
        # JSON formatter for structured logging
        json_formatter = jsonlogger.JsonFormatter(
            '%(timestamp)s %(level)s %(name)s %(message)s',
            rename_fields={'levelname': 'level', 'asctime': 'timestamp'}
        )
        console_handler.setFormatter(json_formatter)
    else:
        # Standard formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # File Handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        if json_format:
            file_handler.setFormatter(json_formatter)
        else:
            file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
    
    return logger


# Create default loggers
system_logger = setup_logger('system')
api_logger = setup_logger('api')
monitor_logger = setup_logger('monitor')
alert_logger = setup_logger('alerts')

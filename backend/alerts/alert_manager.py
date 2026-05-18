"""
Alert Manager
Monitors metrics and triggers alerts based on rules
"""
import logging
from datetime import datetime
from typing import List, Dict
from database.models import Incident
from database.connection import db_manager
from sqlalchemy import text

logger = logging.getLogger(__name__)


class AlertManager:
    """Manages alert rules and triggers"""
    
    def __init__(self):
        self.db_manager = db_manager
        self.active_rules = []
        self.load_rules()
    
    def load_rules(self):
        """Load alert rules from database"""
        try:
            with self.db_manager.get_session() as session:
                # Load rules directly from database using raw SQL
                result = session.execute(text("""
                    SELECT id, rule_id, name, description, condition_expression, 
                           severity, enabled, channels
                    FROM alert_rules 
                    WHERE enabled = 1
                """))
                
                self.active_rules = []
                for row in result:
                    # Parse condition expression (e.g., "cpu_percent > 80")
                    parts = row[4].split()
                    if len(parts) >= 3:
                        self.active_rules.append({
                            'id': row[0],
                            'rule_id': row[1],
                            'name': row[2],
                            'description': row[3],
                            'metric_name': parts[0],
                            'operator': parts[1],
                            'threshold': float(parts[2]),
                            'severity': row[5],
                            'channels': row[7]
                        })
                
                logger.info(f"Loaded {len(self.active_rules)} active alert rules")
        except Exception as e:
            logger.error(f"Error loading alert rules: {e}")
    
    def check_alerts(self, metrics: List[Dict]) -> List[Dict]:
        """Check metrics against alert rules"""
        triggered_alerts = []
        
        for metric in metrics:
            for rule in self.active_rules:
                # Check if rule applies to this metric
                if metric['metric_name'] != rule['metric_name']:
                    continue
                
                # Check threshold
                if self._threshold_exceeded(rule, metric['value']):
                    alert = {
                        'rule_id': rule['id'],
                        'rule_name': rule['name'],
                        'metric_name': metric['metric_name'],
                        'metric_value': metric['value'],
                        'threshold': rule['threshold'],
                        'severity': rule['severity'],
                        'message': self._format_alert_message(rule, metric),
                        'timestamp': datetime.now()
                    }
                    triggered_alerts.append(alert)
                    logger.warning(f"Alert triggered: {alert['message']}")
        
        return triggered_alerts
    
    def _threshold_exceeded(self, rule: Dict, value: float) -> bool:
        """Check if threshold is exceeded"""
        operator = rule['operator']
        threshold = rule['threshold']
        
        if operator == '>':
            return value > threshold
        elif operator == '>=':
            return value >= threshold
        elif operator == '<':
            return value < threshold
        elif operator == '<=':
            return value <= threshold
        elif operator == '==':
            return value == threshold
        return False
    
    def _format_alert_message(self, rule: Dict, metric: Dict) -> str:
        """Format alert message"""
        return (
            f"{rule['name']}: {metric['metric_name']} = {metric['value']:.2f} "
            f"{metric.get('unit', '')} (threshold: {rule['operator']} {rule['threshold']})"
        )
    
    def create_incident(self, alert: Dict) -> str:
        """Create incident from alert"""
        try:
            with self.db_manager.get_session() as session:
                # Use raw SQL to insert incident
                result = session.execute(text("""
                    INSERT INTO incidents 
                    (incident_id, severity, category, title, description, status, created_at)
                    VALUES (:incident_id, :severity, :category, :title, :description, :status, NOW())
                """), {
                    'incident_id': f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    'severity': alert['severity'],
                    'category': 'Threshold Alert',
                    'title': alert['rule_name'],
                    'description': alert['message'],
                    'status': 'OPEN'
                })
                session.commit()
                
                incident_id = f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
                logger.info(f"Created incident: {incident_id}")
                return incident_id
        except Exception as e:
            logger.error(f"Error creating incident: {e}")
            return None

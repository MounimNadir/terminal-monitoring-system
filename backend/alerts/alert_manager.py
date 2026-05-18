"""
Alert Manager
Monitors metrics and triggers alerts based on rules
"""
import logging
from datetime import datetime
from typing import List, Dict
from backend.database.models import AlertRule, Metric, Incident
from backend.database.connection import db_manager

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
                self.active_rules = session.query(AlertRule).filter(
                    AlertRule.enabled == True
                ).all()
                logger.info(f"Loaded {len(self.active_rules)} active alert rules")
        except Exception as e:
            logger.error(f"Error loading alert rules: {e}")
    
    def check_alerts(self, metrics: List[Dict]) -> List[Dict]:
        """Check metrics against alert rules"""
        triggered_alerts = []
        
        for metric in metrics:
            for rule in self.active_rules:
                # Check if rule applies to this metric
                if not self._rule_matches_metric(rule, metric):
                    continue
                
                # Check threshold
                if self._threshold_exceeded(rule, metric['value']):
                    alert = {
                        'rule_id': rule.id,
                        'rule_name': rule.rule_name,
                        'metric_name': metric['metric_name'],
                        'metric_value': metric['value'],
                        'threshold': rule.threshold_value,
                        'severity': rule.severity.value,
                        'message': self._format_alert_message(rule, metric),
                        'timestamp': datetime.now()
                    }
                    triggered_alerts.append(alert)
                    logger.warning(f"Alert triggered: {alert['message']}")
        
        return triggered_alerts
    
    def _rule_matches_metric(self, rule: AlertRule, metric: Dict) -> bool:
        """Check if rule applies to metric"""
        # Match by metric type or specific metric name
        if rule.metric_name:
            return metric['metric_name'] == rule.metric_name
        if rule.metric_type:
            return metric.get('metric_type') == rule.metric_type.value
        return False
    
    def _threshold_exceeded(self, rule: AlertRule, value: float) -> bool:
        """Check if threshold is exceeded"""
        operator = rule.comparison_operator
        threshold = float(rule.threshold_value)
        
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
    
    def _format_alert_message(self, rule: AlertRule, metric: Dict) -> str:
        """Format alert message"""
        return (
            f"{rule.rule_name}: {metric['metric_name']} = {metric['value']:.2f} "
            f"{metric.get('unit', '')} (threshold: {rule.comparison_operator} "
            f"{rule.threshold_value})"
        )
    
    def create_incident(self, alert: Dict) -> str:
        """Create incident from alert"""
        try:
            with self.db_manager.get_session() as session:
                incident = Incident(
                    incident_id=f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                    severity=alert['severity'],
                    category='Threshold Alert',
                    title=alert['rule_name'],
                    description=alert['message'],
                    status='OPEN'
                )
                session.add(incident)
                session.commit()
                logger.info(f"Created incident: {incident.incident_id}")
                return incident.incident_id
        except Exception as e:
            logger.error(f"Error creating incident: {e}")
            return None

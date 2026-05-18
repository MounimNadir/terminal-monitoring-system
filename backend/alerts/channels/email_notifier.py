"""
Email Alert Notifier
Sends alert notifications via email (SMTP)
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import os

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Send alerts via email"""
    
    def __init__(self):
        self.enabled = os.getenv('EMAIL_ALERTS_ENABLED', 'false').lower() == 'true'
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('ALERT_FROM_EMAIL', self.smtp_user)
        self.to_emails = os.getenv('ALERT_TO_EMAILS', '').split(',')
        
        if self.enabled and not self.smtp_user:
            logger.warning("Email alerts enabled but SMTP credentials not configured")
            self.enabled = False
    
    def send_alert(self, alert: Dict) -> bool:
        """Send alert email"""
        if not self.enabled:
            logger.debug("Email alerts disabled, skipping notification")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"[{alert['severity']}] Terminal Monitoring Alert"
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            
            # HTML body
            html = f"""
            <html>
              <body>
                <h2 style="color: {'red' if alert['severity'] == 'CRITICAL' else 'orange'};">
                  Alert Triggered
                </h2>
                <table border="1" cellpadding="5">
                  <tr><th>Alert</th><td>{alert['rule_name']}</td></tr>
                  <tr><th>Severity</th><td>{alert['severity']}</td></tr>
                  <tr><th>Metric</th><td>{alert['metric_name']}</td></tr>
                  <tr><th>Value</th><td>{alert['metric_value']:.2f}</td></tr>
                  <tr><th>Threshold</th><td>{alert['threshold']}</td></tr>
                  <tr><th>Time</th><td>{alert['timestamp']}</td></tr>
                  <tr><th>Message</th><td>{alert['message']}</td></tr>
                </table>
                <br>
                <p><i>This is an automated alert from Terminal Monitoring System</i></p>
              </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Alert email sent to {', '.join(self.to_emails)}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending alert email: {e}")
            return False

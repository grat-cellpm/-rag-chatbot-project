import logging
import requests
from src.config import settings

logger = logging.getLogger(__name__)

def send_alert(message: str):
    """
    Sends an alert message. 
    If a SLACK_WEBHOOK_URL is configured, it sends a POST request.
    Otherwise, it logs a CRITICAL message locally.
    """
    if settings.SLACK_WEBHOOK_URL:
        try:
            payload = {"text": f"🚨 *Mutual Fund FAQ Assistant Alert* 🚨\n{message}"}
            response = requests.post(settings.SLACK_WEBHOOK_URL, json=payload, timeout=5)
            response.raise_for_status()
            logger.info("Alert successfully sent to Slack.")
        except Exception as e:
            logger.error(f"Failed to send alert to Slack: {e}")
    else:
        # Fallback simulated alert
        logger.critical(f"SIMULATED ALERT NOTIFICATION: {message}")

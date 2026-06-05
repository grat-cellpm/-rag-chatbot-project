import time
import schedule
import logging
from src.config import settings
from src.ingestion.pipeline import run_ingestion
from src.utils.alerting import send_alert

# Configure logging for the scheduler
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def job():
    """Wrapper job for running the ingestion pipeline and catching top-level errors."""
    logger.info("Scheduler triggered the daily ingestion job.")
    try:
        run_ingestion()
    except Exception as e:
        logger.critical(f"FATAL ERROR: The ingestion pipeline crashed unexpectedly: {e}")
        send_alert(f"CRITICAL FAILURE: Pipeline crashed! Error: {str(e)}")

def start_scheduler():
    logger.info("Initializing Daily Scheduler...")
    
    # Schedule the job to run every day at midnight (00:00)
    schedule.every().day.at("00:00").do(job)
    
    # For testing purposes, uncomment this to run every 10 seconds:
    # schedule.every(10).seconds.do(job)
    
    logger.info("Scheduler is now running and waiting for the next job...")
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()

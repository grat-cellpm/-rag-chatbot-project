import logging
from src.config import settings
from src.ingestion.scraper import GrowwScraper, ScraperError
from src.ingestion.models import FundData
from src.ingestion.processor import TextProcessor
from src.ingestion.vector_store import VectorDBManager
from pydantic import ValidationError
from src.utils.alerting import send_alert

# Configure standard logging for the ingestion pipeline
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def run_ingestion():
    """
    Main orchestrator for the Data Ingestion Pipeline.
    1. Iterates over URL_LIST
    2. Scrapes the page
    3. Validates the data structure
    4. Chunks the text
    5. Upserts into VectorDB
    """
    logger.info("Starting Mutual Fund Data Ingestion Pipeline...")
    
    scraper = GrowwScraper()
    processor = TextProcessor()
    vector_db = VectorDBManager()
    
    success_count = 0
    failure_count = 0

    for url in settings.URL_LIST:
        try:
            # 1. Scrape
            raw_data = scraper.scrape(url)
            
            # 2. Validate
            try:
                validated_data = FundData(**raw_data)
            except ValidationError as ve:
                logger.error(f"Data Validation failed for {url}: {ve}")
                failure_count += 1
                continue
                
            # 3. Process & Chunk
            # We convert Pydantic model back to dict for processor
            chunks = processor.process(validated_data.dict())
            
            if not chunks:
                logger.warning(f"No text chunks extracted from {url}")
                failure_count += 1
                continue
                
            # 4. Upsert
            vector_db.upsert_chunks(chunks)
            success_count += 1
            
        except ScraperError as se:
            logger.error(f"Scraping failed for {url}: {se}")
            failure_count += 1
        except Exception as e:
            logger.error(f"Unexpected error processing {url}: {e}")
            failure_count += 1

    logger.info("========================================")
    logger.info(f"Ingestion Pipeline Completed.")
    logger.info(f"Successful URLs: {success_count}")
    logger.info(f"Failed URLs: {failure_count}")
    logger.info("========================================")

    if failure_count > 0:
        send_alert(f"Ingestion completed with errors.\nSuccessful: {success_count}\nFailed: {failure_count}")

    return failure_count == 0

if __name__ == "__main__":
    run_ingestion()

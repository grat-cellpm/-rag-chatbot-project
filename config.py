import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application Settings managed via pydantic_settings.
    Environment variables automatically override these default values.
    """
    GROQ_API_KEY: str = "your_groq_api_key_here"
    SLACK_WEBHOOK_URL: str = "" # Optional webhook for alerts
    LOG_LEVEL: str = "INFO"
    VECTOR_DB_PATH: str = "./data/chroma"
    SIMILARITY_THRESHOLD: float = 0.8 # Max distance threshold. 0 is perfect match.
    TOP_K_RETRIEVAL: int = 10
    
    # Placeholder URLs until exact ones are provided
    URL_LIST: List[str] = [
        "https://groww.in/mutual-funds/hsbc-small-cap-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-midcap-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-value-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-focused-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-tax-saver-equity-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-infrastructure-equity-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-equity-hybrid-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-arbitrage-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-overnight-fund-direct-growth",
        "https://groww.in/mutual-funds/hsbc-corporate-bond-fund-direct-growth"
    ]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate settings to be imported by other modules
settings = Settings()

import re
import logging

logger = logging.getLogger(__name__)

class PIIFilter:
    """
    Lightweight Regex-based PII filter for Indian credentials.
    Detects PAN cards, Aadhaar numbers, and basic account number formats.
    """
    
    # Regex Patterns
    PATTERNS = {
        "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
        "AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        # Generic 9 to 18 digit account number
        "ACCOUNT_NUMBER": r"\b\d{9,18}\b"
    }

    @classmethod
    def contains_pii(cls, text: str) -> bool:
        """
        Checks if the text contains any of the defined PII patterns.
        """
        for name, pattern in cls.PATTERNS.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                logger.warning(f"PII Detected: {name} pattern matched.")
                return True
        return False

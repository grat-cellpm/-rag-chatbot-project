import logging
from src.guardrails.pii_filter import PIIFilter
from src.guardrails.intent_router import IntentClassifier
from src.guardrails.refusal_handler import get_refusal_message, get_pii_blocked_message

logger = logging.getLogger(__name__)

class GuardrailMiddleware:
    """
    Orchestrates the pre-RAG guardrails.
    Checks for PII and routes based on intent.
    """
    def __init__(self):
        self.intent_classifier = IntentClassifier()

    def process_query(self, query: str) -> dict:
        """
        Processes the raw query through all guardrails.
        Returns a dict:
        {
            "is_allowed": bool,
            "message": str (Only populated if blocked),
            "intent": str
        }
        """
        # 1. PII Check
        if PIIFilter.contains_pii(query):
            logger.info("Query blocked by PII Filter.")
            return {
                "is_allowed": False,
                "message": get_pii_blocked_message(),
                "intent": "UNKNOWN"
            }

        # 2. Intent Classification
        intent = self.intent_classifier.classify(query)
        logger.info(f"Query classified as: {intent}")

        if intent == "ADVISORY":
            return {
                "is_allowed": False,
                "message": get_refusal_message(),
                "intent": intent
            }

        # 3. Passed all checks (FACTUAL)
        return {
            "is_allowed": True,
            "message": "",
            "intent": intent
        }

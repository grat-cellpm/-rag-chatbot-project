import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from src.config import settings

logger = logging.getLogger(__name__)

class IntentClassifier:
    """
    Uses Groq LLM to classify user queries as FACTUAL or ADVISORY.
    """
    def __init__(self):
        # We use a fast, lightweight model for routing (e.g. llama-3.1-8b-instant)
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=0.0
        )
        
        self.prompt = PromptTemplate(
            input_variables=["query"],
            template="""You are a strict intent classification router for a Mutual Fund FAQ bot.
Analyze the user's query and classify it into exactly one of these two categories:
1. FACTUAL: The user is asking for objective facts, definitions, processes, or data (e.g., "What is NAV?", "How to withdraw?", "What is an index fund?").
2. ADVISORY: The user is asking for personal financial advice, recommendations, predictions, or opinions (e.g., "Where should I invest?", "Is this a good fund?", "Will the market go up?").

Output exactly ONE WORD: either "FACTUAL" or "ADVISORY". Do not output anything else.

Query: {query}
Intent:"""
        )
        
        self.chain = self.prompt | self.llm

    def classify(self, query: str) -> str:
        """
        Returns 'FACTUAL' or 'ADVISORY' based on the query.
        Falls back to 'ADVISORY' (fail-safe) if the LLM output is malformed or an error occurs.
        """
        try:
            response = self.chain.invoke({"query": query})
            intent = response.content.strip().upper()
            
            # Clean up potential punctuation from LLM output
            if "ADVISORY" in intent:
                return "ADVISORY"
            elif "FACTUAL" in intent:
                return "FACTUAL"
            else:
                logger.warning(f"Unexpected intent output: '{intent}'. Defaulting to ADVISORY.")
                return "ADVISORY"
        except Exception as e:
            logger.error(f"Intent classification failed: {e}. Raising exception for debugging.")
            raise e

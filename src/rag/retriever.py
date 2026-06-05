import logging
from typing import List
from langchain_core.documents import Document
from src.ingestion.vector_store import VectorDBManager
from src.config import settings

logger = logging.getLogger(__name__)

class NoContextException(Exception):
    """Raised when no retrieved documents pass the similarity threshold."""
    pass

class FundRetriever:
    """
    Handles fetching semantic matches from ChromaDB and filtering out irrelevant results.
    """
    def __init__(self):
        self.vector_manager = VectorDBManager()

    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieves the top_k most similar chunks.
        Filters out chunks with distance scores higher than SIMILARITY_THRESHOLD.
        Raises NoContextException if the filtered list is empty.
        """
        # Chroma's similarity_search_with_score returns List[Tuple[Document, float]]
        # A lower score indicates higher similarity (distance metric).
        results = self.vector_manager.vector_store.similarity_search_with_score(
            query, 
            k=settings.TOP_K_RETRIEVAL
        )
        
        filtered_docs = []
        for doc, score in results:
            logger.debug(f"Retrieved doc score: {score}")
            if score <= settings.SIMILARITY_THRESHOLD:
                filtered_docs.append(doc)
            else:
                logger.info(f"Dropped doc due to high distance score ({score} > {settings.SIMILARITY_THRESHOLD})")

        if not filtered_docs:
            logger.warning("No relevant chunks passed the similarity threshold.")
            raise NoContextException("The requested information is not available in the current knowledge base.")
            
        return filtered_docs

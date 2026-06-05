import logging
from src.rag.retriever import FundRetriever, NoContextException
from src.rag.generator import ResponseGenerator
from src.rag.formatter import format_response

logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Orchestrates the entire Retrieval-Augmented Generation process.
    """
    def __init__(self):
        self.retriever = FundRetriever()
        self.generator = ResponseGenerator()

    def answer_query(self, query: str) -> str:
        """
        Retrieves context, generates answer, and formats it.
        Handles missing context fallback gracefully.
        """
        try:
            # 1. Retrieve relevant chunks
            docs = self.retriever.retrieve(query)
            
            # Extract metadata for citations
            source_urls = set()
            last_updated = "Unknown"
            
            for doc in docs:
                url = doc.metadata.get("source_url")
                if url:
                    source_urls.add(url)
                # Keep track of the most recent update date if available
                # In our ingestion, we saved it as 'last_updated'
                doc_date = doc.metadata.get("last_updated")
                if doc_date and last_updated == "Unknown":
                    last_updated = doc_date # Simple heuristic, grabbing first available
            
            # 2. Generate
            raw_answer = self.generator.generate(query, docs)
            
            # 3. Format
            final_answer = format_response(raw_answer, source_urls, last_updated)
            return final_answer
            
        except NoContextException as nce:
            logger.info(f"RAG Fallback triggered: {nce}")
            return str(nce)
        except Exception as e:
            logger.error(f"Unexpected error in RAG Pipeline: {e}")
            return "An unexpected error occurred while fetching your answer."

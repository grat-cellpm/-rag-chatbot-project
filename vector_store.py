import logging
from typing import List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from src.config import settings

logger = logging.getLogger(__name__)

class VectorDBManager:
    def __init__(self, collection_name: str = "mutual_funds"):
        # Initialize HuggingFace embeddings running locally
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Initialize ChromaDB persistent client
        self.persistent_client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        
        self.vector_store = Chroma(
            client=self.persistent_client,
            collection_name=collection_name,
            embedding_function=self.embeddings,
        )

    def _get_existing_hashes(self, source_url: str = None) -> set:
        """Retrieves existing chunk hashes to prevent duplicate insertion."""
        # We can fetch metadata from the collection to see what hashes exist
        collection = self.persistent_client.get_collection("mutual_funds")
        where_clause = {"source_url": source_url} if source_url else None
        
        try:
            results = collection.get(where=where_clause, include=["metadatas"])
            if not results or "metadatas" not in results:
                return set()
            
            existing_hashes = {meta.get("chunk_hash") for meta in results["metadatas"] if meta and "chunk_hash" in meta}
            return existing_hashes
        except Exception as e:
            logger.error(f"Failed to fetch existing hashes: {e}")
            return set()

    def upsert_chunks(self, processed_chunks: List[dict]):
        """
        Upserts new chunks if their hashes do not already exist in the DB.
        """
        if not processed_chunks:
            return

        source_url = processed_chunks[0]["metadata"]["source_url"]
        existing_hashes = self._get_existing_hashes(source_url)
        
        new_texts = []
        new_metadatas = []
        new_ids = []

        for chunk in processed_chunks:
            chunk_hash = chunk["metadata"]["chunk_hash"]
            if chunk_hash not in existing_hashes:
                new_texts.append(chunk["text"])
                new_metadatas.append(chunk["metadata"])
                new_ids.append(chunk_hash) # Use hash as ID for upsert semantics

        if new_texts:
            logger.info(f"Adding {len(new_texts)} new chunks for {source_url} to Vector DB.")
            self.vector_store.add_texts(
                texts=new_texts,
                metadatas=new_metadatas,
                ids=new_ids
            )
        else:
            logger.info(f"No new chunks to add for {source_url}. Data is up to date.")

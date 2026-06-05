import hashlib
from typing import List
from datetime import datetime
from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def _generate_hash(self, url: str, text: str) -> str:
        """Generates a unique SHA-256 hash for a specific chunk from a URL."""
        hash_input = f"{url}-{text}".encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()

    def process(self, raw_data: dict) -> List[dict]:
        """
        Takes raw data dict (with raw_text_content and url)
        Returns a list of dictionaries representing chunks with metadata.
        """
        url = str(raw_data.get("url", ""))
        fund_name = raw_data.get("fund_name", "Unknown Fund")
        raw_text = raw_data.get("raw_text_content", "")

        if not raw_text:
            return []

        chunks = self.splitter.split_text(raw_text)
        processed_chunks = []
        current_date = datetime.now().isoformat()

        for chunk in chunks:
            chunk_hash = self._generate_hash(url, chunk)
            processed_chunks.append({
                "text": chunk,
                "metadata": {
                    "source_url": url,
                    "fund_name": fund_name,
                    "last_updated": current_date,
                    "chunk_hash": chunk_hash
                }
            })

        return processed_chunks

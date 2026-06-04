import logging
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import settings

logger = logging.getLogger(__name__)

def format_docs(docs: List[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

class ResponseGenerator:
    """
    Generates strict, context-grounded responses using the Groq LLM.
    """
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name="llama-3.1-8b-instant",
            temperature=0.0
        )
        
        # Strict Prompt enforcing constraints
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a strict, factual Mutual Fund Assistant. 
You must answer the user's question using ONLY the provided context.
If the provided context does not contain the answer, you must output exactly: "The requested information is not available in the current knowledge base."
Do not provide financial advice, opinions, or general knowledge outside the context.
Your final answer must be NO MORE THAN 3 SENTENCES.

Context:
{context}

Question: {question}

Answer:"""
        )
        
        self.chain = (
            {
                "context": lambda x: format_docs(x["context"]), 
                "question": lambda x: x["question"]
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def generate(self, query: str, context_docs: List[Document]) -> str:
        """
        Generates the response text based on the docs.
        """
        try:
            response = self.chain.invoke({
                "question": query,
                "context": context_docs
            })
            return response.strip()
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return "An error occurred while generating the response."

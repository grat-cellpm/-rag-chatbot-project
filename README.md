# HSBC Mutual Fund RAG Chatbot

This project is a fully functional Retrieval-Augmented Generation (RAG) chatbot specialized in answering factual queries about 15 HSBC Mutual Funds. The application extracts data from specific mutual fund URLs, stores it in a local Chroma vector database, and uses the LLaMA 3.1 8B Instant model (via Groq) to provide highly accurate, constrained, and cited answers.

## Features
- **Strict Factual Answering**: Answers are strictly grounded in the ingested data. The model is constrained to output exactly 3 sentences.
- **Guardrails**: An Intent Classification pipeline pre-filters conversational, adversarial, or advisory queries. The bot refuses to provide financial advice.
- **Citations**: Every valid answer provides a direct citation link to the specific fund's source URL.
- **Beautiful UI**: Built with Streamlit, the user interface simulates a modern, dark-themed AI assistant layout.

---

## Architecture Overview
The system relies on three primary components:
1. **Data Ingestion Pipeline**: (`src/ingestion/`) Scrapes the 15 URLs, extracts HTML and structured JSON-LD FAQ data, chunks it, and vectorizes it into ChromaDB using SentenceTransformers (`all-MiniLM-L6-v2`).
2. **Guardrail Middleware**: (`src/guardrails/`) Evaluates incoming user queries using the Groq API. Identifies if the prompt is asking for advice, casual chat, or PII.
3. **RAG Pipeline**: (`src/rag/`) Retrieves the top-K relevant chunks from ChromaDB and passes them to LLaMA-3.1 to generate a constrained response.

*(See `architecture.md` for deeper technical details).*

---

## Setup & Installation

### 1. Prerequisites
- Python 3.11+
- Virtual Environment (`venv` or `conda`)

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
# Required for model access
GROQ_API_KEY=your_groq_api_key_here

# (Optional) Embedding model local path/cache
HF_HOME=./.cache/huggingface
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage Guide

### 1. Run Data Ingestion
Before running the bot, you must populate the vector database by scraping the mutual fund data.
```bash
python -m src.ingestion.pipeline
```
This process takes ~30 seconds and will create a `data/chroma` directory containing your embeddings.

### 2. Start the Application
Run the Streamlit frontend.
```bash
streamlit run ui/app.py
```
Open your browser at `http://localhost:8501`.

---

## Testing & Validation

The project includes a robust test suite covering guardrails, constraints, retrieval accuracy, and system load.

Run unit tests:
```bash
pytest
```

Evaluate Retrieval Hit Rate (Golden Dataset):
```bash
python tests/eval_retrieval.py
```

Run concurrent Load Test:
```bash
python tests/load_test.py
```

## Constraints Imposed
- **3-Sentence Rule**: LLM prompts strictly enforce a 3-sentence constraint.
- **No Investment Advice**: Refusals are handled at the middleware layer.
- **Citation formatting**: Formatting layer strictly appends one unique URL.

## Disclaimer
Facts-only. No investment advice. Please consult a registered financial advisor or visit official AMFI/SEBI resources.

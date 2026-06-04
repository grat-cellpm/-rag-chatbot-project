# System Architecture: Mutual Fund FAQ Assistant

## 1. High-Level Architecture Overview
The system follows a standard **Retrieval-Augmented Generation (RAG)** architecture, enhanced with strict guardrails to ensure compliance with the facts-only constraints. 

The architecture is divided into three main pipelines:
1. **Data Ingestion Pipeline**: Scrapes, processes, and indexes the 15 specified HSBC Mutual Fund URLs.
2. **Query Processing & Guardrails**: Intercepts user queries to classify them as factual vs. advisory.
3. **Retrieval & Generation Pipeline**: Fetches relevant context and generates a concise, constrained response.

---

## 2. Data Ingestion Pipeline
Since the corpus is strictly limited to 15 URLs from Groww, the ingestion pipeline will be lightweight.

- **Scheduler**: A cron job or task scheduling mechanism that triggers the ingestion pipeline daily, ensuring the vector database is always synced with the latest facts and dates.
- **Web Scraper/Loader**: A module (e.g., using BeautifulSoup or Playwright) to fetch the HTML content from the 15 specific Groww URLs.
- **Data Cleaner**: Removes boilerplate HTML, navbars, and ads, extracting only the relevant scheme data (Expense ratio, Exit load, Fund management, etc.).
- **Text Chunker**: Splits the extracted text into smaller, semantically meaningful chunks (e.g., using a RecursiveCharacterTextSplitter) to ensure accurate retrieval.
- **Embedding Model**: Converts the text chunks into dense vector representations using a model like OpenAI `text-embedding-3-small` or an open-source alternative (e.g., `BGE-m3`).
- **Vector Database**: A lightweight vector store (e.g., ChromaDB, FAISS, or Qdrant) to store the embeddings alongside their metadata (Source URL, Last Updated Date).

---

## 3. Query Processing & Guardrails (The Refusal Module)
Before searching the database, every user query must pass through a strict classification layer to prevent the assistant from providing investment advice.

- **Intent Classifier (LLM or Rule-based)**:
  - **Factual Queries** (e.g., "What is the exit load of HSBC Midcap Fund?"): Routed to the Retrieval Pipeline.
  - **Advisory/Opinion Queries** (e.g., "Should I invest in this fund?", "Which fund is better?"): Intercepted immediately.
- **Refusal Handler**: If a query is classified as advisory, the system bypasses retrieval and generation, immediately returning a standard refusal template:
  > *"I can only provide factual information about mutual fund schemes and cannot offer investment advice. For guidance, please consult a registered financial advisor or visit official AMFI/SEBI resources."*

---

## 4. Retrieval & Generation Pipeline
For valid, factual queries, the system retrieves context and constructs the response.

- **Semantic Search (Retriever)**: Embeds the user's query and performs a cosine similarity search against the Vector Database to fetch the top-k most relevant chunks.
- **Prompt Builder**: Constructs a strict prompt for the LLM. The prompt will include:
  1. The user's query.
  2. The retrieved context chunks.
  3. **System Instructions**:
     - Do not use outside knowledge.
     - Keep the answer to a maximum of 3 sentences.
     - State the facts clearly without any marketing language.
- **Generation Model (LLM)**: An LLM (e.g., GPT-3.5-Turbo, GPT-4o-mini, or Claude 3 Haiku) generates the final text based *only* on the provided prompt and context.

---

## 5. Post-Processing & Formatting
Before displaying the result to the user, the system ensures all output constraints are met:

- **Constraint Checker**: Truncates or flags the response if it exceeds 3 sentences.
- **Citation Injector**: Appends exactly **one** citation link (derived from the metadata of the retrieved chunk).
- **Footer Appender**: Appends the mandatory footer: `“Last updated from sources: <date>”`.

---

## 6. User Interface (Minimal)
A lightweight frontend (e.g., built with Streamlit, Gradio, or a basic React app) that provides:
1. **Welcome Message & Disclaimer**: Prominently displaying *“Facts-only. No investment advice.”*
2. **Quick-Start Prompts**: Three clickable example questions (e.g., "What is the expense ratio for HSBC Small Cap Fund?").
3. **Chat Interface**: A simple input box and message history limited to the current session (no PII collection or persistent chat history).

---

## 7. Security & Privacy Layer
- **No PII Logging**: The system explicitly drops and does not log any patterns matching PAN, Aadhaar, account numbers, or contact details.
- **Stateless Execution**: The backend processes queries statelessly without storing user profiles or long-term session IDs.

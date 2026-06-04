# Implementation Plan: Mutual Fund FAQ Assistant

## 1. Objective
Build a robust, facts-only Retrieval-Augmented Generation (RAG) assistant for querying mutual fund information based on a curated set of 15 Groww URLs. The system aims to provide accurate, concise, and verifiable factual data while strictly refusing any advisory queries, adhering to high standards of reliability, scalability, security, and maintainability.

---

## 2. Phase-wise Plan

### Phase 1: Project Setup & Foundation
**Goal**: Establish the development environment, repository structure, and core dependencies to ensure a maintainable and scalable codebase.
**Tasks**:
- Initialize project repository with a standard, modular directory structure (e.g., `/data`, `/src`, `/ui`, `/tests`, `/docs`).
- Set up Git version control and define a branching strategy (e.g., GitFlow).
- Configure a Python virtual environment (e.g., `poetry` or `pipenv`) for robust dependency management.
- Install and pin core dependencies (`langchain`, `chromadb`, `groq`, `beautifulsoup4`, `streamlit`, `pytest`).
- Implement configuration management using `.env` files and environment validation (e.g., `pydantic-settings`) for secure API key handling.
- Setup pre-commit hooks for code linting, formatting (e.g., `black`, `ruff`), and type checking (`mypy`).
**Expected Deliverables**:
- A properly structured, version-controlled repository.
- `pyproject.toml` or `requirements.txt` with locked dependencies.
- Initialized environment configuration templates.

### Phase 2: Data Ingestion & Storage Pipeline
**Goal**: Build a scalable and reliable data pipeline to scrape, clean, chunk, and embed data from the 15 specific URLs, incorporating strict deduplication and data validation.
**Tasks**:
- Develop a robust web scraper with automated error handling, retries, and appropriate rate-limiting.
- Implement data cleaning modules to strip HTML boilerplate, ads, and isolate purely factual content.
- **Data Validation**: Add automated validation checks to ensure extracted data meets expected schemas (e.g., verifying the presence of numerical values for Expense Ratio or Exit Load).
- Implement `RecursiveCharacterTextSplitter` for semantic and context-aware text chunking.
- **Deduplication**: Implement hashing mechanisms (e.g., SHA-256) on chunks to prevent duplicate vector ingestion during subsequent runs.
- Generate embeddings (e.g., `text-embedding-3-small`) and upsert into the Vector DB (ChromaDB), including rich metadata (Source URL, Last Updated Date, Hash).
**Expected Deliverables**:
- Automated, resilient scraping and ingestion scripts.
- Populated, validated, and deduplicated Vector Database instance.

### Phase 3: Daily Scheduler Integration
**Goal**: Automate the data ingestion pipeline to keep information up to date, ensuring high system reliability and observability.
**Tasks**:
- Refactor the ingestion logic into a modular, stateless, and runnable function.
- Configure a reliable scheduler (e.g., standard `cron`, GitHub Actions, or Airflow for future scalability) to trigger the ingestion pipeline every 24 hours.
- Implement robust structural logging (e.g., using Python's `logging` or `structlog`) to capture scraping statistics, chunk counts, and system errors.
- Set up monitoring and alerting mechanisms (e.g., email notifications or Slack webhooks) to notify engineering teams of ingestion failures.
**Expected Deliverables**:
- Scheduled daily ingestion job.
- Centralized logging configuration and alerting integration.

### Phase 4: Query Guardrails & Refusal Module
**Goal**: Enforce strict "facts-only" constraints and maintain application security by filtering sensitive information and proactively handling advisory intents.
**Tasks**:
- Build an intent classification router (using zero-shot classification or a specialized lightweight LLM prompt) to distinguish "Factual" from "Advisory" queries.
- Implement a deterministic Refusal Handler that overrides the generation pipeline and returns: *"Facts-only. No investment advice. Please consult a registered financial advisor or visit official AMFI/SEBI resources."*
- Integrate PII filtering using regex patterns and specialized libraries (e.g., Microsoft Presidio) to mask/drop sensitive inputs (PAN, Aadhaar, account numbers).
**Expected Deliverables**:
- Functional intent classification module.
- Hardcoded, compliant refusal system.
- PII and security filtering pipeline.

### Phase 5: RAG Pipeline (Retrieval & Generation)
**Goal**: Retrieve the most relevant context and generate concise, factual responses with strict formatting, including graceful fallback handling.
**Tasks**:
- Implement semantic search logic to query the Vector DB and retrieve the top-k most relevant chunks.
- **Fallback Handling**: Implement a similarity score threshold. If top retrieved chunks fall below this threshold (i.e., information not found), trigger a graceful fallback response: *"The requested information is not available in the current knowledge base."*
- Design and version-control a strict LLM generation prompt enforcing:
  - Maximum output length: 3 sentences.
  - Strict adherence to using the provided context ONLY.
- Develop a post-processing formatting module to guarantee exactly **one citation link** and append the mandatory footer: `“Last updated from sources: <date>”`.
**Expected Deliverables**:
- Fully functional, integrated RAG backend module.
- Version-controlled prompt templates.
- Output formatting and fallback post-processor.

### Phase 6: Minimal User Interface
**Goal**: Develop a clean, responsive, and minimal interface for end users to interact seamlessly with the backend assistant.
**Tasks**:
- Initialize a Streamlit (or Gradio) web application architecture.
- Design the UI layout to prominently feature the mandatory disclaimer: *“Facts-only. No investment advice.”*
- Implement and style at least three clickable example queries for quick user onboarding.
- Integrate the chat interface with the RAG backend, handling asynchronous network calls, loading states, and streaming responses (if applicable).
- Ensure the UI handles and displays backend errors, rate limits, or timeouts gracefully to the user.
**Expected Deliverables**:
- Deployed, interactive, and responsive web interface.

### Phase 7: Testing, Validation & Documentation
**Goal**: Ensure the end-to-end system meets all functional, non-functional, and compliance requirements before final delivery.
**Tasks**:
- **Retrieval Validation & Testing**: Create a "golden dataset" of queries and contexts. Evaluate retrieval effectiveness using formal metrics like Mean Reciprocal Rank (MRR) or Hit Rate.
- Conduct rigorous constraint testing to prove the 3-sentence limit, single link citation, and footer rules are never broken under edge cases.
- Run guardrail testing against a suite of adversarial and advisory queries.
- Perform load testing to assess application stability and response latency under concurrent requests.
- Compile final project documentation (`README.md`, API specs, architecture diagrams).
**Expected Deliverables**:
- Comprehensive automated test suite (unit and integration tests).
- Evaluation report for retrieval and generation accuracy.
- Complete technical and operational documentation.

---

## 3. Success Metrics

To objectively evaluate the performance, compliance, and reliability of the Mutual Fund FAQ Assistant, the following metrics will be tracked:

- **Response Accuracy**: Percentage of generated responses that are 100% factual, free of hallucinations, and strictly derived from the provided context (Target: > 98%).
- **Retrieval Accuracy (Hit Rate / MRR)**: The frequency and rank with which the correct factual chunk is retrieved in the top-k results from the Vector DB (Target: > 95%).
- **Citation Coverage**: Percentage of factual responses that correctly include exactly one valid and relevant citation link to the source material (Target: 100%).
- **Refusal Accuracy**: The system's precision and recall in successfully identifying and refusing advisory, conversational, or out-of-domain queries (Target: > 99%).
- **Response Latency**: End-to-end time taken from user query submission to complete response generation (Target: < 2.5 seconds per query on average, at the 95th percentile).
- **Pipeline Freshness/Uptime**: Percentage of days the scheduled data ingestion pipeline successfully runs, validates, and updates the vector database without critical failure (Target: 99.9% uptime).

---

## 4. Final Deliverables

1. **Source Code**: A well-documented, modular, and cleanly structured Python codebase hosted in a version-controlled repository (e.g., GitHub), complete with CI/CD configurations.
2. **Automated Data Pipeline**: A deployed, scheduled job responsible for robust data scraping, data validation, deduplication, and Vector DB ingestion.
3. **Web Application**: A functional, minimal, and responsive user interface accessible via a web browser.
4. **Testing & Evaluation Report**: A formal document detailing the results of the golden dataset retrieval testing, constraint validation, guardrail effectiveness, and latency benchmarks.
5. **Technical Documentation**: A comprehensive `README.md` and architecture document outlining local setup instructions, environment configuration, system flow, deployment steps, and known limitations.

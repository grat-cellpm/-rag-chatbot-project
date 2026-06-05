# Railway Deployment Plan

This document outlines the standard operating procedure for deploying the **Groww AI - Mutual Fund Assistant** application to Railway.

## Architecture Context

Currently, the application runs as a **Monolithic Application** powered by Streamlit (`ui/app.py`). The Streamlit application directly imports and invokes the backend logic (`src/rag/pipeline.py` and `src/guardrails/middleware.py`). 

Because of this monolithic design, both the frontend and backend are deployed together as a single service on Railway.

## Prerequisites

1. **GitHub Account**: Your codebase must be pushed to a repository on GitHub.
2. **Railway Account**: You must have an account on [Railway.app](https://railway.app/).
3. **Environment Variables**: You must have your production API keys ready (e.g., `GROQ_API_KEY`).
4. **Procfile**: The repository must contain a `Procfile` in the root directory to instruct Railway how to start the Streamlit server. 
   - *Note: This has already been created in the repository.*
   - Contents of `Procfile`: `web: streamlit run ui/app.py --server.port $PORT --server.address 0.0.0.0`

---

## Deployment Steps

### Phase 1: Code Preparation
1. Ensure all your latest changes are committed.
2. Ensure the `Procfile` and `requirements.txt` are tracked in git and pushed to your main branch on GitHub.

### Phase 2: Railway Project Setup
1. Log in to [Railway](https://railway.app/).
2. From the dashboard, click on **New Project**.
3. Select **Deploy from GitHub repo**.
4. Search for and select your repository (`Rag chatbot project`).
5. Click **Deploy Now**.
   - *Railway will use Nixpacks to automatically detect the Python environment via `requirements.txt` and the startup command via the `Procfile`.*

### Phase 3: Environment Configuration
While the initial build is happening (it will likely fail on the first run if API keys are missing):
1. Click on the newly created **Service** block in your Railway project diagram.
2. Navigate to the **Variables** tab.
3. Click **New Variable** and add all secrets from your local `.env` file.
   - Example: 
     - **VARIABLE_NAME**: `GROQ_API_KEY`
     - **VALUE**: `<your-api-key>`
4. Railway will automatically trigger a new deployment to apply these variables.

### Phase 4: Network Exposure
By default, Railway services do not have public endpoints.
1. In the same Service block, navigate to the **Settings** tab.
2. Scroll down to the **Networking** section.
3. Click **Generate Domain**.
4. Railway will provide a public URL (e.g., `https://your-app-name.up.railway.app`).

---

## Troubleshooting

### Build Failures
If the build phase fails, check the **Deploy Logs** on Railway. Common issues include:
- A missing dependency in `requirements.txt`.
- Syntax errors preventing Python from starting.

### Application Crashes
If the build succeeds but the app crashes during runtime, check the **App Logs**. Common issues include:
- Missing Environment Variables (e.g., the app tries to initialize an LLM but the `GROQ_API_KEY` is not set).
- Incorrect file paths (ensure all file paths in the code use relative paths rather than absolute local paths).

### Port Binding Issues
If the app starts but Railway marks it as "Crashed" because it couldn't detect an active port, ensure the `Procfile` strictly uses `--server.port $PORT --server.address 0.0.0.0`. Railway dynamically assigns `$PORT` at runtime, and Streamlit must bind to it.

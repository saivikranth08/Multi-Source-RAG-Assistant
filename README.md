# 💬 Multi-Source RAG Assistant

An industry-grade Retrieval-Augmented Generation (RAG) system capable of ingesting diverse data sources—including digital PDFs, scanned/image PDFs (OCR), text files, and web URLs. It features hybrid search (dense + sparse), Cohere reranking, Postgres-backed conversation history, a LangGraph-orchestrated workflow state machine, and a gorgeous glassmorphic analytics dashboard.

---

## 🏗️ Flow Architecture

```mermaid
graph TD
    User([User UI]) -->|Upload PDF, OCR, Web URL, TXT| API[FastAPI Backend]
    User -->|Ask Question| API
    API -->|1. Ingest & Chunk| Embeddings[HuggingFace Embeddings]
    Embeddings -->|2. Store Vectors| Qdrant[(Qdrant Vector DB)]
    API -->|3. Run Query Graph| LangGraph{LangGraph Orchestrator}
    
    subgraph LangGraph Nodes
        LangGraph --> Retrieve[1. Retrieve Node]
        Retrieve --> Dense[Dense Search] & Sparse[BM25 Sparse Search]
        Dense & Sparse --> CohereRerank[Cohere Rerank API]
        CohereRerank --> BuildPrompt[2. Build Prompt Node]
        BuildPrompt --> Generate[3. Generate Node]
    end
    
    Generate -->|llama-3.1-8b-instant| Groq[Groq LLM API]
    Groq -->|Response| API
    API -->|4. Log Session History| Postgres[(PostgreSQL DB)]
    API -->|5. Return Answer & Sources| User
```

---

## ✨ Features

- **📂 Multi-Source Ingestion Engine:**
  - **Standard PDFs:** PyPDF extracts text instantly.
  - **Scanned/Image PDFs:** Deep OCR powered by **LlamaParse** converts complex pages & tables into structured markdown.
  - **Text Files:** Standard raw text files stream with UTF-8 safety.
  - **Web URLs:** Scrapes and processes clean webpage content via BeautifulSoup.
- **🔍 Advanced Retrieval Pipeline:**
  - **Hybrid Search:** Combines dense semantic vectors (Qdrant) and sparse keyword matches (BM25) with custom weighting (60/40) for high precision.
  - **State-of-the-Art Reranking:** Filters and optimizes retrieved candidate chunks using the Cohere Rerank API (`rerank-english-v3.0`).
- **🧠 LangGraph State Machine:** Multi-node deterministic RAG workflow (`retrieve` -> `prompt` -> `generate`) structured as a clean state-machine.
- **💾 Persistent DB Conversational Memory:** Customized database-backed history using **SQLAlchemy** and **PostgreSQL** to maintain context across sessions.
- **📊 Glassmorphic Dashboards:**
  - **Main Assistant App:** Glassmorphic sidebars, drag-and-drop document uploaders, session controllers, and dynamic resource expandable drawers.
  - **Live Analytics App:** Dynamic charting cards showing **Total Queries**, **Avg Latency Speed**, and **Error Rates**.

---

## 🛠️ Tech Stack

- **Core Frameworks:** FastAPI (Backend API), Streamlit (Frontend UIs)
- **RAG & Agentics:** LangChain, LangGraph, LlamaParse
- **Vector Search:** Qdrant (In-Memory Collection Client)
- **Database & Persistence:** PostgreSQL, SQLAlchemy
- **Embeddings & LLMs:** HuggingFace `all-MiniLM-L6-v2` (Local), Groq `llama-3.1-8b-instant`
- **Reranker:** Cohere Rerank API (`rerank-english-v3.0`)
- **Tracing & Evaluation:** LangSmith / LangChain Tracing

---

## 📁 Directory Structure

```
MultiSource_RAG/
├── backend/
│   ├── analytics/     # Query & latency telemetry
│   ├── api/           # FastAPI application endpoints
│   ├── database/      # PostgreSQL connection and SQLAlchemy schema
│   ├── graph/         # LangGraph workflow state machine definitions
│   ├── ingestion/     # Parsers for PDFs, Scanned files (OCR), text & web pages
│   ├── llm/           # Groq client instantiation & system prompt variables
│   ├── retrieval/     # Embedding loads, chunk splitters, Qdrant stores, Cohere rerankers
│   └── utils/         # Configuration variables and log handlers
├── frontend/
│   ├── app.py         # Main glassmorphic chat application
│   └── simple_analytics.py # Quick analytics live dashboard
├── docker-compose.yml # PostgreSQL instance provisioning
├── requirements.txt   # Core app dependencies
└── .env               # API keys & Database connection strings
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ and Docker Desktop installed.

### 2. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory and populate it with your API keys:
```env
GROQ_API_KEY=your_groq_api_key
LLAMA_CLOUD_API_KEY=your_llamaparse_api_key
COHERE_API_KEY=your_cohere_api_key

# Database Connectivity
# Default values matching docker-compose.yml
DATABASE_URL=postgresql://raguser:ragpassword@localhost:5432/ragdb

# Optional Tracing (LangSmith)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=MultiSource_RAG
```

### 3. Spin Up the Database
Start the containerized PostgreSQL database using Docker Compose:
```bash
docker-compose up -d
```

### 4. Install Dependencies
Set up your virtual environment and install all packages:
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 5. Run the Backend API
Start the FastAPI server via Uvicorn:
```bash
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```

### 6. Run the Frontend Applications
In two separate terminals, run the Streamlit apps:
* **Start RAG Chat UI:**
  ```bash
  streamlit run frontend/app.py
  ```
* **Start Quick Analytics Dashboard:**
  ```bash
  streamlit run frontend/simple_analytics.py
  ```

---

## ⚡ API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/upload/pdf` | Upload standard digital PDF, clear vector store, build semantic index |
| `POST` | `/upload/scanned-pdf` | Upload scanned PDF, parse using LlamaParse OCR, update semantic index |
| `POST` | `/upload/text` | Upload and process standard UTF-8 text file |
| `POST` | `/upload/url` | Scrape and ingest a webpage URL |
| `POST` | `/query` | Orchestrate LangGraph execution context and return prompt response with sources |
| `GET` | `/history/{session_id}` | Fetch session history string |
| `DELETE` | `/clear/{session_id}` | Clear message history database records for session |
| `DELETE` | `/clear/all` | Purge entire postgres conversational history |
<div align="center">

# 💬 Multi-Source RAG Assistant

![RAG System](https://img.shields.io/badge/RAG-System-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge&logo=streamlit)

An **industry-grade Retrieval-Augmented Generation (RAG) system** capable of ingesting diverse data sources—including digital PDFs, scanned/image PDFs (OCR), text files, and web URLs. Features hybrid search (dense + sparse), Cohere reranking, Postgres-backed conversation history, LangGraph-orchestrated workflow, and a gorgeous glassmorphic analytics dashboard.

[Features](#-features) • [Architecture](#-architecture) • [Tech Stack](#-tech-stack) • [Getting Started](#-getting-started) • [API Reference](#-api-reference)

</div>

---

## 🎯 Features

<table>
<tr>
<td width="50%">

### 📂 Multi-Source Ingestion
- **Standard PDFs** - PyPDF instant text extraction
- **Scanned/Image PDFs** - Deep OCR via LlamaParse
- **Text Files** - UTF-8 safe streaming
- **Web URLs** - BeautifulSoup scraping

</td>
<td width="50%">

### 🔍 Advanced Retrieval
- **Hybrid Search** - Dense + Sparse (60/40 weighting)
- **Cohere Reranking** - `rerank-english-v3.0`
- **High Precision** - Optimized candidate filtering
- **BM25 Integration** - Keyword matching

</td>
</tr>
<tr>
<td width="50%">

### 🧠 Intelligent Orchestration
- **LangGraph State Machine** - Deterministic workflow
- **Multi-Node Pipeline** - Retrieve → Prompt → Generate
- **Groq LLM** - `llama-3.1-8b-instant`
- **LangSmith Tracing** - Full observability

</td>
<td width="50%">

### 💾 Persistent Memory
- **PostgreSQL Backend** - Conversation history
- **SQLAlchemy ORM** - Clean data modeling
- **Session Management** - Cross-session context
- **Analytics Telemetry** - Query & latency tracking

</td>
</tr>
</table>

---

## 🏗️ Architecture

```mermaid
graph TB
    subgraph Client["👤 Client Layer"]
        UI["🎨 Streamlit Chat UI<br/><small>Glassmorphic Interface</small>"]
        Analytics["📊 Analytics Dashboard<br/><small>Real-time Metrics</small>"]
    end
    
    subgraph API["⚡ API Gateway Layer"]
        FastAPI["FastAPI Server<br/><small>Port 8000</small>"]
    end
    
    subgraph Ingestion["📥 Document Ingestion Pipeline"]
        direction LR
        PDF["📄 PDF Parser<br/><small>PyPDF</small>"]
        OCR["🔍 OCR Engine<br/><small>LlamaParse</small>"]
        TXT["📝 Text Parser<br/><small>UTF-8</small>"]
        WEB["🌐 Web Scraper<br/><small>BeautifulSoup</small>"]
    end
    
    subgraph Embedding["🧬 Embedding Layer"]
        HF["🤗 HuggingFace<br/><small>all-MiniLM-L6-v2</small>"]
        Chunker["✂️ Text Splitter<br/><small>Recursive Chunking</small>"]
    end
    
    subgraph Orchestration["🧠 RAG Orchestration - LangGraph"]
        direction TB
        LG["🔄 State Machine"]
        N1["1️⃣ Retrieve Node<br/><small>Hybrid Search</small>"]
        N2["2️⃣ Prompt Builder<br/><small>Context Assembly</small>"]
        N3["3️⃣ Generate Node<br/><small>LLM Response</small>"]
        
        LG --> N1 --> N2 --> N3
    end
    
    subgraph Search["🔍 Search & Ranking Layer"]
        direction LR
        Dense["🎯 Dense Search<br/><small>Semantic Vectors</small>"]
        Sparse["🔤 Sparse Search<br/><small>BM25 Keywords</small>"]
        Rerank["⭐ Cohere Rerank<br/><small>v3.0 API</small>"]
        
        Dense --> Rerank
        Sparse --> Rerank
    end
    
    subgraph Storage["💾 Storage Layer"]
        Qdrant[("🗄️ Qdrant<br/><small>Vector Database</small>")]
        Postgres[("🐘 PostgreSQL<br/><small>Conversation History</small>")]
    end
    
    subgraph AI["🤖 AI Services"]
        Groq["🚀 Groq LLM<br/><small>llama-3.1-8b-instant</small>"]
        LangSmith["📈 LangSmith<br/><small>Tracing & Monitoring</small>"]
    end
    
    UI --> FastAPI
    Analytics --> FastAPI
    
    FastAPI --> PDF & OCR & TXT & WEB
    PDF & OCR & TXT & WEB --> Chunker
    Chunker --> HF
    HF --> Qdrant
    
    FastAPI --> LG
    N1 --> Dense & Sparse
    Rerank --> N2
    N3 --> Groq
    
    Dense -.-> Qdrant
    Sparse -.-> Qdrant
    
    Groq --> FastAPI
    FastAPI --> Postgres
    FastAPI -.-> LangSmith
    
    FastAPI --> UI & Analytics
    
    classDef clientStyle fill:#667eea,stroke:#764ba2,stroke-width:3px,color:#fff
    classDef apiStyle fill:#f093fb,stroke:#f5576c,stroke-width:3px,color:#fff
    classDef ingestionStyle fill:#4facfe,stroke:#00f2fe,stroke-width:2px,color:#fff
    classDef embeddingStyle fill:#43e97b,stroke:#38f9d7,stroke-width:2px,color:#fff
    classDef orchestrationStyle fill:#fa709a,stroke:#fee140,stroke-width:3px,color:#fff
    classDef searchStyle fill:#30cfd0,stroke:#330867,stroke-width:2px,color:#fff
    classDef storageStyle fill:#a8edea,stroke:#fed6e3,stroke-width:3px,color:#333
    classDef aiStyle fill:#ff9a56,stroke:#ff6a88,stroke-width:2px,color:#fff
    
    class UI,Analytics clientStyle
    class FastAPI apiStyle
    class PDF,OCR,TXT,WEB ingestionStyle
    class HF,Chunker embeddingStyle
    class LG,N1,N2,N3 orchestrationStyle
    class Dense,Sparse,Rerank searchStyle
    class Qdrant,Postgres storageStyle
    class Groq,LangSmith aiStyle
```

---

## 🛠️ Tech Stack

<table>
<tr>
<td align="center" width="16.66%">
<img src="https://cdn.worldvectorlogo.com/logos/fastapi.svg" width="65" height="65"><br>
<b>FastAPI</b><br>
<sub>Backend API</sub>
</td>
<td align="center" width="16.66%">
<img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="65" height="65"><br>
<b>Streamlit</b><br>
<sub>Frontend UI</sub>
</td>
<td align="center" width="16.66%">
<img src="https://avatars.githubusercontent.com/u/126733545?s=200&v=4" width="65" height="65"><br>
<b>LangChain</b><br>
<sub>RAG Framework</sub>
</td>
<td align="center" width="16.66%">
<img src="https://avatars.githubusercontent.com/u/126733545?s=200&v=4" width="65" height="65"><br>
<b>LangGraph</b><br>
<sub>Orchestration</sub>
</td>
<td align="center" width="16.66%">
<img src="https://avatars.githubusercontent.com/u/132372032?s=200&v=4" width="65" height="65"><br>
<b>LangSmith</b><br>
<sub>Observability</sub>
</td>
<td align="center" width="16.66%">
<img src="https://avatars.githubusercontent.com/u/91993427?s=200&v=4" width="65" height="65"><br>
<b>Qdrant</b><br>
<sub>Vector DB</sub>
</td>
</tr>
<tr>
<td align="center" width="16.66%">
<img src="https://cdn.worldvectorlogo.com/logos/postgresql.svg" width="65" height="65"><br>
<b>PostgreSQL</b><br>
<sub>Persistence</sub>
</td>
<td align="center" width="16.66%">
<img src="https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png" width="75" height="65"><br>
<b>Docker</b><br>
<sub>Containerization</sub>
</td>
<td align="center" width="16.66%">
<img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" width="65" height="65"><br>
<b>HuggingFace</b><br>
<sub>Embeddings</sub>
</td>
<td align="center" width="16.66%">
<img src="https://avatars.githubusercontent.com/u/161824701?s=200&v=4" width="65" height="65"><br>
<b>Groq</b><br>
<sub>LLM Inference</sub>
</td>
<td align="center" width="16.66%">
<img src="https://cohere.com/favicon-32x32.png" width="65" height="65"><br>
<b>Cohere</b><br>
<sub>Reranking</sub>
</td>
<td align="center" width="16.66%">
<img src="https://avatars.githubusercontent.com/u/62400072?s=200&v=4" width="65" height="65"><br>
<b>LlamaParse</b><br>
<sub>OCR Engine</sub>
</td>
</tr>
</table>

### Technology Breakdown

| Category | Technologies |
|----------|-------------|
| **🎨 Frontend** | Streamlit (Glassmorphic UI) |
| **⚡ Backend** | FastAPI, Uvicorn |
| **🧠 RAG Framework** | LangChain, LangGraph (State Machine) |
| **🔍 Vector Search** | Qdrant (In-Memory), BM25 Sparse Retrieval |
| **💾 Database** | PostgreSQL, SQLAlchemy ORM |
| **🧬 Embeddings** | HuggingFace `all-MiniLM-L6-v2` (384-dim) |
| **🤖 LLM** | Groq `llama-3.1-8b-instant` |
| **⭐ Reranking** | Cohere `rerank-english-v3.0` |
| **📄 OCR** | LlamaParse Cloud API |
| **📈 Observability** | LangSmith Tracing & Monitoring |
| **🐳 Infrastructure** | Docker Compose |

---

## 📁 Project Structure

```
MultiSource_RAG/
│
├── 🔧 backend/
│   ├── 📊 analytics/          # Query & latency telemetry
│   ├── ⚡ api/                 # FastAPI endpoints
│   ├── 💾 database/            # PostgreSQL + SQLAlchemy
│   ├── 🧠 graph/               # LangGraph state machine
│   ├── 📥 ingestion/           # Multi-source parsers
│   ├── 🤖 llm/                 # Groq client & prompts
│   ├── 🔍 retrieval/           # Embeddings, Qdrant, reranking
│   └── 🛠️ utils/               # Config & logging
│
├── 🎨 frontend/
│   ├── app.py                 # Main chat interface
│   └── simple_analytics.py    # Analytics dashboard
│
├── 🐳 docker-compose.yml       # PostgreSQL container
├── 📦 requirements.txt         # Python dependencies
└── 🔐 .env                     # Environment variables
```

---

## 🚀 Getting Started

### Prerequisites

<table>
<tr>
<td>

```bash
# Required
Python 3.10+
Docker Desktop
```

</td>
<td>

```bash
# API Keys Needed
Groq API Key
LlamaParse API Key
Cohere API Key
```

</td>
</tr>
</table>

### 1️⃣ Environment Configuration

Create a `.env` file in the root directory:

```env
# 🤖 AI Service Keys
GROQ_API_KEY=your_groq_api_key
LLAMA_CLOUD_API_KEY=your_llamaparse_api_key
COHERE_API_KEY=your_cohere_api_key

# 💾 Database Configuration
DATABASE_URL=postgresql://raguser:ragpassword@localhost:5432/ragdb

# 📊 Optional: LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=MultiSource_RAG
```

### 2️⃣ Database Setup

```bash
# Start PostgreSQL container
docker-compose up -d
```

### 3️⃣ Install Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 4️⃣ Launch Backend

```bash
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```

### 5️⃣ Launch Frontend

Run the following commands in two separate terminal shells:

* **Terminal 1 — Main Chat Interface:**
  ```bash
  streamlit run frontend/app.py
  ```
* **Terminal 2 — Analytics Dashboard:**
  ```bash
  streamlit run frontend/simple_analytics.py
  ```

---

## ⚡ API Reference

### Endpoints Overview

<table>
<thead>
<tr>
<th width="10%">Method</th>
<th width="30%">Endpoint</th>
<th width="60%">Description</th>
</tr>
</thead>
<tbody>

<tr>
<td><code>POST</code></td>
<td><code>/upload/pdf</code></td>
<td>📄 Upload standard digital PDF and build semantic index</td>
</tr>

<tr>
<td><code>POST</code></td>
<td><code>/upload/scanned-pdf</code></td>
<td>🔍 Upload scanned PDF with LlamaParse OCR processing</td>
</tr>

<tr>
<td><code>POST</code></td>
<td><code>/upload/text</code></td>
<td>📝 Upload and process UTF-8 text file</td>
</tr>

<tr>
<td><code>POST</code></td>
<td><code>/upload/url</code></td>
<td>🌐 Scrape and ingest webpage content</td>
</tr>

<tr>
<td><code>POST</code></td>
<td><code>/query</code></td>
<td>🧠 Execute LangGraph workflow and return AI response with sources</td>
</tr>

<tr>
<td><code>GET</code></td>
<td><code>/history/{session_id}</code></td>
<td>📜 Retrieve conversation history for session</td>
</tr>

<tr>
<td><code>DELETE</code></td>
<td><code>/clear/{session_id}</code></td>
<td>🗑️ Clear specific session history</td>
</tr>

<tr>
<td><code>DELETE</code></td>
<td><code>/clear/all</code></td>
<td>💥 Purge all conversation history</td>
</tr>

</tbody>
</table>

---

## 📊 System Workflow

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant API as FastAPI
    participant LG as LangGraph
    participant VS as Vector Store
    participant LLM as Groq LLM
    participant DB as PostgreSQL

    User->>UI: Upload Document
    UI->>API: POST /upload/*
    API->>API: Parse & Chunk
    API->>VS: Store Embeddings
    API-->>UI: ✅ Success

    User->>UI: Ask Question
    UI->>API: POST /query
    API->>LG: Initialize Graph
    LG->>VS: Hybrid Search
    VS-->>LG: Top Candidates
    LG->>LG: Cohere Rerank
    LG->>LLM: Generate Response
    LLM-->>LG: Answer
    LG-->>API: Response + Sources
    API->>DB: Log Conversation
    API-->>UI: Display Answer
    UI-->>User: Show Results
```

---

## 🎨 UI Preview

<div align="center">

### Main Chat Interface
*Glassmorphic design with drag-and-drop document upload, session management, and expandable source citations*

### Analytics Dashboard
*Real-time metrics showing total queries, average latency, and error rates with dynamic charting*

</div>

---

## 📝 License

This project is available for educational and commercial use.

---

<div align="center">
 Built with ❤️ using LangChain, FastAPI, and Streamlit
⭐ Star this repo if you find it helpful!

</div>
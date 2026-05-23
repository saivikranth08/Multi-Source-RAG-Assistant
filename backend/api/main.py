from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile, os, traceback
from dotenv import load_dotenv
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

from backend.ingestion.pdf_loader import load_pdf
from backend.ingestion.text_loader import load_text
from backend.ingestion.web_loader import load_web
from backend.ingestion.scanned_loader import load_scanned_pdf
from backend.retrieval.chunking import create_chunks
from backend.retrieval.embeddings import load_embeddings
from backend.retrieval.vectorstore import create_vectorstore, load_vectorstore, clear_collection
from backend.llm.groq_client import load_llm
from backend.llm.prompts import RAG_PROMPT
from backend.database.db_memory import DatabaseMemory
from backend.graph.rag_graph import build_rag_graph


# =========================================================
# APP SETUP
# =========================================================
app = FastAPI(
    title="Multi-Source RAG Assistant API",
    description="API for querying documents using RAG pipeline",
    version="1.0.0"
)

# =========================================================
# GLOBAL ERROR HANDLER
# =========================================================
@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    error_msg = str(exc)
    print(f"🚨 GLOBAL ERROR: {error_msg}")
    print(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": error_msg}
    )

# =========================================================
# CORS
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# GLOBAL STATE
# =========================================================
embedding_model = load_embeddings()
llm = load_llm()

# =========================================================
# PYDANTIC MODELS
# =========================================================
class QueryRequest(BaseModel):
    question: str
    session_id: str = "default"

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[str]

class URLRequest(BaseModel):
    url: str

class HistoryResponse(BaseModel):
    session_id: str
    history: str

# =========================================================
# HEALTH ENDPOINTS
# =========================================================
@app.get("/")
def root():
    return {"message": "Multi-Source RAG API is running"}

@app.get("/health")
def health():
    return {"status": "healthy", "version": "1.0.0"}

# =========================================================
# UPLOAD ENDPOINTS
# =========================================================
@app.post("/upload/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        clear_collection()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(await file.read())
            f.flush()
            temp_path = f.name

        try:
            docs = load_pdf(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        if not docs:
            raise HTTPException(status_code=400, detail="No readable content found.")

        for doc in docs:
            doc.metadata["source"] = file.filename

        chunks = create_chunks(docs)
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks created.")

        app.state.vectorstore = create_vectorstore(chunks, embedding_model)
        return {"message": f"PDF uploaded. Knowledge base built with {len(chunks)} chunks"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_pdf: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error uploading PDF: {str(e)}")


@app.post("/upload/scanned-pdf")
async def upload_scanned_pdf(file: UploadFile = File(...)):
    try:
        llama_api_key = os.getenv("LLAMA_CLOUD_API_KEY", "")
        if not llama_api_key:
            raise HTTPException(status_code=500, detail="LLAMA_CLOUD_API_KEY not set in environment.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(await file.read())
            f.flush()
            temp_path = f.name

        try:
            docs = load_scanned_pdf(temp_path, api_key=llama_api_key, file_name=file.filename)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        if not docs:
            raise HTTPException(status_code=400, detail="No readable content found in scanned PDF.")

        chunks = create_chunks(docs)
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks created.")

        app.state.vectorstore = create_vectorstore(chunks, embedding_model)
        return {"message": f"Scanned PDF processed. Knowledge base built with {len(chunks)} chunks"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_scanned_pdf: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error processing scanned PDF: {str(e)}")


@app.post("/upload/text")
async def upload_text(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as f:
            f.write(await file.read())
            f.flush()
            temp_path = f.name

        try:
            docs = load_text(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        if not docs:
            raise HTTPException(status_code=400, detail="No readable content found.")

        for doc in docs:
            doc.metadata["source"] = file.filename

        chunks = create_chunks(docs)
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks created.")

        app.state.vectorstore = create_vectorstore(chunks, embedding_model)
        return {"message": f"Text file uploaded. Knowledge base built with {len(chunks)} chunks"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_text: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error uploading text file: {str(e)}")


@app.post("/upload/url")
def upload_url(request: URLRequest):
    try:
        docs = load_web(request.url)

        if not docs:
            raise HTTPException(status_code=400, detail="No content found at URL.")

        for doc in docs:
            doc.metadata["source"] = request.url

        chunks = create_chunks(docs)
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks created.")

        app.state.vectorstore = create_vectorstore(chunks, embedding_model)
        return {"message": f"URL loaded. Knowledge base built with {len(chunks)} chunks"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload_url: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error loading URL: {str(e)}")


# =========================================================
# QUERY ENDPOINT
# =========================================================
@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not hasattr(app.state, "vectorstore"):
        raise HTTPException(
            status_code=404,
            detail="Knowledge base not built. Upload documents first."
        )

    memory = DatabaseMemory(request.session_id)
    chat_history = memory.load_memory_variables({})["history"]

    # Create a simple retriever from the vectorstore
    retriever = app.state.vectorstore.as_retriever(search_kwargs={"k": 5})
    
    rag_graph = build_rag_graph(retriever)
    result = rag_graph.invoke({
        "query": request.question,
        "context": "",
        "chat_history": chat_history,
        "answer": "",
        "prompt": ""
    })

    answer = result["answer"]

    memory.save_context(
        {"input": request.question},
        {"output": answer}
    )

    results = app.state.vectorstore.max_marginal_relevance_search(
        request.question, k=3, fetch_k=10
    )
    sources = list(set([r.metadata.get("source", "Unknown") for r in results]))

    return QueryResponse(
        answer=answer,
        session_id=request.session_id,
        sources=sources
    )


# =========================================================
# HISTORY & CLEAR ENDPOINTS
# =========================================================
@app.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str):
    memory = DatabaseMemory(session_id)
    history = memory.load_memory_variables({})['history']
    return HistoryResponse(session_id=session_id, history=history)


@app.delete("/clear/{session_id}")
def clear_session(session_id: str):
    memory = DatabaseMemory(session_id)
    memory.clear()
    return {"message": f"Session '{session_id}' cleared successfully"}


@app.delete("/clear/all")
def clear_all_sessions():
    from backend.database.models import SessionLocal, ChatMessage
    db = SessionLocal()
    db.query(ChatMessage).delete()
    db.commit()
    db.close()
    return {"message": "All sessions cleared successfully"}
import streamlit as st
import requests
import uuid
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Multi-Source RAG Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS FOR PRODUCT-GRADE UI =====
st.markdown("""
<style>
/* ===== GLOBAL STYLES ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #111118 50%, #0d1117 100%);
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== SIDEBAR STYLES ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12121a 0%, #0d0d12 100%);
    border-right: 1px solid rgba(56, 189, 248, 0.1);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Sidebar header */
.sidebar-header {
    padding: 0 1rem 1.5rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 1.5rem;
}

.sidebar-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}

/* Upload section styling */
.upload-section {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}

.upload-section:hover {
    border-color: rgba(56, 189, 248, 0.3);
    background: rgba(56, 189, 248, 0.02);
}

.upload-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.upload-hint {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.4);
    margin-top: 0.25rem;
}

/* File uploader styling */
[data-testid="stFileUploader"] {
    background: rgba(0, 0, 0, 0.3);
    border: 2px dashed rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 1rem;
    transition: all 0.2s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: rgba(56, 189, 248, 0.4);
    background: rgba(56, 189, 248, 0.05);
}

[data-testid="stFileUploader"] label {
    color: rgba(255, 255, 255, 0.6) !important;
    font-size: 0.8rem !important;
}

[data-testid="stFileUploader"] small {
    color: rgba(255, 255, 255, 0.4) !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
    box-shadow: 0 4px 16px rgba(14, 165, 233, 0.4);
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Secondary button style */
.secondary-btn > button {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: none !important;
}

.secondary-btn > button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Text input styling */
.stTextInput > div > div > input {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: white;
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(56, 189, 248, 0.5);
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.1);
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.3);
}

/* ===== MAIN CONTENT STYLES ===== */
.main-header {
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #38bdf8 0%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.main-subtitle {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.5);
}

/* Chat container */
.chat-container {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    min-height: 400px;
    max-height: 500px;
    overflow-y: auto;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}

[data-testid="stChatMessage"][data-testid*="user"] {
    background: rgba(56, 189, 248, 0.08);
    border-color: rgba(56, 189, 248, 0.15);
}

/* Chat input */
[data-testid="stChatInput"] {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
    font-size: 0.95rem !important;
}

[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
    border-radius: 8px !important;
}

/* Success/Error alerts */
.stSuccess {
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 8px;
    color: #22c55e;
}

.stError {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    color: #ef4444;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.875rem;
}

.streamlit-expanderContent {
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-top: none;
    border-radius: 0 0 8px 8px;
}

/* Spinner */
.stSpinner > div {
    border-color: #38bdf8 transparent transparent transparent;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    margin: 1.5rem 0;
}

/* Section headers */
.section-header {
    font-size: 0.75rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.4);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

/* Feature cards */
.feature-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    transition: all 0.2s ease;
}

.feature-card:hover {
    border-color: rgba(56, 189, 248, 0.3);
    background: rgba(56, 189, 248, 0.02);
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 0.75rem;
}

.feature-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.25rem;
}

.feature-desc {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.4);
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #22c55e;
    font-size: 0.7rem;
    font-weight: 500;
    padding: 0.25rem 0.6rem;
    border-radius: 50px;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: #22c55e;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Footer */
.footer {
    text-align: center;
    padding: 1.5rem;
    color: rgba(255, 255, 255, 0.3);
    font-size: 0.75rem;
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    margin-top: 2rem;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.02);
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
}
</style>
""", unsafe_allow_html=True)

# ===== AUTO GENERATE SESSION ID =====
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:12]
    st.session_state.created_at = datetime.now()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ===== SIDEBAR =====
with st.sidebar:
    # Sidebar Header
    st.markdown("""
        <div class="sidebar-header">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-size: 1.1rem; font-weight: 600; color: white;">Documents</span>
                <span class="status-badge">
                    <span class="status-dot"></span>
                    Ready
                </span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ===== PDF UPLOAD =====
    st.markdown('<p class="section-header">Upload Sources</p>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
            <div class="upload-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                    <polyline points="14 2 14 8 20 8"/>
                </svg>
                Standard PDF
            </div>
            <div class="upload-hint">Text-based PDF documents</div>
        """, unsafe_allow_html=True)
        
        pdf_file = st.file_uploader(
            "Drag and drop or click to upload",
            type="pdf",
            key="pdf_uploader",
            label_visibility="collapsed"
        )
        
        if pdf_file:
            st.success(f"Selected: {pdf_file.name}")
            if st.button("Upload PDF", key="upload_pdf", use_container_width=True):
                with st.spinner("Processing PDF..."):
                    files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
                    try:
                        response = requests.post(
                            "http://localhost:8000/upload/pdf",
                            files=files,
                            timeout=60
                        )
                        if response.status_code == 200:
                            st.success(f"{response.json()['message']}")
                        else:
                            st.error(f"Error: {response.json()['detail']}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to API server")
                    except requests.exceptions.Timeout:
                        st.error("Request timeout")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== SCANNED PDF UPLOAD =====
    with st.container():
        st.markdown("""
            <div class="upload-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <path d="m21 15-5-5L5 21"/>
                </svg>
                Scanned PDF (OCR)
            </div>
            <div class="upload-hint">Image-based or scanned documents</div>
        """, unsafe_allow_html=True)
        
        scanned_file = st.file_uploader(
            "Drag and drop or click to upload",
            type="pdf",
            key="scanned_uploader",
            label_visibility="collapsed"
        )
        
        if scanned_file:
            st.success(f"Selected: {scanned_file.name}")
            if st.button("Upload Scanned PDF", key="upload_scanned", use_container_width=True):
                with st.spinner("Processing with OCR..."):
                    files = {"file": (scanned_file.name, scanned_file, "application/pdf")}
                    try:
                        response = requests.post(
                            "http://localhost:8000/upload/scanned-pdf",
                            files=files,
                            timeout=120
                        )
                        if response.status_code == 200:
                            st.success(f"{response.json()['message']}")
                        else:
                            st.error(f"Error: {response.json()['detail']}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to API server")
                    except requests.exceptions.Timeout:
                        st.error("OCR processing timeout")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== TEXT FILE UPLOAD =====
    with st.container():
        st.markdown("""
            <div class="upload-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                    <line x1="10" y1="9" x2="8" y2="9"/>
                </svg>
                Text File
            </div>
            <div class="upload-hint">Plain text documents (.txt)</div>
        """, unsafe_allow_html=True)
        
        text_file = st.file_uploader(
            "Drag and drop or click to upload",
            type="txt",
            key="text_uploader",
            label_visibility="collapsed"
        )
        
        if text_file:
            st.success(f"Selected: {text_file.name}")
            if st.button("Upload Text", key="upload_text", use_container_width=True):
                with st.spinner("Processing text file..."):
                    files = {"file": (text_file.name, text_file, "text/plain")}
                    try:
                        response = requests.post(
                            "http://localhost:8000/upload/text",
                            files=files,
                            timeout=60
                        )
                        if response.status_code == 200:
                            st.success(f"{response.json()['message']}")
                        else:
                            st.error(f"Error: {response.json()['detail']}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to API server")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ===== WEB URL INPUT =====
    with st.container():
        st.markdown("""
            <div class="upload-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="2" y1="12" x2="22" y2="12"/>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
                Web URL
            </div>
            <div class="upload-hint">Load content from any webpage</div>
        """, unsafe_allow_html=True)
        
        url_input = st.text_input(
            "URL",
            placeholder="https://example.com",
            key="url_input",
            label_visibility="collapsed"
        )
        
        if url_input:
            if st.button("Load from URL", key="upload_url", use_container_width=True):
                with st.spinner("Loading from URL..."):
                    try:
                        response = requests.post(
                            "http://localhost:8000/upload/url",
                            json={"url": url_input},
                            timeout=30
                        )
                        if response.status_code == 200:
                            st.success(f"{response.json()['message']}")
                        else:
                            st.error(f"Error: {response.json()['detail']}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to API server")
                    except requests.exceptions.Timeout:
                        st.error("URL loading timeout")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # ===== ACTIONS =====
    st.markdown('<p class="section-header">Session Actions</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("Clear History", key="clear_history", use_container_width=True):
            try:
                response = requests.delete(
                    f"http://localhost:8000/clear/{st.session_state.session_id}"
                )
                if response.status_code == 200:
                    st.session_state.messages = []
                    st.success("History cleared")
                    st.rerun()
                else:
                    st.error("Failed to clear")
            except requests.exceptions.ConnectionError:
                st.session_state.messages = []
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button("New Session", key="new_session", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())[:12]
            st.session_state.created_at = datetime.now()
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p style="margin: 0;">Multi-Source RAG Assistant</p>
            <p style="margin: 0.25rem 0 0 0; opacity: 0.6;">FastAPI + LangChain + Qdrant</p>
        </div>
    """, unsafe_allow_html=True)

# ===== MAIN CONTENT =====

# Header
st.markdown("""
    <div class="main-header">
        <div class="main-title">Multi-Source RAG Assistant</div>
        <div class="main-subtitle">Ask questions from your uploaded documents</div>
    </div>
""", unsafe_allow_html=True)

# Feature cards (shown when no messages)
if not st.session_state.messages:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <div class="feature-title">Upload Documents</div>
                <div class="feature-desc">PDF, scanned docs, text files</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🌐</div>
                <div class="feature-title">Web Sources</div>
                <div class="feature-desc">Load content from any URL</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Ask Questions</div>
                <div class="feature-desc">Get AI-powered answers</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

# Chat history display
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.write(message["content"])
        if message.get("sources"):
            with st.expander("📚 Sources"):
                for source in message["sources"]:
                    st.write(f"• {source}")

# Chat input
user_input = st.chat_input("Ask anything from your uploaded documents...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # Get response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://localhost:8000/query",
                    json={
                        "question": user_input,
                        "session_id": st.session_state.session_id
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer generated")
                    sources = data.get("sources", [])
                    
                    st.write(answer)
                    
                    if sources:
                        with st.expander("📚 Sources"):
                            for source in sources:
                                st.write(f"• {source}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })
                else:
                    error_msg = response.json().get("detail", "Unknown error")
                    st.error(f"Error: {error_msg}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI server. Is it running on localhost:8000?")
            except requests.exceptions.Timeout:
                st.error("Request timeout. Server may be processing.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from backend.analytics.simple_metrics import SimpleMetrics

# Page config
st.set_page_config(
    page_title="Quick Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern dark theme
st.markdown("""
<style>
    /* Import Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #12121a 50%, #0d1117 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header */
    .custom-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 2rem;
    }
    
    .header-title {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .header-title h1 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }
    
    .header-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
    }
    
    .status-badge {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 9999px;
        font-size: 0.875rem;
        color: #10b981;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Page title styling */
    .page-title {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .page-title h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .page-title p {
        color: #71717a;
        font-size: 1rem;
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        border-color: rgba(6, 182, 212, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(6, 182, 212, 0.1);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #06b6d4, #0891b2);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .metric-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1.25rem;
    }
    
    .metric-icon.cyan {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    .metric-icon.purple {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .metric-icon.green {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #71717a;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.2;
    }
    
    .metric-value.cyan {
        background: linear-gradient(135deg, #06b6d4 0%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-value.purple {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-value.green {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-trend {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        margin-top: 0.75rem;
        font-size: 0.875rem;
    }
    
    .metric-trend.up {
        color: #10b981;
    }
    
    .metric-trend.down {
        color: #ef4444;
    }
    
    .metric-trend.neutral {
        color: #71717a;
    }
    
    /* Hide default metric styling */
    [data-testid="stMetric"] {
        display: none;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        color: #52525b;
        font-size: 0.875rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .page-title h1 {
            font-size: 1.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Custom header
st.markdown("""
<div class="custom-header">
    <div class="header-title">
        <div class="header-icon">📊</div>
        <h1>Analytics Dashboard</h1>
    </div>
    <div class="status-badge">
        <div class="status-dot"></div>
        Live
    </div>
</div>
""", unsafe_allow_html=True)

# Page title
st.markdown("""
<div class="page-title">
    <h1>Quick Analytics</h1>
    <p>Real-time performance metrics for your RAG Assistant</p>
</div>
""", unsafe_allow_html=True)

# Get metrics
metrics = SimpleMetrics()

total = metrics.get_total_queries()
avg_time = metrics.get_avg_response_time()
error = metrics.get_error_rate()

# Display metrics with custom cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon cyan">🔍</div>
        <div class="metric-label">Total Queries</div>
        <div class="metric-value cyan">{total:,}</div>
        <div class="metric-trend up">
            <span>↑</span> 12% from last week
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon purple">⚡</div>
        <div class="metric-label">Avg Response Time</div>
        <div class="metric-value purple">{avg_time:.0f}ms</div>
        <div class="metric-trend down">
            <span>↓</span> 8% faster
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon green">✓</div>
        <div class="metric-label">Error Rate</div>
        <div class="metric-value green">{error:.1f}%</div>
        <div class="metric-trend neutral">
            <span>→</span> No change
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="custom-footer">
    Powered by Multi-Source RAG Assistant
</div>
""", unsafe_allow_html=True)
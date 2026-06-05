import streamlit as st
import os
import sys

# Inject Streamlit secrets into environment variables so backend catches it
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# Add project root to path robustly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..')) if os.path.basename(current_dir) == 'ui' else current_dir

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.guardrails.middleware import GuardrailMiddleware
from src.rag.pipeline import RAGPipeline

st.set_page_config(
    page_title="Groww AI - Mutual Fund Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_backend():
    middleware = GuardrailMiddleware()
    pipeline = RAGPipeline()
    return middleware, pipeline

middleware, pipeline = get_backend()

# Custom CSS for styling strictly matching the provided image
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Styles */
    :root {
        --bg-main: #0B141A;
        --bg-sidebar: #0B141A;
        --text-main: #FFFFFF;
        --text-muted: #94A3B8;
        --text-dark: #64748B;
        --accent: #10B981; 
        --accent-hover: #059669;
        --card-bg: #0F161C;
        --border-color: #1E293B;
    }

    * {
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-main);
        color: var(--text-main);
    }
    
    [data-testid="stHeader"] {
        background-color: transparent;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
    }
    
    /* Hide default sidebar stuff */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    .sidebar-logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 40px;
        padding-top: 10px;
    }
    
    .sidebar-logo-icon {
        background-color: #064E3B;
        border-radius: 8px;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .sidebar-logo-inner {
        width: 14px;
        height: 14px;
        border: 2px solid var(--accent);
        border-radius: 4px;
    }

    .sidebar-label {
        color: var(--text-dark);
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .sidebar-btn-active {
        background-color: var(--card-bg);
        border-right: 3px solid var(--accent);
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 12px;
        color: var(--accent);
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
    }

    .sidebar-nav-item {
        color: var(--text-muted);
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 16px;
        cursor: pointer;
    }
    
    .sidebar-nav-item:hover {
        color: var(--text-main);
    }

    .upgrade-btn-container {
        position: absolute;
        bottom: 20px;
        width: calc(100% - 40px);
        left: 20px;
    }

    .upgrade-btn {
        width: 100%;
        background: linear-gradient(90deg, #10B981, #059669);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 14px;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 12px;
        cursor: pointer;
        text-align: center;
    }
    
    .upgrade-subtext {
        color: var(--text-dark);
        font-size: 10px;
        text-align: center;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* Top Nav Styling */
    .top-nav {
        position: absolute;
        top: 20px;
        left: 20px;
        right: 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 100;
        padding-bottom: 20px;
    }
    
    /* Main Content Area */
    .hero-container {
        text-align: center;
        margin-top: 100px;
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-icon {
        width: 80px;
        height: 80px;
        border: 1px solid var(--border-color);
        border-radius: 20px;
        margin: 0 auto 30px auto;
        position: relative;
    }
    
    .hero-dot {
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 8px;
        height: 8px;
        background-color: var(--accent);
        border-radius: 50%;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 500;
        margin-bottom: 20px;
        line-height: 1.2;
    }
    
    .hero-title i {
        font-family: 'Georgia', serif;
        font-style: italic;
    }
    
    .hero-subtitle {
        color: var(--text-muted);
        font-size: 16px;
        margin-bottom: 8px;
    }

    .hero-subtext {
        color: var(--text-dark);
        font-size: 14px;
        margin-top: 20px;
    }

    /* AI Welcome Card */
    .welcome-card-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 60px;
        margin-bottom: 40px;
    }
    
    .welcome-card {
        display: flex;
        gap: 20px;
        max-width: 800px;
        width: 100%;
    }
    
    .ai-avatar {
        width: 40px;
        height: 40px;
        background-color: var(--border-color);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        color: var(--accent);
        font-size: 20px;
    }
    
    .ai-content {
        flex-grow: 1;
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        background-color: var(--card-bg);
    }
    
    .ai-text {
        color: var(--text-main);
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 30px;
    }
    
    /* Styled chips as Streamlit buttons */
    div.stButton > button {
        background-color: transparent !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--accent) !important;
        padding: 12px 20px !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        height: auto !important;
        box-shadow: none !important;
        transition: border-color 0.2s;
    }
    
    div.stButton > button:hover {
        border-color: var(--accent) !important;
    }

    /* Chat Input Styling */
    .stChatInputContainer {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 30px !important;
        padding: 4px 16px !important;
    }
    
    .stChatInputContainer:focus-within {
        border-color: var(--text-dark) !important;
    }

    /* Hide standard user icon in chat input */
    .stChatInputContainer svg {
        color: var(--text-main) !important;
    }
    
    /* Footer */
    .main-footer {
        position: fixed;
        bottom: 20px;
        width: 100%;
        text-align: center;
        pointer-events: none;
    }
    
    .main-footer-links {
        color: var(--text-dark);
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .main-footer-links span {
        margin: 0 15px;
        pointer-events: auto;
        cursor: pointer;
    }
    
    .main-footer-copyright {
        color: var(--text-dark);
        font-size: 9px;
        letter-spacing: 0.5px;
    }
    
    /* Adjust main block padding to push content down from absolute header */
    .block-container {
        padding-top: 3rem !important;
    }

</style>
""", unsafe_allow_html=True)

# Top Navigation Bar (Absolute Positioned via CSS)
st.markdown("""
<div class="top-nav">
    <div style="color: #64748B; font-size: 13px; font-weight: 600; letter-spacing: 1px;">PORTFOLIO ASSISTANT</div>
    <div style="display: flex; align-items: center; gap: 24px;">
        <span style="color: #94A3B8; font-size: 18px; cursor: pointer;">↺</span>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="color: #94A3B8; font-size: 13px; text-align: right; line-height: 1.2;">
                Alex<br>Rivera
            </div>
            <div style="background-color: #1E293B; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #94A3B8;">
                👤
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo-container">
        <div class="sidebar-logo-icon">
            <div class="sidebar-logo-inner"></div>
        </div>
        <div>
            <div style="color: white; font-weight: bold; font-size: 18px;">Groww <span style="font-weight: 800;">AI</span></div>
            <div style="color: #64748B; font-size: 10px; letter-spacing: 1px;">INTELLIGENCE</div>
        </div>
    </div>
    
    <div class="sidebar-label">WORKSPACE</div>
    <div class="sidebar-btn-active">
        <span>+</span>
        <span>New Session</span>
    </div>

    <div class="sidebar-label">ANALYTICS</div>
    <div style="display: flex; flex-direction: column; gap: 16px;">
        <div class="sidebar-nav-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
            Market View
        </div>
        <div class="sidebar-nav-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="M10 4v4"></path><path d="M2 8h20"></path><path d="M6 4v4"></path></svg>
            Assets
        </div>
        <div class="sidebar-nav-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
            Preferences
        </div>
        <div class="sidebar-nav-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"></path><path d="M5 21V7l8-4v18"></path><path d="M19 21V11l-6-3"></path><path d="M9 9v.01"></path><path d="M9 13v.01"></path><path d="M9 17v.01"></path></svg>
            Direct Mutual Funds
        </div>
        <div class="sidebar-nav-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>
            ELSS Tax Strategy
        </div>
    </div>
    
    <div class="upgrade-btn-container">
        <div class="upgrade-btn">UPGRADE TO PRO</div>
        <div class="upgrade-subtext">PREMIUM ACCESS ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Using a state variable to hold triggered prompt from buttons
if "button_prompt" not in st.session_state:
    st.session_state.button_prompt = None

def set_prompt(q):
    st.session_state.button_prompt = q

if not st.session_state.messages:
    # Empty State Hero Section
    st.markdown("""
        <div class="hero-container">
            <div class="hero-icon">
                <div class="hero-dot"></div>
            </div>
            <h1 class="hero-title">Refining your <i>wealth</i><br>with precision.</h1>
            <p class="hero-subtitle">Your specialized advisor for Mutual Funds, SIP strategies, and</p>
            <p class="hero-subtitle">tax-efficient portfolio management.</p>
            <p class="hero-subtext">AFC-HSBC mutual funds</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown("""
        <div class="welcome-card-wrapper">
            <div class="welcome-card">
                <div class="ai-avatar">🤖</div>
                <div class="ai-content">
                    <p class="ai-text">
                        Greetings. I am your Groww AI assistant. I can analyze expense ratios, evaluate exit loads, or curate fund selections based on your risk profile.
                    </p>
    """, unsafe_allow_html=True)
    
    # Place buttons side by side inside the HTML block using columns
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        if st.button("Direct Mutual Funds", key="q1", use_container_width=True):
            st.session_state.button_prompt = "Tell me about HSBC direct mutual funds."
        if st.button("Expense Ratio", key="q3", use_container_width=True):
            st.session_state.button_prompt = "What is the expense ratio for HSBC Small Cap Fund?"
    with col2:
        if st.button("ELSS Tax Strategies", key="q2", use_container_width=True):
            st.session_state.button_prompt = "What is the HSBC Tax Saver Equity Fund and its lock-in period?"
        if st.button("Exit Load", key="q4", use_container_width=True):
            st.session_state.button_prompt = "What is the exit load for HSBC Midcap Fund?"
            
    st.markdown("""
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Inquire about funds, SIPs, or taxation...")

if st.session_state.button_prompt:
    prompt = st.session_state.button_prompt
    st.session_state.button_prompt = None

if prompt:
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                guard_result = middleware.process_query(prompt)
                if not guard_result["is_allowed"]:
                    response = guard_result["message"]
                else:
                    response = pipeline.answer_query(prompt)
            except Exception as e:
                response = f"Sorry, an error occurred while processing your request: {str(e)}"
        
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("""
<div class="main-footer">
    <div class="main-footer-links">
        <span>TERMS</span>
        <span>PRIVACY</span>
        <span>SUPPORT</span>
    </div>
    <div class="main-footer-copyright">
        © 2024 GROWW AI • PRECISION WEALTH MANAGEMENT
    </div>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import logging
from utils import check_backend_health
from components.search_interface import render_search_interface
from components.chat import render_chat_interface
from components.search_results import render_search_results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Semantic Search Engine", layout="wide")

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0E1117;
    }

    h1 { color: #FAFAFA; }
    h2, h3 { color: #E0E0E0; padding-bottom: 1rem;}

    [data-testid="stChatMessageContent"] {
        background-color: #1E293B;
        border-radius: 15px;
        padding: 12px;
    }
    [data-testid="stChatMessageContent"] p {
        color: #FAFAFA;
    }

    .card {
        background-color: #181E29;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #334155;
        transition: box-shadow 0.3s ease, border-color 0.3s ease;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card:hover {
        box-shadow: 0 4px 20px rgba(45, 212, 191, 0.2);
        border-color: #14B8A6;
    }
    .card-title {
        color: #14B8A6;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .card-brand {
        color: #FFFFFF;
        font-weight: bold;
    }

    .stButton > button, .stFormSubmitButton > button {
        border-radius: 20px;
        background-color: #14B8A6;
        color: #0E1117;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background-color: #0F766E;
        color: white;
    }

    div[data-testid="stModal"] {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: 9999;
    }
    div[data-testid="stModal"] > div:first-child {
        position: relative !important;
        width: 90%;
        max-width: 640px;
        transform: none !important;
        border-radius: 15px;
        background-color: #0E1117;
        border: 1px solid #334155;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if "searched" not in st.session_state:
    st.session_state.searched = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "products" not in st.session_state:
    st.session_state.products = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "backend_connected" not in st.session_state:
    st.session_state.backend_connected = check_backend_health()

logger.info(f"App started - Backend connected: {st.session_state.backend_connected}")

if not st.session_state.backend_connected:
    st.warning("⚠️ Backend API is not running. Please start the backend server first.")
    st.code("cd backend && python run_server.py")
    st.info("💡 Make sure to set your OPENAI_API_KEY in the backend/.env file")

if not st.session_state.searched:
    render_search_interface()
else:
    logger.info(f"Rendering search results view (session: {st.session_state.session_id})")

    chat_col, results_col = st.columns([1, 3])

    with chat_col:
        render_chat_interface(st.session_state.session_id)

    with results_col:
        render_search_results(st.session_state.products)
import streamlit as st
import time
import logging
from utils import start_chat_session

logger = logging.getLogger(__name__)

def render_search_interface():
    """Render the initial search interface"""
    logger.info("Rendering search interface")

    st.markdown("<h1 style='text-align: center; margin-top: 5rem;'>Semantic Search</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("search_form"):
            search_query = st.text_input("Search", placeholder="Looking to Search...", label_visibility="collapsed")
            submit_button = st.form_submit_button("Search", use_container_width=True)

            if submit_button and search_query:
                logger.info(f"Search submitted: '{search_query}'")

                loading_placeholder = st.empty()
                with loading_placeholder:
                    st.markdown("🔍 **Starting AI-powered search...**")

                with st.spinner("Connecting to AI assistant..."):
                    chat_response = start_chat_session(search_query)

                loading_placeholder.empty()

                if chat_response:
                    logger.info(f"Chat session started successfully: {chat_response.get('session_id')}")

                    st.session_state.searched = True
                    st.session_state.session_id = chat_response["session_id"]
                    st.session_state.messages = [
                        {"role": "user", "content": search_query},
                        {"role": "assistant", "content": chat_response["initial_message"]["content"]}
                    ]

                    from data import get_fake_products
                    st.session_state.products = get_fake_products(search_query)

                    st.rerun()
                else:
                    logger.error("Failed to start chat session")
                    st.error("❌ Failed to start search session. Please check the backend connection and try again.")
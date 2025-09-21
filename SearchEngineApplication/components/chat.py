import streamlit as st
import time
import logging
from utils import send_chat_message

logger = logging.getLogger(__name__)

def simulate_streaming_response(text: str, placeholder) -> None:
    """Simulate streaming response by displaying text word by word"""
    words = text.split()
    displayed_text = ""

    for word in words:
        displayed_text += word + " "
        placeholder.markdown(displayed_text + "▌")
        time.sleep(0.03)

    placeholder.markdown(displayed_text.strip())

def render_chat_interface(session_id: str = None) -> None:
    """Render the complete chat interface"""
    logger.info("Rendering chat interface")

    st.markdown("#### 💬 AI Assistant")

    if st.button("🔄 Reset Chat", use_container_width=True):
        logger.info("Reset chat button clicked")
        st.session_state.searched = False
        st.session_state.messages = []
        st.session_state.products = []
        st.session_state.session_id = None
        st.rerun()

    # Adjust chat container height to leave room for input
    chat_container = st.container(height=650, border=False)

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Fixed CSS for chat input and container positioning
    st.markdown("""
        <style>
        /* Fix chat container positioning */
        [data-testid="stVerticalBlock"] > div:has(.stChatInput) {
            position: sticky !important;
            bottom: 0 !important;
            background-color: #0E1117 !important;
            padding-top: 10px !important;
            z-index: 100 !important;
        }

        /* Chat input styling */
        .stChatInput textarea {
            min-height: 50px !important;
            border-radius: 20px !important;
            border: 2px solid #334155 !important;
            background-color: #1E293B !important;
            color: #FAFAFA !important;
            padding: 12px 16px !important;
            resize: vertical !important;
            max-height: 150px !important;
        }

        .stChatInput textarea:focus {
            border-color: #14B8A6 !important;
            background-color: #0F172A !important;
            box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.1) !important;
        }

        /* Ensure chat messages container doesn't overlap with input */
        .stChatInput {
            margin-top: 10px !important;
            margin-bottom: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if prompt := st.chat_input("Ask about products, compare items, get recommendations..."):
        logger.info(f"User entered prompt: '{prompt}'")

        st.session_state.messages.append({"role": "user", "content": prompt})

        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        if not session_id:
            logger.error("No session ID available for chat")
            error_message = "❌ Chat session not available. Please start a new search."
            st.session_state.messages.append({"role": "assistant", "content": error_message})

            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(error_message)
            st.rerun()
            return

        with st.spinner("🤖 Getting AI response..."):
            chat_response = send_chat_message(session_id, prompt)

        if chat_response:
            assistant_content = chat_response["assistant_response"]["content"]
            logger.info(f"Received assistant response (length: {len(assistant_content)})")

            with chat_container:
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    simulate_streaming_response(assistant_content, response_placeholder)

            st.session_state.messages.append({"role": "assistant", "content": assistant_content})
        else:
            error_message = "❌ I'm having trouble connecting to the AI service. Please check the backend server and try again."
            logger.error("Failed to get assistant response")

            with chat_container:
                with st.chat_message("assistant"):
                    st.markdown(error_message)

            st.session_state.messages.append({"role": "assistant", "content": error_message})

        st.rerun()
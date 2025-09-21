import requests
import streamlit as st
import logging
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_URL = "http://localhost:8000"

def start_chat_session(query: str, user_id: str = None) -> Optional[Dict]:
    """Start a new chat session with the backend"""
    try:
        logger.info(f"Starting chat session for query: '{query}'")

        response = requests.post(
            f"{BACKEND_URL}/chat/start",
            json={"query": query, "user_id": user_id},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            logger.info(f"Chat session started successfully: {result.get('session_id')}")
            return result
        else:
            error_msg = f"Backend returned status {response.status_code}"
            logger.error(error_msg)
            st.error(f"❌ {error_msg}")
            return None

    except requests.exceptions.ConnectException:
        error_msg = "Cannot connect to backend server. Please ensure the backend is running."
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except requests.exceptions.Timeout:
        error_msg = "Request timed out. The backend server might be overloaded."
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None

def send_chat_message(session_id: str, message: str, user_id: str = None) -> Optional[Dict]:
    """Send a message to an existing chat session"""
    try:
        logger.info(f"Sending message to session {session_id}: '{message}'")

        response = requests.post(
            f"{BACKEND_URL}/chat/message",
            json={"session_id": session_id, "message": message, "user_id": user_id},
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            logger.info(f"Message sent successfully to session {session_id}")
            return result
        elif response.status_code == 404:
            error_msg = "Chat session not found. Please start a new conversation."
            logger.error(error_msg)
            st.error(f"❌ {error_msg}")
            return None
        else:
            error_msg = f"Backend returned status {response.status_code}"
            logger.error(error_msg)
            st.error(f"❌ {error_msg}")
            return None

    except requests.exceptions.ConnectException:
        error_msg = "Cannot connect to backend server. Please ensure the backend is running."
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except requests.exceptions.Timeout:
        error_msg = "Request timed out. The backend server might be overloaded."
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        st.error(f"❌ {error_msg}")
        return None

def check_backend_health() -> bool:
    """Check if the backend server is running and healthy"""
    try:
        logger.info("Checking backend health")

        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        is_healthy = response.status_code == 200

        if is_healthy:
            logger.info("Backend is healthy")
        else:
            logger.warning(f"Backend health check failed with status {response.status_code}")

        return is_healthy

    except requests.exceptions.RequestException:
        logger.warning("Backend health check failed - server not reachable")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking backend health: {str(e)}")
        return False
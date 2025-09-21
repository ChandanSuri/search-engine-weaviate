import uuid
import logging
from datetime import datetime
from typing import Dict, List
from models import ChatMessage, ChatSession
from client import openai_client

logger = logging.getLogger(__name__)

def generate_session_id() -> str:
    """Generate a unique session ID"""
    session_id = str(uuid.uuid4())
    logger.debug(f"Generated new session ID: {session_id}")
    return session_id

def create_system_prompt() -> str:
    """Create the system prompt for the search engine chatbot"""
    return """You are an intelligent search engine assistant. Your role is to:

1. Help users find products and information based on their queries
2. Provide detailed explanations about search results
3. Compare products and make recommendations
4. Answer follow-up questions about items found
5. Be conversational and helpful

When a user starts a search, acknowledge their query and explain what kind of results you'll help them find. For follow-up questions, provide detailed, helpful responses about the products or search topic.

Keep responses concise but informative, and always maintain a friendly, helpful tone."""

async def process_chat_start(query: str, user_id: str = None) -> Dict:
    """
    Process the initial chat start request
    """
    try:
        logger.info(f"Processing chat start for query: '{query}' (user: {user_id})")

        session_id = generate_session_id()
        system_prompt = create_system_prompt()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"I want to search for: {query}"}
        ]

        response_data = await openai_client.create_response(messages)

        initial_message = ChatMessage(
            role="assistant",
            content=response_data["content"],
            timestamp=datetime.now(),
            response_id=response_data["response_id"]
        )

        user_message = ChatMessage(
            role="user",
            content=query,
            timestamp=datetime.now()
        )

        chat_session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            messages=[user_message, initial_message],
            created_at=datetime.now(),
            last_updated=datetime.now()
        )

        logger.info(f"Chat session created successfully: {session_id}")
        logger.debug(f"Initial response length: {len(response_data['content'])}")

        return {
            "session": chat_session,
            "response_id": response_data["response_id"],
            "usage": response_data.get("usage")
        }

    except Exception as e:
        logger.error(f"Error processing chat start: {str(e)}")
        raise

async def process_chat_message(
    session: ChatSession,
    message: str,
    user_id: str = None
) -> Dict:
    """
    Process a new message in an existing chat session
    """
    try:
        logger.info(f"Processing message in session {session.session_id}: '{message}' (user: {user_id})")

        user_message = ChatMessage(
            role="user",
            content=message,
            timestamp=datetime.now()
        )

        system_prompt = create_system_prompt()
        openai_messages = [{"role": "system", "content": system_prompt}]

        recent_messages = session.messages[-10:] if len(session.messages) > 10 else session.messages
        logger.debug(f"Using {len(recent_messages)} recent messages for context")

        for msg in recent_messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })

        openai_messages.append({
            "role": "user",
            "content": message
        })

        previous_response_id = None
        if session.messages:
            last_assistant_message = next(
                (msg for msg in reversed(session.messages) if msg.role == "assistant"),
                None
            )
            if last_assistant_message and last_assistant_message.response_id:
                previous_response_id = last_assistant_message.response_id

        response_data = await openai_client.create_response(
            openai_messages,
            previous_response_id=previous_response_id
        )

        assistant_response = ChatMessage(
            role="assistant",
            content=response_data["content"],
            timestamp=datetime.now(),
            response_id=response_data["response_id"],
            previous_response_id=previous_response_id
        )

        session.messages.extend([user_message, assistant_response])
        session.last_updated = datetime.now()

        logger.info(f"Message processed successfully in session {session.session_id}")
        logger.debug(f"Assistant response length: {len(response_data['content'])}")

        return {
            "user_message": user_message,
            "assistant_response": assistant_response,
            "usage": response_data.get("usage")
        }

    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise

def validate_session_request(session_id: str, chat_sessions: Dict) -> ChatSession:
    """
    Validate and retrieve a chat session
    """
    if not session_id:
        logger.warning("Session ID not provided")
        raise ValueError("Session ID is required")

    if session_id not in chat_sessions:
        logger.warning(f"Session not found: {session_id}")
        raise ValueError(f"Chat session {session_id} not found")

    logger.debug(f"Session {session_id} validated successfully")
    return chat_sessions[session_id]
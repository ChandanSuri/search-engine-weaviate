import logging
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException
from models import (
    StartChatRequest, StartChatResponse, SendMessageRequest,
    SendMessageResponse
)
from helpers import process_chat_start, process_chat_message, validate_session_request

logger = logging.getLogger(__name__)

router = APIRouter()
chat_sessions: Dict = {}

@router.get("/")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint accessed")
    return {"message": "Search Engine Chat API is running", "status": "healthy"}

@router.post("/chat/start", response_model=StartChatResponse)
async def start_chat(request: StartChatRequest):
    """
    Start a new chat session with an initial search query
    """
    try:
        logger.info(f"Starting new chat session for query: '{request.query}'")

        result = await process_chat_start(request.query, request.user_id)
        session = result["session"]

        chat_sessions[session.session_id] = session

        logger.info(f"Chat session {session.session_id} stored successfully")

        return StartChatResponse(
            session_id=session.session_id,
            initial_message=session.messages[-1],
            response_id=result["response_id"],
            status="success"
        )

    except ValueError as e:
        logger.error(f"Validation error starting chat: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error starting chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start chat: {str(e)}")

@router.post("/chat/message", response_model=SendMessageResponse)
async def send_message(request: SendMessageRequest):
    """
    Send a message in an existing chat session
    """
    try:
        logger.info(f"Sending message to session {request.session_id}: '{request.message}'")

        session = validate_session_request(request.session_id, chat_sessions)

        result = await process_chat_message(session, request.message, request.user_id)

        chat_sessions[request.session_id] = session

        logger.info(f"Message sent successfully to session {request.session_id}")

        return SendMessageResponse(
            session_id=request.session_id,
            user_message=result["user_message"],
            assistant_response=result["assistant_response"],
            status="success"
        )

    except ValueError as e:
        logger.error(f"Validation error sending message: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.get("/chat/{session_id}")
async def get_chat_session(session_id: str):
    """
    Get chat session details and message history
    """
    try:
        logger.info(f"Retrieving chat session: {session_id}")

        session = validate_session_request(session_id, chat_sessions)

        logger.info(f"Chat session {session_id} retrieved successfully")
        return session

    except ValueError as e:
        logger.error(f"Error retrieving chat session: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/chat/{session_id}")
async def delete_chat_session(session_id: str):
    """
    Delete a chat session
    """
    try:
        logger.info(f"Deleting chat session: {session_id}")

        validate_session_request(session_id, chat_sessions)
        del chat_sessions[session_id]

        logger.info(f"Chat session {session_id} deleted successfully")
        return {"message": "Chat session deleted successfully", "status": "success"}

    except ValueError as e:
        logger.error(f"Error deleting chat session: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/chat/sessions/list")
async def list_chat_sessions(user_id: Optional[str] = None):
    """
    List all chat sessions, optionally filtered by user_id
    """
    try:
        logger.info(f"Listing chat sessions (user_id: {user_id})")

        if user_id:
            filtered_sessions = {
                sid: session for sid, session in chat_sessions.items()
                if session.user_id == user_id
            }
            logger.info(f"Found {len(filtered_sessions)} sessions for user {user_id}")
            return {"sessions": filtered_sessions, "count": len(filtered_sessions)}

        logger.info(f"Returning all {len(chat_sessions)} sessions")
        return {"sessions": chat_sessions, "count": len(chat_sessions)}

    except Exception as e:
        logger.error(f"Error listing chat sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to list sessions: {str(e)}")

@router.get("/chat/{session_id}/responses")
async def get_conversation_responses(session_id: str):
    """
    Get all responses for a conversation using OpenAI Responses API
    """
    try:
        logger.info(f"Getting conversation responses for session: {session_id}")

        session = validate_session_request(session_id, chat_sessions)

        if hasattr(session, 'conversation_id') and session.conversation_id:
            from client import openai_client
            responses = await openai_client.list_conversation_responses(
                conversation_id=session.conversation_id
            )
            logger.info(f"Retrieved {len(responses)} responses from OpenAI")
            return {"responses": responses, "count": len(responses)}
        else:
            logger.warning(f"No conversation_id found for session {session_id}")
            return {"responses": [], "count": 0, "message": "No conversation ID available"}

    except ValueError as e:
        logger.error(f"Error getting conversation responses: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting conversation responses: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get responses: {str(e)}")
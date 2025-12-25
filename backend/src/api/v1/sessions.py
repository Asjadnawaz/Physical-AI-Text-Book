from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
from ...models.chat_session import ChatSession
from ...services.chat_service import ChatService


router = APIRouter()
chat_service = ChatService()


@router.post("/chat/start")
async def start_chat(
    page_url: Optional[str] = None,
    user_context: Optional[Dict[str, Any]] = None
):
    """
    Start a new chat session
    """
    try:
        session = chat_service.create_session(
            page_url=page_url or "",
            user_context=user_context or {}
        )
        return {
            "session_id": session.id,
            "message": "Chat session started successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting chat session: {str(e)}")


@router.get("/chat/{session_id}/history")
async def get_chat_history(session_id: str):
    """
    Get chat session history
    """
    try:
        messages = chat_service.get_session_history(session_id)
        if not messages:
            raise HTTPException(status_code=404, detail="Session not found")

        return {
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat(),
                    "sources": msg.sources if msg.role == "assistant" else []
                }
                for msg in messages
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from ...models.message import Message
from ...services.chat_service import ChatService


router = APIRouter()
chat_service = ChatService()


@router.post("/chat/{session_id}/message")
async def send_message(
    session_id: str,
    content: str,
    selected_text: Optional[str] = None
):
    """
    Send a message in the chat session
    """
    try:
        response = chat_service.process_user_message(
            session_id=session_id,
            content=content,
            selected_text=selected_text or ""
        )
        return {
            "response": response.response_text,
            "sources": response.sources,
            "confidence": response.confidence_score
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
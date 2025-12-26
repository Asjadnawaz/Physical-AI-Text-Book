from fastapi import APIRouter, HTTPException, Depends, Path
from typing import Optional
from pydantic import Body
from ...models.message import Message
from ...services.chat_service import ChatService


router = APIRouter()
chat_service = ChatService()


@router.post("/chat/{session_id}/message",
             summary="Send a message in the chat session",
             description="Sends a user message to the chatbot and returns an AI-generated response based on textbook content. Optionally includes selected text for contextual queries.",
             response_description="The chatbot's response with sources and confidence score")
async def send_message(
    session_id: str = Path(..., description="The unique identifier of the chat session"),
    content: str = Body(..., description="The user's message content", example="What is Physical AI?"),
    selected_text: Optional[str] = Body(None, description="Text selected by the user for contextual queries", example="Physical AI challenges the traditional view of intelligence as computation divorced from physical reality.")
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
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    """
    Represents a single message in a chat conversation
    """
    id: str
    session_id: str
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    sources: List[str] = []
    selected_text: Optional[str] = None
    citations: List[dict] = []
    retrieved_chunks: List[str] = []

    class Config:
        # Allow the model to work properly with datetime objects
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
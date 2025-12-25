from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message


class ChatSession(BaseModel):
    """
    Represents a user's conversation with the chatbot, including message history and context
    """
    id: str
    user_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List['Message'] = []
    metadata: dict = {}

    def add_message(self, message: 'Message'):
        """Add a message to the session"""
        self.messages.append(message)
        self.updated_at = datetime.now()
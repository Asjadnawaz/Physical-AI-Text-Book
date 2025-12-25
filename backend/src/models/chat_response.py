from datetime import datetime
from typing import List
from pydantic import BaseModel


class ChatResponse(BaseModel):
    """
    The AI-generated response to the user's query, including citations to textbook sections
    """
    id: str
    query_id: str
    response_text: str
    sources: List[str]  # Citations to textbook sections used in the response
    timestamp: datetime
    confidence_score: float  # Confidence level in the response accuracy (0.0 to 1.0)
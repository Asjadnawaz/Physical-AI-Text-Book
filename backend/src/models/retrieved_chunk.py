from typing import List, Optional
from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    """
    A segment of textbook content retrieved based on semantic similarity to the user's query
    """
    id: str
    textbook_page: str
    content: str
    embedding: List[float] = []
    similarity_score: float  # Between 0.0 and 1.0
    metadata: dict = {}

    class Config:
        # Allow the model to work properly with lists of floats
        arbitrary_types_allowed = True
from datetime import datetime
from typing import List
from pydantic import BaseModel


class UserQuery(BaseModel):
    """
    The input from the user, including selected text context if applicable
    """
    id: str
    session_id: str
    query_text: str
    selected_text: str = ""
    timestamp: datetime
    processed_chunks: List[str] = []  # IDs of RetrievedChunk that were used to answer this query
from datetime import datetime
from typing import List
from pydantic import BaseModel


class TextbookContent(BaseModel):
    """
    Represents the processed textbook content that is available for retrieval
    """
    id: str
    page_path: str  # Path to the textbook page (e.g., "/chapter-1/section-1")
    section_title: str
    content: str
    chunk_index: int  # Position of this chunk within the page
    embedding: List[float] = []  # Vector representation of the content
    created_at: datetime
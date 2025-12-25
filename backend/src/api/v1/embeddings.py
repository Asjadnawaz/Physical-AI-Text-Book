from fastapi import APIRouter, HTTPException
from typing import Optional
from ...services.textbook_content_service import TextbookContentService


router = APIRouter()
content_service = TextbookContentService()


@router.post("/embeddings/chunk")
async def process_textbook_chunk(
    page_path: str,
    content: str,
    section_title: Optional[str] = None
):
    """
    Process textbook content for embedding
    """
    try:
        # In a real implementation, this would process and store the content
        # For now, we'll just return a success message
        # The actual processing would be done by the content service

        # Generate a mock content ID
        import uuid
        content_id = str(uuid.uuid4())

        # Store in the retrieval service
        from ...services.retrieval_service import RetrievalService
        retrieval_service = RetrievalService()
        retrieval_service.store_textbook_content(
            content_id=content_id,
            content=content,
            page_path=page_path,
            section_title=section_title or ""
        )

        return {
            "message": "Content processed and stored successfully",
            "chunk_count": 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing content: {str(e)}")
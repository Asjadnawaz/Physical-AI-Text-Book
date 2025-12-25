from fastapi import APIRouter, HTTPException
from typing import Optional
from ...services.retrieval_service import RetrievalService


router = APIRouter()
retrieval_service = RetrievalService()


@router.post("/search")
async def semantic_search(
    query: str,
    max_results: Optional[int] = 5
):
    """
    Perform semantic search in textbook content
    """
    try:
        retrieved_chunks = retrieval_service.retrieve_relevant_content(query)

        # Limit results if needed
        if max_results and max_results > 0:
            retrieved_chunks = retrieved_chunks[:max_results]

        results = [
            {
                "content": chunk.content,
                "page_path": chunk.textbook_page,
                "section_title": chunk.metadata.get("section_title", ""),
                "similarity_score": chunk.similarity_score
            }
            for chunk in retrieved_chunks
        ]

        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")
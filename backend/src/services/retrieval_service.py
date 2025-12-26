from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http import models
from ..models.retrieved_chunk import RetrievedChunk
from ..config.settings import settings
from .embedding_service import EmbeddingService


class RetrievalService:
    """
    Service for retrieving relevant textbook content based on user queries
    """

    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.embedding_service = EmbeddingService()
        self.collection_name = settings.QDRANT_COLLECTION
        self.max_results = settings.MAX_RETRIEVAL_RESULTS

        # Initialize the collection if it doesn't exist
        self._init_collection()

    def _init_collection(self):
        """
        Initialize the Qdrant collection for storing textbook content embeddings
        """
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=1536,  # Size of embedding vectors
                    distance=models.Distance.COSINE
                )
            )

    def store_textbook_content(self, content_id: str, content: str, page_path: str, section_title: str = ""):
        """
        Store textbook content with its embedding in the vector database
        """
        # Generate embedding for the content
        embedding = self.embedding_service.generate_embedding(content)

        # Prepare metadata
        metadata = {
            "page_path": page_path,
            "section_title": section_title,
            "content_id": content_id
        }

        # Store in Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=content_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        "page_path": page_path,
                        "section_title": section_title,
                        "content_id": content_id
                    }
                )
            ]
        )

    def retrieve_relevant_content(self, query: str) -> List[RetrievedChunk]:
        """
        Retrieve relevant textbook content based on the query
        """
        # Generate embedding for the query
        query_embedding = self.embedding_service.generate_embedding(query)

        # Search in Qdrant
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=self.max_results,
            with_payload=True
        )

        # Convert results to RetrievedChunk objects and apply validation/filtering
        retrieved_chunks = []
        for result in search_results:
            payload = result.payload

            # Basic validation: ensure content is meaningful
            content = payload.get("content", "")
            if not content or len(content.strip()) < 10:  # Skip very short or empty content
                continue

            # Filter based on similarity score threshold (e.g., only return results with score > 0.1)
            similarity_score = float(result.score)
            if similarity_score < 0.1:  # Minimum relevance threshold
                continue

            chunk = RetrievedChunk(
                id=result.id,
                textbook_page=payload.get("page_path", ""),
                content=content,
                embedding=[],  # We don't need the full embedding in the response
                similarity_score=similarity_score,
                metadata={
                    "section_title": payload.get("section_title", ""),
                    "content_id": payload.get("content_id", "")
                }
            )
            retrieved_chunks.append(chunk)

        # Sort by similarity score in descending order
        retrieved_chunks.sort(key=lambda x: x.similarity_score, reverse=True)

        return retrieved_chunks

    def retrieve_content_by_page(self, page_path: str) -> List[RetrievedChunk]:
        """
        Retrieve all content chunks for a specific textbook page
        """
        # Search in Qdrant with a filter for the specific page
        search_results = self.client.search(
            collection_name=self.collection_name,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="page_path",
                        match=models.MatchValue(value=page_path)
                    )
                ]
            ),
            limit=100,  # Retrieve up to 100 chunks for the page
            with_payload=True
        )

        # Convert results to RetrievedChunk objects
        retrieved_chunks = []
        for result in search_results:
            payload = result.payload
            chunk = RetrievedChunk(
                id=result.id,
                textbook_page=payload.get("page_path", ""),
                content=payload.get("content", ""),
                embedding=[],  # We don't need the full embedding in the response
                similarity_score=float(result.score),
                metadata={
                    "section_title": payload.get("section_title", ""),
                    "content_id": payload.get("content_id", "")
                }
            )
            retrieved_chunks.append(chunk)

        return retrieved_chunks
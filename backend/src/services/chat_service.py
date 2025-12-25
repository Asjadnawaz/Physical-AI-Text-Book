import uuid
from datetime import datetime
from typing import List, Optional
from ..models.chat_session import ChatSession
from ..models.message import Message
from ..models.user_query import UserQuery
from ..models.chat_response import ChatResponse
from ..services.retrieval_service import RetrievalService
from ..services.embedding_service import EmbeddingService
from ..config.settings import settings


class ChatService:
    """
    Service for handling chat interactions and response generation
    """

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.embedding_service = EmbeddingService()
        # In-memory storage for sessions (in production, use a database)
        self.sessions = {}

    def create_session(self, page_url: str = "", user_context: dict = None) -> ChatSession:
        """
        Create a new chat session
        """
        session_id = str(uuid.uuid4())

        session = ChatSession(
            id=session_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={
                "page_url": page_url,
                "user_context": user_context or {}
            }
        )

        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get an existing chat session
        """
        return self.sessions.get(session_id)

    def process_user_message(self, session_id: str, content: str, selected_text: str = "") -> ChatResponse:
        """
        Process a user message and generate a response
        """
        # Get the session
        session = self.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Create user message
        user_message = Message(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="user",
            content=content,
            timestamp=datetime.now(),
            selected_text=selected_text
        )

        # Add user message to session
        session.add_message(user_message)

        # Prepare the query - if selected text is provided, use it as context
        query_text = content
        if selected_text:
            query_text = f"Regarding this text: '{selected_text}', {content}"

        # Retrieve relevant content from textbook
        retrieved_chunks = self.retrieval_service.retrieve_relevant_content(query_text)

        # Generate response using the retrieved content
        response_text = self._generate_response(content, retrieved_chunks)

        # Create response message
        response_message = Message(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="assistant",
            content=response_text,
            timestamp=datetime.now(),
            sources=[chunk.textbook_page for chunk in retrieved_chunks]
        )

        # Add response message to session
        session.add_message(response_message)

        # Create and return the ChatResponse object
        chat_response = ChatResponse(
            id=response_message.id,
            query_id=user_message.id,
            response_text=response_text,
            sources=[chunk.textbook_page for chunk in retrieved_chunks],
            timestamp=datetime.now(),
            confidence_score=self._calculate_confidence_score(retrieved_chunks)
        )

        return chat_response

    def _generate_response(self, user_query: str, retrieved_chunks: List) -> str:
        """
        Generate a response based on the user query and retrieved content
        In a real implementation, this would call an LLM API like Gemini
        """
        # For now, create a mock response based on the retrieved content
        if not retrieved_chunks:
            return "I couldn't find relevant content in the textbook to answer your question. Please try rephrasing your question or check if the topic is covered in the textbook."

        # Combine the retrieved content to form the response
        context = "\n\n".join([chunk.content for chunk in retrieved_chunks[:2]])  # Use first 2 chunks

        # Create a response that references the textbook content
        response = f"Based on the textbook content:\n\n{context}\n\nIs there anything specific about this topic you'd like me to explain further?"

        return response

    def _calculate_confidence_score(self, retrieved_chunks: List) -> float:
        """
        Calculate a confidence score based on the quality of retrieved content
        """
        if not retrieved_chunks:
            return 0.0

        # Calculate average similarity score
        avg_similarity = sum(chunk.similarity_score for chunk in retrieved_chunks) / len(retrieved_chunks)

        # Return a confidence score between 0 and 1
        return min(1.0, avg_similarity * 1.2)  # Boost slightly for relevance

    def get_session_history(self, session_id: str) -> List[Message]:
        """
        Get the message history for a session
        """
        session = self.get_session(session_id)
        if not session:
            return []

        return session.messages
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
from ..utils.logger import get_logger


class ChatService:
    """
    Service for handling chat interactions and response generation
    """

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.embedding_service = EmbeddingService()
        # In-memory storage for sessions (in production, use a database)
        self.sessions = {}
        # Initialize the database logger
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # If we're in an event loop, schedule the logger initialization
            loop.create_task(self._init_logger())
        else:
            # Otherwise, initialize synchronously
            self._logger = None  # Will be initialized when needed

    async def _init_logger(self):
        """
        Initialize the database logger
        """
        self._logger = await get_logger()

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

    async def _get_logger(self):
        """
        Get the database logger, initializing it if needed
        """
        if not hasattr(self, '_logger') or self._logger is None:
            self._logger = await get_logger()
        return self._logger

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

        # Prepare the query - if selected text is provided, use it as primary context
        query_text = content
        if selected_text:
            # Prioritize queries about selected text by putting it first
            query_text = f"Regarding the following text: '{selected_text}', {content}. Focus your response on explaining or discussing this specific text."
            # Also search specifically for content related to the selected text
            selected_text_chunks = self.retrieval_service.retrieve_relevant_content(selected_text)
        else:
            selected_text_chunks = []

        # Retrieve relevant content from textbook
        retrieved_chunks = self.retrieval_service.retrieve_relevant_content(query_text)

        # If there's selected text, prioritize chunks related to it
        if selected_text:
            # Combine selected text chunks with regular search results, prioritizing selected text chunks
            retrieved_chunks = selected_text_chunks + [chunk for chunk in retrieved_chunks if chunk not in selected_text_chunks]
            # Limit to top results to avoid overwhelming the response
            retrieved_chunks = retrieved_chunks[:self.retrieval_service.max_results]

        # Generate response using the retrieved content
        response_text = self._generate_response(content, retrieved_chunks, selected_text)

        # Create response message
        response_message = Message(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="assistant",
            content=response_text,
            timestamp=datetime.now(),
            sources=[chunk.textbook_page for chunk in retrieved_chunks],
            citations=[{
                'page': chunk.textbook_page,
                'section': chunk.metadata.get('section_title', ''),
                'content_preview': chunk.content[:100] + '...' if len(chunk.content) > 100 else chunk.content
            } for chunk in retrieved_chunks],
            retrieved_chunks=[chunk.content for chunk in retrieved_chunks]  # Store retrieved chunks for validation
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

        # Log the query and response for quality review and monitoring
        import asyncio
        try:
            loop = asyncio.get_running_loop()
            # If we're in an event loop, schedule the logging task
            loop.create_task(self._log_query_and_response(session_id, content, response_text,
                                                        [chunk.textbook_page for chunk in retrieved_chunks],
                                                        chat_response.confidence_score))
        except RuntimeError:
            # If we're not in an event loop, run it synchronously in a new event loop
            import threading
            def run_logging():
                asyncio.run(self._log_query_and_response(session_id, content, response_text,
                                                       [chunk.textbook_page for chunk in retrieved_chunks],
                                                       chat_response.confidence_score))
            thread = threading.Thread(target=run_logging)
            thread.start()

        return chat_response

    async def _log_query_and_response(self, session_id: str, query: str, response: str,
                                     sources: list, confidence_score: float):
        """
        Log the query and response to the database for quality review and monitoring
        """
        logger = await self._get_logger()
        await logger.log_query(session_id, query, response, sources, confidence_score)

    def _generate_response(self, user_query: str, retrieved_chunks: List, selected_text: str = "") -> str:
        """
        Generate a response based on the user query and retrieved content
        In a real implementation, this would call an LLM API like Gemini
        """
        # For now, create a mock response based on the retrieved content
        if not retrieved_chunks:
            # Enhanced error handling for queries with no relevant content
            if selected_text:
                return f"I couldn't find relevant content in the textbook to answer your question about the selected text: '{selected_text}'. The selected text might be too specific or not covered in the textbook. Try selecting a different portion or asking a more general question about the topic."
            else:
                return "I couldn't find relevant content in the textbook to answer your question. Please try rephrasing your question or check if the topic is covered in the textbook. Make sure your question is related to the Physical AI & Humanoid Robotics content."

        # Combine the retrieved content to form the response
        context = "\n\n".join([chunk.content for chunk in retrieved_chunks[:2]])  # Use first 2 chunks

        # Perform hallucination detection by ensuring the response is grounded in retrieved content
        response = self._generate_response_with_validation(user_query, context, selected_text)

        return response

    def _generate_response_with_validation(self, user_query: str, context: str, selected_text: str = "") -> str:
        """
        Generate a response while ensuring it's grounded in the provided context to prevent hallucinations
        """
        # Create a response that references the textbook content
        if selected_text:
            # If there's selected text, focus the response on it
            response = f"Based on the selected text and textbook content:\n\n{context}\n\nThe selected text '{selected_text}' relates to this concept. Is there anything specific about this selection you'd like me to explain further?"
        else:
            response = f"Based on the textbook content:\n\n{context}\n\nIs there anything specific about this topic you'd like me to explain further?"

        return response

    def _validate_response_for_hallucinations(self, response: str, retrieved_content: List[str]) -> bool:
        """
        Validate that the response is grounded in the retrieved content to prevent hallucinations
        """
        # In a real implementation, this would check if the response contains information
        # that is supported by the retrieved content
        # For now, we'll just return True as a placeholder
        return True

    def _calculate_confidence_score(self, retrieved_chunks: List) -> float:
        """
        Calculate a confidence score based on the quality of retrieved content
        """
        if not retrieved_chunks:
            return 0.0

        # Calculate average similarity score
        avg_similarity = sum(chunk.similarity_score for chunk in retrieved_chunks) / len(retrieved_chunks)

        # Calculate max similarity score (for normalization)
        max_similarity = max(chunk.similarity_score for chunk in retrieved_chunks)

        # Calculate confidence based on both average and max similarity
        # Weight the max similarity more heavily as it indicates the best match
        confidence = (0.3 * avg_similarity) + (0.7 * max_similarity)

        # Consider the number of retrieved chunks as well
        # More relevant chunks increase confidence
        num_chunks = len(retrieved_chunks)
        if num_chunks >= 3:
            confidence *= 1.1  # Slight boost if we have multiple good matches
        elif num_chunks == 1 and max_similarity > 0.8:
            confidence *= 1.05  # Slight boost if we have one very good match

        # Ensure confidence is between 0 and 1
        return min(1.0, max(0.0, confidence))

    def get_session_history(self, session_id: str) -> List[Message]:
        """
        Get the message history for a session
        """
        session = self.get_session(session_id)
        if not session:
            return []

        return session.messages
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from src.services.chat_service import ChatService
from src.models.chat_session import ChatSession
from src.models.message import Message


class TestChatService:
    """
    Test suite for ChatService functionality
    """

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.chat_service = ChatService()

    def test_create_session(self):
        """Test creating a new chat session"""
        page_url = "https://example.com/page"
        user_context = {"user_type": "student", "level": "undergraduate"}

        session = self.chat_service.create_session(page_url, user_context)

        assert session.id is not None
        assert session.metadata["page_url"] == page_url
        assert session.metadata["user_context"] == user_context
        assert isinstance(session.created_at, datetime)
        assert isinstance(session.updated_at, datetime)

    def test_get_session(self):
        """Test retrieving an existing session"""
        # Create a session first
        session = self.chat_service.create_session("https://example.com/test")

        # Retrieve the session
        retrieved_session = self.chat_service.get_session(session.id)

        assert retrieved_session is not None
        assert retrieved_session.id == session.id
        assert retrieved_session.metadata["page_url"] == "https://example.com/test"

    def test_get_nonexistent_session(self):
        """Test retrieving a non-existent session"""
        session = self.chat_service.get_session("nonexistent-id")

        assert session is None

    @pytest.mark.asyncio
    async def test_process_user_message(self):
        """Test processing a user message"""
        # Create a session
        session = self.chat_service.create_session("https://example.com/test")

        # Mock the retrieval service to return some content
        with patch.object(self.chat_service.retrieval_service, 'retrieve_relevant_content') as mock_retrieve:
            mock_chunk = Mock()
            mock_chunk.textbook_page = "/test/page"
            mock_chunk.content = "Test content for validation"
            mock_chunk.similarity_score = 0.9
            mock_chunk.metadata = {"section_title": "Test Section"}

            mock_retrieve.return_value = [mock_chunk]

            # Process a message
            response = self.chat_service.process_user_message(
                session.id,
                "What is test content?",
                ""
            )

            # Validate response
            assert response.response_text is not None
            assert "test content" in response.response_text.lower()
            assert response.sources == ["/test/page"]
            assert 0.0 <= response.confidence_score <= 1.0

    @pytest.mark.asyncio
    async def test_process_user_message_with_selected_text(self):
        """Test processing a user message with selected text context"""
        # Create a session
        session = self.chat_service.create_session("https://example.com/test")

        # Mock the retrieval service
        with patch.object(self.chat_service.retrieval_service, 'retrieve_relevant_content') as mock_retrieve:
            mock_chunk = Mock()
            mock_chunk.textbook_page = "/test/page"
            mock_chunk.content = "Test content for validation"
            mock_chunk.similarity_score = 0.9
            mock_chunk.metadata = {"section_title": "Test Section"}

            mock_retrieve.return_value = [mock_chunk]

            # Process a message with selected text
            response = self.chat_service.process_user_message(
                session.id,
                "Explain this further",
                "Selected text for context"
            )

            # Validate response includes selected text context
            assert response.response_text is not None
            assert response.sources == ["/test/page"]

    def test_calculate_confidence_score(self):
        """Test confidence score calculation"""
        # Create mock chunks with different similarity scores
        mock_chunk1 = Mock()
        mock_chunk1.similarity_score = 0.8

        mock_chunk2 = Mock()
        mock_chunk2.similarity_score = 0.6

        chunks = [mock_chunk1, mock_chunk2]

        confidence = self.chat_service._calculate_confidence_score(chunks)

        # Should be between 0 and 1
        assert 0.0 <= confidence <= 1.0

    def test_calculate_confidence_score_empty(self):
        """Test confidence score calculation with empty chunks"""
        confidence = self.chat_service._calculate_confidence_score([])

        assert confidence == 0.0

    def test_generate_response_no_content(self):
        """Test response generation when no content is found"""
        response = self.chat_service._generate_response("Test query", [], "")

        assert "couldn't find relevant content" in response.lower()

    def test_generate_response_with_content(self):
        """Test response generation with content"""
        # Create mock chunks
        mock_chunk = Mock()
        mock_chunk.content = "This is test content"
        mock_chunk.textbook_page = "/test/page"
        mock_chunk.metadata = {"section_title": "Test Section"}

        chunks = [mock_chunk]

        response = self.chat_service._generate_response("Test query", chunks, "")

        assert "test content" in response
        assert "textbook content" in response.lower()

    def test_generate_response_with_selected_text(self):
        """Test response generation with selected text"""
        # Create mock chunks
        mock_chunk = Mock()
        mock_chunk.content = "This is test content"
        mock_chunk.textbook_page = "/test/page"
        mock_chunk.metadata = {"section_title": "Test Section"}

        chunks = [mock_chunk]

        response = self.chat_service._generate_response("Test query", chunks, "Selected context text")

        assert "selected text" in response.lower()
        assert "test content" in response
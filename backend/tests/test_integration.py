import pytest
import asyncio
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from src.api.main import create_app
from src.services.chat_service import ChatService
from src.models.chat_session import ChatSession


class TestIntegration:
    """
    Integration tests for the RAG Chatbot API
    """

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.app = create_app()
        self.client = TestClient(self.app)

    def test_health_check_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "service" in data
        assert data["service"] == "RAG Chatbot API"

    @patch('src.services.chat_service.ChatService')
    def test_start_chat_session(self, mock_chat_service_class):
        """Test starting a new chat session"""
        # Mock the chat service
        mock_chat_service = Mock()
        mock_chat_service_class.return_value = mock_chat_service

        mock_session = Mock(spec=ChatSession)
        mock_session.id = "test-session-id"
        mock_chat_service.create_session.return_value = mock_session

        # Make request
        response = self.client.post("/api/v1/chat/start", params={
            "page_url": "https://example.com/test-page"
        })

        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert data["session_id"] == "test-session-id"
        assert "message" in data

    @patch('src.services.chat_service.ChatService')
    def test_send_message(self, mock_chat_service_class):
        """Test sending a message to the chatbot"""
        # Mock the chat service
        mock_chat_service = Mock()
        mock_chat_service_class.return_value = mock_chat_service

        # Mock the response
        mock_response = Mock()
        mock_response.response_text = "This is a test response"
        mock_response.sources = ["/test/page"]
        mock_response.confidence_score = 0.9
        mock_chat_service.process_user_message.return_value = mock_response

        # Make request
        response = self.client.post("/api/v1/chat/test-session-id/message", json={
            "content": "Test message",
            "selected_text": ""
        })

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert data["response"] == "This is a test response"
        assert "sources" in data
        assert "confidence" in data

    @patch('src.services.chat_service.ChatService')
    def test_send_message_with_selected_text(self, mock_chat_service_class):
        """Test sending a message with selected text context"""
        # Mock the chat service
        mock_chat_service = Mock()
        mock_chat_service_class.return_value = mock_chat_service

        # Mock the response
        mock_response = Mock()
        mock_response.response_text = "Response considering selected text"
        mock_response.sources = ["/test/page"]
        mock_response.confidence_score = 0.85
        mock_chat_service.process_user_message.return_value = mock_response

        # Make request with selected text
        response = self.client.post("/api/v1/chat/test-session-id/message", json={
            "content": "Explain this further",
            "selected_text": "This is the selected text"
        })

        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "selected text" in data["response"].lower()
        assert "confidence" in data

    def test_search_endpoint(self):
        """Test the semantic search endpoint"""
        with patch('src.services.retrieval_service.RetrievalService') as mock_retrieval_class:
            mock_retrieval = Mock()
            mock_retrieval_class.return_value = mock_retrieval

            # Mock search results
            mock_chunk = Mock()
            mock_chunk.content = "Test search result content"
            mock_chunk.textbook_page = "/test/search"
            mock_chunk.metadata = {"section_title": "Test Section"}
            mock_chunk.similarity_score = 0.8
            mock_retrieval.retrieve_relevant_content.return_value = [mock_chunk]

            response = self.client.post("/api/v1/search", json={
                "query": "test search query",
                "max_results": 5
            })

            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert len(data["results"]) == 1
            result = data["results"][0]
            assert "content" in result
            assert "page_path" in result
            assert "similarity_score" in result

    @patch('src.services.chat_service.ChatService')
    def test_get_chat_history(self, mock_chat_service_class):
        """Test retrieving chat history"""
        # Mock the chat service
        mock_chat_service = Mock()
        mock_chat_service_class.return_value = mock_chat_service

        # Mock messages
        mock_user_message = Mock()
        mock_user_message.role = "user"
        mock_user_message.content = "Hello"
        mock_user_message.timestamp = "2023-01-01T00:00:00"
        mock_user_message.sources = []

        mock_assistant_message = Mock()
        mock_assistant_message.role = "assistant"
        mock_assistant_message.content = "Hi there"
        mock_assistant_message.timestamp = "2023-01-01T00:00:01"
        mock_assistant_message.sources = ["/test/page"]

        mock_chat_service.get_session_history.return_value = [
            mock_user_message,
            mock_assistant_message
        ]

        response = self.client.get("/api/v1/chat/test-session-id/history")

        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert len(data["messages"]) == 2

        # Check user message
        user_msg = data["messages"][0]
        assert user_msg["role"] == "user"
        assert user_msg["content"] == "Hello"
        assert user_msg["sources"] == []  # Should be empty for user messages

        # Check assistant message
        assistant_msg = data["messages"][1]
        assert assistant_msg["role"] == "assistant"
        assert assistant_msg["content"] == "Hi there"
        assert "/test/page" in assistant_msg["sources"]

    def test_error_handling_404(self):
        """Test error handling for non-existent endpoints"""
        response = self.client.get("/api/v1/nonexistent/endpoint")

        # Should return 404 for non-existent endpoints
        assert response.status_code == 404

    @patch('src.services.chat_service.ChatService')
    def test_error_handling_404_chat_session(self, mock_chat_service_class):
        """Test error handling for non-existent chat sessions"""
        # Mock the chat service to raise an exception
        mock_chat_service = Mock()
        mock_chat_service_class.return_value = mock_chat_service
        mock_chat_service.get_session_history.return_value = []
        mock_chat_service.get_session_history.side_effect = Exception("Session not found")

        response = self.client.get("/api/v1/chat/nonexistent-session/history")

        # Should return 404 or 500 depending on implementation
        assert response.status_code in [404, 500]
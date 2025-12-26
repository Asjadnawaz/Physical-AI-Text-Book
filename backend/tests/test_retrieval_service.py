import pytest
from unittest.mock import Mock, patch
from src.services.retrieval_service import RetrievalService
from src.models.retrieved_chunk import RetrievedChunk


class TestRetrievalService:
    """
    Test suite for RetrievalService functionality
    """

    def setup_method(self):
        """Set up test fixtures before each test method."""
        with patch('qdrant_client.QdrantClient') as mock_qdrant:
            self.retrieval_service = RetrievalService()

    @patch('qdrant_client.QdrantClient')
    def test_store_textbook_content(self, mock_qdrant_class):
        """Test storing textbook content"""
        # Mock the client
        mock_client = Mock()
        mock_qdrant_class.return_value = mock_client
        mock_client.get_collection.side_effect = Exception("Collection doesn't exist")  # Simulate collection not existing

        # Create a new service instance with the mocked client
        service = RetrievalService()
        service.client = mock_client

        # Mock the embedding service
        with patch.object(service, 'embedding_service') as mock_embedding:
            mock_embedding.generate_embedding.return_value = [0.1, 0.2, 0.3]

            # Call the method
            service.store_textbook_content("content_id_1", "Test content", "/test/page", "Test Section")

            # Verify the client was called correctly
            assert mock_client.upsert.called
            args, kwargs = mock_client.upsert.call_args
            assert kwargs['collection_name'] == service.collection_name

    @patch('qdrant_client.QdrantClient')
    def test_retrieve_relevant_content(self, mock_qdrant_class):
        """Test retrieving relevant content"""
        # Mock the client
        mock_client = Mock()
        mock_qdrant_class.return_value = mock_client

        # Create a new service instance with the mocked client
        service = RetrievalService()
        service.client = mock_client

        # Mock search results
        mock_result = Mock()
        mock_result.id = "result_id"
        mock_result.score = 0.8
        mock_result.payload = {
            "content": "Test content for retrieval",
            "page_path": "/test/page",
            "section_title": "Test Section",
            "content_id": "content_id_1"
        }
        mock_client.search.return_value = [mock_result]

        # Mock the embedding service
        with patch.object(service, 'embedding_service') as mock_embedding:
            mock_embedding.generate_embedding.return_value = [0.1, 0.2, 0.3]

            # Call the method
            results = service.retrieve_relevant_content("Test query about content")

            # Verify the results
            assert len(results) == 1
            chunk = results[0]
            assert isinstance(chunk, RetrievedChunk)
            assert chunk.id == "result_id"
            assert chunk.content == "Test content for retrieval"
            assert chunk.textbook_page == "/test/page"
            assert chunk.similarity_score == 0.8

    @patch('qdrant_client.QdrantClient')
    def test_retrieve_content_by_page(self, mock_qdrant_class):
        """Test retrieving content by page path"""
        # Mock the client
        mock_client = Mock()
        mock_qdrant_class.return_value = mock_client

        # Create a new service instance with the mocked client
        service = RetrievalService()
        service.client = mock_client

        # Mock search results
        mock_result = Mock()
        mock_result.id = "result_id"
        mock_result.score = 0.9
        mock_result.payload = {
            "content": "Content specific to this page",
            "page_path": "/specific/page",
            "section_title": "Specific Section",
            "content_id": "content_id_2"
        }
        mock_client.search.return_value = [mock_result]

        # Call the method
        results = service.retrieve_content_by_page("/specific/page")

        # Verify the results
        assert len(results) == 1
        chunk = results[0]
        assert chunk.textbook_page == "/specific/page"
        assert chunk.content == "Content specific to this page"

    def test_retrieve_relevant_content_with_validation_filtering(self):
        """Test that content validation and filtering works in retrieve_relevant_content"""
        # This test verifies that the validation logic in retrieve_relevant_content works
        # by checking that short or low-score content is filtered out
        with patch('qdrant_client.QdrantClient') as mock_qdrant_class:
            mock_client = Mock()
            mock_qdrant_class.return_value = mock_client

            service = RetrievalService()
            service.client = mock_client

            # Mock search results with one high-score result and one low-score result
            high_score_result = Mock()
            high_score_result.id = "high_score_id"
            high_score_result.score = 0.9  # High score
            high_score_result.payload = {
                "content": "This is meaningful content that should be included",
                "page_path": "/test/page",
                "section_title": "Test Section",
                "content_id": "content_id_1"
            }

            low_score_result = Mock()
            low_score_result.id = "low_score_id"
            low_score_result.score = 0.05  # Low score (below threshold of 0.1)
            low_score_result.payload = {
                "content": "Short content",
                "page_path": "/test/page2",
                "section_title": "Test Section 2",
                "content_id": "content_id_2"
            }

            empty_content_result = Mock()
            empty_content_result.id = "empty_id"
            empty_content_result.score = 0.8
            empty_content_result.payload = {
                "content": "",  # Empty content
                "page_path": "/test/page3",
                "section_title": "Test Section 3",
                "content_id": "content_id_3"
            }

            mock_client.search.return_value = [
                high_score_result,
                low_score_result,
                empty_content_result
            ]

            # Mock the embedding service
            with patch.object(service, 'embedding_service') as mock_embedding:
                mock_embedding.generate_embedding.return_value = [0.1, 0.2, 0.3]

                # Call the method
                results = service.retrieve_relevant_content("Test query")

                # Verify that only the high-score result with meaningful content is returned
                assert len(results) == 1
                chunk = results[0]
                assert chunk.id == "high_score_id"
                assert chunk.content == "This is meaningful content that should be included"
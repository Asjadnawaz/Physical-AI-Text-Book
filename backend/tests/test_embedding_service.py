import pytest
import numpy as np
from src.services.embedding_service import EmbeddingService


class TestEmbeddingService:
    """
    Test suite for EmbeddingService functionality
    """

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.embedding_service = EmbeddingService()

    def test_generate_embedding_basic(self):
        """Test generating an embedding for basic text"""
        text = "Hello, world!"
        embedding = self.embedding_service.generate_embedding(text)

        # Check that it returns a list of floats
        assert isinstance(embedding, list)
        assert len(embedding) == 1536  # Default embedding size
        assert all(isinstance(val, float) for val in embedding)
        assert all(0.0 <= val <= 1.0 for val in embedding)

    def test_generate_embedding_deterministic(self):
        """Test that the same text produces the same embedding"""
        text = "Consistent test text"
        embedding1 = self.embedding_service.generate_embedding(text)
        embedding2 = self.embedding_service.generate_embedding(text)

        # Should be identical
        assert embedding1 == embedding2

    def test_generate_embedding_different_texts(self):
        """Test that different texts produce different embeddings"""
        text1 = "First test text"
        text2 = "Second test text"
        embedding1 = self.embedding_service.generate_embedding(text1)
        embedding2 = self.embedding_service.generate_embedding(text2)

        # Should be different
        assert embedding1 != embedding2

    def test_calculate_similarity_identical(self):
        """Test similarity calculation for identical embeddings"""
        embedding = [0.5] * 10  # Use shorter embedding for test
        similarity = self.embedding_service.calculate_similarity(embedding, embedding)

        # Should be close to 1.0 (perfect similarity)
        assert 0.99 < similarity <= 1.0

    def test_calculate_similarity_different(self):
        """Test similarity calculation for different embeddings"""
        embedding1 = [1.0, 0.0, 0.0]
        embedding2 = [0.0, 1.0, 0.0]
        similarity = self.embedding_service.calculate_similarity(embedding1, embedding2)

        # Should be low similarity
        assert 0.0 <= similarity < 0.5

    def test_calculate_similarity_orthogonal(self):
        """Test similarity calculation for orthogonal embeddings"""
        embedding1 = [1.0, 0.0]
        embedding2 = [0.0, 1.0]
        similarity = self.embedding_service.calculate_similarity(embedding1, embedding2)

        # Should be 0 for orthogonal vectors
        assert abs(similarity) < 0.01

    def test_generate_embeddings_batch(self):
        """Test generating embeddings for a batch of texts"""
        texts = ["Text 1", "Text 2", "Text 3"]
        embeddings = self.embedding_service.generate_embeddings_batch(texts)

        # Should return list of embeddings
        assert isinstance(embeddings, list)
        assert len(embeddings) == 3
        for embedding in embeddings:
            assert isinstance(embedding, list)
            assert len(embedding) == 1536

    def test_embedding_size_consistency(self):
        """Test that embeddings are consistently the right size"""
        test_texts = [
            "Short",
            "This is a medium length text",
            "This is a much longer text that contains more words and should still result in the same embedding size",
            ""  # Empty string
        ]

        for text in test_texts:
            embedding = self.embedding_service.generate_embedding(text)
            assert len(embedding) == 1536

    def test_embedding_normalization(self):
        """Test that embeddings are normalized to expected range"""
        text = "Test text for normalization"
        embedding = self.embedding_service.generate_embedding(text)

        # All values should be between 0 and 1
        assert all(0.0 <= val <= 1.0 for val in embedding)
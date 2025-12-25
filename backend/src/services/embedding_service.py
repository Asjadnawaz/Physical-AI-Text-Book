import numpy as np
from typing import List
from ..config.settings import settings


class EmbeddingService:
    """
    Service for generating and working with text embeddings
    """

    def __init__(self):
        # In a real implementation, this would connect to an embedding API
        # For now, we'll use a mock implementation
        self.model = settings.EMBEDDING_MODEL

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text
        In a real implementation, this would call an embedding API like OpenAI
        """
        # Mock implementation - in real scenario would use actual embedding API
        # For now, we'll generate a deterministic "embedding" based on the text
        import hashlib
        import struct

        # Create a simple deterministic embedding based on the text content
        # This is for demonstration purposes only
        text_hash = hashlib.md5(text.encode()).digest()
        # Convert to a list of floats that looks like an embedding
        embedding = []
        for i in range(0, len(text_hash), 4):
            chunk = text_hash[i:i+4]
            if len(chunk) == 4:
                val = struct.unpack('f', chunk)[0]  # Unpack as float
                embedding.append(abs(val) % 1)  # Normalize to 0-1 range
            else:
                # Pad if the chunk is smaller than 4 bytes
                chunk = chunk + b'\x00' * (4 - len(chunk))
                val = struct.unpack('f', chunk)[0]
                embedding.append(abs(val) % 1)

        # Ensure the embedding has a consistent size (truncate or pad)
        target_size = 1536  # Common embedding size for text-embedding-ada-002
        if len(embedding) > target_size:
            embedding = embedding[:target_size]
        else:
            embedding.extend([0.0] * (target_size - len(embedding)))

        return embedding

    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Calculate cosine similarity between two embeddings
        """
        # Convert to numpy arrays for computation
        arr1 = np.array(embedding1)
        arr2 = np.array(embedding2)

        # Calculate cosine similarity
        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)

        # Ensure similarity is between 0 and 1
        return max(0.0, min(1.0, float(similarity)))

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts
        """
        return [self.generate_embedding(text) for text in texts]
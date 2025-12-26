# Data Model: Embedding Pipeline

## Entities

### CrawledContent
- **url** (string): Source URL of the content
- **raw_html** (string): Raw HTML content from the page
- **clean_text** (string): Cleaned text content extracted from HTML
- **title** (string): Page title extracted from HTML
- **created_at** (datetime): Timestamp of crawling
- **status** (enum): Status of crawling (success, failed, partial)

### TextChunk
- **id** (string): Unique identifier for the chunk
- **content** (string): Text content of the chunk (512 tokens max)
- **source_url** (string): URL where the content originated
- **chunk_index** (integer): Sequential index of the chunk in the document
- **metadata** (object): Additional metadata about the chunk
- **token_count** (integer): Number of tokens in the chunk

### EmbeddingRecord
- **vector_id** (string): Unique identifier for the vector record
- **embedding_vector** (array[float]): Vector representation of the text chunk
- **payload** (object): Metadata payload including source URL, chunk index, content preview
- **created_at** (datetime): Timestamp when the embedding was created
- **model_used** (string): Name of the embedding model used

## Relationships
- One CrawledContent can generate multiple TextChunk instances
- One TextChunk maps to one EmbeddingRecord
- Multiple EmbeddingRecord instances are stored in the same Qdrant collection

## Validation Rules
- TextChunk content must be between 10 and 512 tokens
- EmbeddingRecord must have a valid vector with 1024 dimensions (for Cohere model)
- URL must be a valid HTTP/HTTPS address
- Chunk overlap should be between 10-20% of chunk size
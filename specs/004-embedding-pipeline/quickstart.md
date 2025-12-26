# Quickstart Guide: Embedding Pipeline

## Prerequisites
- Python 3.9+
- UV package manager
- Cohere API key
- Qdrant API key or access to Qdrant instance

## Setup

### 1. Clone and Navigate to Backend Directory
```bash
mkdir -p backend
cd backend
```

### 2. Initialize Project with UV
```bash
uv init
uv add cohere qdrant-client requests beautifulsoup4 python-dotenv
```

### 3. Create Environment File
Create a `.env` file with the following content:
```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
BOOK_SITE_URL=https://physical-ai-text-book-lovat.vercel.app/
```

### 4. Install Dependencies
```bash
uv sync
```

## Usage

### Run the Embedding Pipeline
```bash
cd src
python main.py
```

## Expected Output
- All URLs from the book site will be crawled
- Text content will be extracted and cleaned
- Text will be chunked into appropriate sizes
- Embeddings will be generated using Cohere
- Embeddings will be stored in Qdrant collection named "rag_embedding"

## Verification
After running the pipeline, you can verify:
1. The "rag_embedding" collection exists in Qdrant
2. The collection contains the expected number of records
3. Each record has proper metadata including source URLs
# Quickstart Guide: RAG Chatbot Integration

## Overview
This guide will help you set up and run the RAG Chatbot for the Physical AI & Humanoid Robotics textbook. The system consists of a backend API that handles RAG processing and a frontend component that integrates with the Docusaurus textbook website.

## Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (for running Qdrant and Postgres locally)
- Access to OpenAI API or compatible service

## Backend Setup

### 1. Environment Configuration
Create a `.env` file in the backend directory with the following variables:

```bash
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=false

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=chatbot_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=chatbot_db

# Vector Database Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=textbook_content

# AI Service Configuration
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-pro  # or appropriate model

# Application Settings
TEXTBOOK_CONTENT_PATH=../website/docs  # Path to textbook markdown files
EMBEDDING_MODEL=text-embedding-ada-002  # or compatible model
MAX_RETRIEVAL_RESULTS=5
RESPONSE_TIMEOUT=30
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run Backend Services
```bash
# Option 1: Using Docker Compose (recommended)
docker-compose up -d

# Option 2: Start services individually
# Start Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Start Postgres
docker run -d --name chatbot-postgres -p 5432:5432 \
  -e POSTGRES_USER=chatbot_user \
  -e POSTGRES_PASSWORD=secure_password \
  -e POSTGRES_DB=chatbot_db \
  postgres:15
```

### 4. Initialize Database and Embeddings
```bash
# Run database migrations
python -m src.database.migrate

# Process textbook content and create embeddings
python -m src.scripts.process_textbook_content
```

### 5. Start Backend Server
```bash
cd backend
python -m src.api.main
```

## Frontend Setup

### 1. Install Frontend Dependencies
```bash
cd website
npm install
```

### 2. Configure Docusaurus
Update `docusaurus.config.js` to include the chatbot component:

```javascript
// Add to plugins array
plugins: [
  // ... existing plugins
  [
    '@docusaurus/plugin-content-pages',
    {
      // ... existing config
    },
  ],
],

// Add to theme config if needed
themeConfig: {
  // ... existing theme config
  chatbot: {
    enabled: true,
    apiUrl: process.env.CHATBOT_API_URL || 'http://localhost:8000/api/v1',
  },
},
```

### 3. Build and Run Website
```bash
cd website
npm run build
npm run serve  # or npm start for development
```

## API Usage Examples

### Start a New Chat Session
```bash
curl -X POST http://localhost:8000/api/v1/chat/start \
  -H "Content-Type: application/json" \
  -d '{
    "page_url": "/chapter-1/section-1",
    "user_context": {
      "selected_text": "Physical AI challenges the traditional view of intelligence"
    }
  }'
```

### Send a Message
```bash
curl -X POST http://localhost:8000/api/v1/chat/session-id-123/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What does this mean for robotics?",
    "selected_text": "Physical AI challenges the traditional view of intelligence"
  }'
```

### Perform Semantic Search
```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "embodied cognition in robotics",
    "max_results": 3
  }'
```

## Testing
Run the full test suite:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd website
npm test
```

## Troubleshooting
1. **API Connection Issues**: Verify backend server is running and API URL is correctly configured
2. **Embedding Processing Errors**: Check that textbook content path is correct and accessible
3. **Database Connection Issues**: Ensure Postgres and Qdrant services are running
4. **Rate Limiting**: Check your AI service API limits and adjust accordingly

## Next Steps
- Customize the chatbot UI to match your textbook's design
- Add analytics and monitoring
- Implement rate limiting and caching
- Set up production deployment configuration
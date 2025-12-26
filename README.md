# RAG Chatbot for Physical AI & Humanoid Robotics Textbook

This project implements a Retrieval-Augmented Generation (RAG) chatbot that integrates with the Docusaurus-based textbook website. The chatbot allows students to ask questions about textbook content and receive accurate, textbook-grounded responses.

## Features

- **Context-Aware Responses**: Answers based solely on textbook content
- **Real-time Interaction**: Fast responses within 5 seconds
- **Session Management**: Maintains conversation history
- **Semantic Search**: Finds relevant content using vector embeddings
- **Docusaurus Integration**: Seamless integration with existing textbook UI

## Architecture

- **Frontend**: React components integrated with Docusaurus
- **Backend**: FastAPI server with Qdrant vector database
- **AI Services**: Gemini API for response generation
- **Data Storage**: PostgreSQL for session management, Qdrant for content embeddings

## Setup Instructions

### Prerequisites

- Node.js (for Docusaurus frontend)
- Python 3.11+ (for FastAPI backend)
- Docker and Docker Compose (for Qdrant and PostgreSQL)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BookAIDD
   ```

2. **Set up the frontend**:
   ```bash
   cd website
   npm install
   ```

3. **Set up the backend**:
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   # In the backend directory
   cp .env.example .env
   # Edit .env to add your API keys
   ```

5. **Start the services**:
   ```bash
   # In the root directory
   docker-compose up -d
   ```

6. **Load the textbook content**:
   ```bash
   cd backend
   python load_textbook_content.py
   ```

7. **Start the backend server**:
   ```bash
   cd backend
   python -m src.api.main
   ```

8. **Start the Docusaurus frontend**:
   ```bash
   cd website
   npm start
   ```

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
```

## Usage

Once both the frontend and backend are running:

1. Navigate to the Docusaurus textbook website (usually `http://localhost:3000`)
2. You'll see a chatbot icon in the bottom-right corner of every page
3. Click the icon to open the chat interface
4. Ask questions about the textbook content
5. The chatbot will search the textbook and provide contextually relevant answers

## Development

### Running in Development Mode

For development, you can run the services separately:

```bash
# Terminal 1: Start Docker services
docker-compose up

# Terminal 2: Start the backend (in backend directory)
python -m src.api.main

# Terminal 3: Start the frontend (in website directory)
npm start
```

### Loading Textbook Content

To reload textbook content after making changes to the docs:

```bash
cd backend
python load_textbook_content.py
```

## Project Structure

```
BookAIDD/
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── config/         # Configuration
│   ├── requirements.txt
│   └── load_textbook_content.py
├── website/                 # Docusaurus frontend
│   ├── docs/               # Textbook markdown files
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   └── services/       # Frontend services
│   └── docusaurus.config.js
├── docker-compose.yml      # Docker services
└── specs/                  # Project specifications
    └── 003-rag-chatbot-integration/
```

## API Endpoints

- `POST /api/v1/chat/start` - Start a new chat session
- `POST /api/v1/chat/{session_id}/message` - Send a message to the chatbot
- `GET /api/v1/chat/{session_id}/history` - Get chat history
- `POST /api/v1/search` - Perform semantic search on textbook content
- `GET /health` - Health check endpoint

## Troubleshooting

- **Frontend not loading**: Make sure the backend is running and accessible
- **Chatbot not responding**: Check that the Qdrant service is running and content has been loaded
- **API errors**: Verify your API keys are correctly set in the environment variables
- **Docker issues**: Ensure Docker is running and you have sufficient permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[License information would go here]
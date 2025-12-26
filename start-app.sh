#!/bin/bash
# Startup script for the RAG Chatbot application

echo "Starting RAG Chatbot for Physical AI & Humanoid Robotics Textbook..."

# Start the Docker services (Qdrant and PostgreSQL)
echo "Starting Docker services..."
docker-compose up -d

# Wait a moment for services to start
sleep 5

echo "Docker services started successfully!"

echo ""
echo "To complete the setup:"
echo "1. Load the textbook content: cd backend && python load_textbook_content.py"
echo "2. Start the backend server: cd backend && python -m src.api.main"
echo "3. Start the frontend: cd website && npm start"
echo ""
echo "The chatbot will be available on the Docusaurus website once both services are running."
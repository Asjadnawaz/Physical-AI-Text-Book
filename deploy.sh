#!/bin/bash

# Deployment script for RAG Chatbot for Physical AI & Humanoid Robotics Textbook

set -e  # Exit on any error

echo "Starting deployment of RAG Chatbot..."

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose is required but not installed. Aborting."
    exit 1
fi

# Check if environment variables are set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "GEMINI_API_KEY environment variable is not set. Please set it before running this script."
    exit 1
fi

if [ -z "$POSTGRES_PASSWORD" ]; then
    echo "POSTGRES_PASSWORD environment variable is not set. Please set it before running this script."
    exit 1
fi

echo "Environment variables are set, proceeding with deployment..."

# Build and start the services
echo "Building and starting services..."
docker-compose -f production-deploy.yml up -d --build

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check if the services are running
if [ "$(docker-compose -f production-deploy.yml ps -q | wc -l)" -eq 0 ]; then
    echo "No services are running. Deployment may have failed."
    exit 1
fi

echo "Services are up and running!"

# Load textbook content into the vector database
echo "Loading textbook content into vector database..."
docker-compose -f production-deploy.yml exec chatbot-api python load_textbook_content.py

echo "Textbook content loaded successfully!"

# Run health check
echo "Running health check..."
sleep 5  # Wait a bit more for the API to be fully ready
HEALTH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$HEALTH_CHECK" -eq 200 ]; then
    echo "Health check passed! API is running at http://localhost:8000"
    echo "Frontend should be available at http://localhost:3000"
else
    echo "Health check failed with status code: $HEALTH_CHECK"
    echo "Check the logs with: docker-compose -f production-deploy.yml logs"
    exit 1
fi

echo ""
echo "Deployment completed successfully!"
echo ""
echo "Access the services:"
echo "- API Documentation: http://localhost:8000/docs"
echo "- Frontend: http://localhost:3000"
echo "- Health Check: http://localhost:8000/health"
echo ""
echo "To view logs: docker-compose -f production-deploy.yml logs -f"
echo "To stop services: docker-compose -f production-deploy.yml down"
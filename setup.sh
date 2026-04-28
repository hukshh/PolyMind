#!/bin/bash

# Ensure /usr/local/bin is in PATH for Mac Docker Desktop
export PATH=$PATH:/usr/local/bin

echo "🚀 Starting PolyMind Docker Setup..."

# Stop any existing containers
docker-compose down

# Build and start in detached mode
docker-compose up --build -d

echo "✅ Containers are starting!"
echo "---------------------------------------"
echo "Frontend: http://localhost:8501"
echo "Backend API: http://localhost:8000/docs"
echo "---------------------------------------"
echo "To see backend logs, run: docker-compose logs -f backend"

#!/bin/bash

echo "======================================"
echo "AI Resume Analyzer - Setup Script"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✓ Docker found"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✓ Docker Compose found"
echo ""

# Copy environment files if they don't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env created. Please update with your configuration."
fi

if [ ! -f "backend/.env" ]; then
    echo "📝 Creating backend/.env file from backend/.env.example..."
    cp backend/.env.example backend/.env
fi

if [ ! -f "frontend/.env.local" ]; then
    echo "📝 Creating frontend/.env.local file from frontend/.env.example..."
    cp frontend/.env.example frontend/.env.local
fi

echo ""
echo "🐳 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

echo ""
echo "✅ All services started!"
echo ""
echo "Access the application at:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Documentation: http://localhost:8000/api/docs"
echo ""
echo "To view logs, run:"
echo "  docker-compose logs -f backend"
echo "  docker-compose logs -f frontend"
echo ""

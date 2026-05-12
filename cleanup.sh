#!/bin/bash

echo "======================================"
echo "AI Resume Analyzer - Cleanup Script"
echo "======================================"
echo ""

# Stop all containers
echo "Stopping containers..."
docker-compose down

# Remove volumes (optional - uncomment to remove data)
# echo "Removing volumes..."
# docker-compose down -v

echo "✅ Cleanup complete!"

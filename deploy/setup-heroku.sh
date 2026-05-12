#!/bin/bash

# AI Resume Analyzer - Heroku Deployment Script

set -e

echo "=========================================="
echo "AI Resume Analyzer - Heroku Setup"
echo "=========================================="

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Installing Heroku CLI..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew tap heroku/brew && brew install heroku
    else
        curl https://cli-assets.heroku.com/install.sh | sh
    fi
fi

# Login to Heroku
echo "Logging into Heroku..."
heroku login

# Get app name
echo "Enter your Heroku app name:"
read APP_NAME

# Create app if it doesn't exist
heroku create $APP_NAME 2>/dev/null || true

# Add PostgreSQL
echo "Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:standard-0 --app=$APP_NAME 2>/dev/null || true

# Get database URL
DB_URL=$(heroku config:get DATABASE_URL --app=$APP_NAME)

# Set environment variables
echo "Setting environment variables..."
heroku config:set \
    SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')" \
    DEBUG=False \
    ALLOWED_ORIGINS="https://$APP_NAME.herokuapp.com" \
    NEXT_PUBLIC_API_URL="https://$APP_NAME.herokuapp.com" \
    --app=$APP_NAME

# Create Procfile
cat > Procfile << 'EOF'
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF

# Commit and push
git add Procfile
git commit -m "Add Heroku Procfile"

# Push to Heroku
echo "Deploying to Heroku..."
git push heroku main

echo ""
echo "=========================================="
echo "✅ Heroku Deployment Complete!"
echo "=========================================="
echo "Application URL: https://$APP_NAME.herokuapp.com"
echo "API Docs: https://$APP_NAME.herokuapp.com/api/docs"
echo ""
echo "Useful commands:"
echo "  View logs: heroku logs --tail --app=$APP_NAME"
echo "  Restart: heroku dyno:restart --app=$APP_NAME"
echo "  Database URL: heroku config:get DATABASE_URL --app=$APP_NAME"
echo ""

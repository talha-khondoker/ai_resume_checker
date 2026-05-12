#!/bin/bash

# Interactive Deployment Setup
# This script helps you choose and configure your deployment

clear

echo "╔════════════════════════════════════════════════════════╗"
echo "║   AI Resume Analyzer - Deployment Setup Wizard         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Platform selection
echo "Which platform would you like to deploy to?"
echo ""
echo "1) Heroku (Easiest - 5 minutes)"
echo "2) DigitalOcean (Best Value - 15 minutes)"
echo "3) AWS (Most Powerful - 20 minutes)"
echo "4) Google Cloud (Enterprise - 15 minutes)"
echo "5) Manual Setup (Any VPS)"
echo ""

read -p "Enter your choice (1-5): " platform_choice

case $platform_choice in
  1)
    echo ""
    echo "🚀 Setting up Heroku deployment..."
    cd deploy
    bash setup-heroku.sh
    ;;
  2)
    echo ""
    echo "🚀 Setting up DigitalOcean deployment..."
    cd deploy
    bash setup-do.sh
    ;;
  3)
    echo ""
    echo "🚀 Setting up AWS deployment..."
    cd deploy
    bash setup-aws.sh
    ;;
  4)
    echo ""
    echo "📋 Google Cloud setup:"
    echo "1. Go to https://console.cloud.google.com"
    echo "2. Create a new project"
    echo "3. Enable Cloud SQL and Cloud Run APIs"
    echo "4. Run: gcloud init"
    echo "5. Follow Cloud SQL deployment guide in DEPLOYMENT.md"
    ;;
  5)
    echo ""
    echo "📋 Manual setup on your VPS:"
    echo ""
    echo "1. SSH into your server:"
    echo "   ssh user@your-server-ip"
    echo ""
    echo "2. Install Docker & Docker Compose:"
    echo "   curl -fsSL https://get.docker.com | sh"
    echo "   sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m) -o /usr/local/bin/docker-compose"
    echo "   sudo chmod +x /usr/local/bin/docker-compose"
    echo ""
    echo "3. Clone your repository:"
    echo "   git clone your-repo-url"
    echo "   cd ai-resume-analyzer"
    echo ""
    echo "4. Setup environment:"
    echo "   cp .env.production .env"
    echo "   nano .env  # Edit with your values"
    echo ""
    echo "5. Deploy:"
    echo "   docker-compose -f docker-compose.prod.yml up -d"
    echo ""
    echo "6. Setup SSL (Let's Encrypt):"
    echo "   sudo certbot certonly --standalone -d yourdomain.com"
    echo "   sudo cp /etc/letsencrypt/live/yourdomain.com/cert.pem ssl/"
    echo "   sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/"
    ;;
  *)
    echo "Invalid choice. Please run the script again."
    exit 1
    ;;
esac

echo ""
echo "════════════════════════════════════════════════════════"
echo "✅ Deployment setup complete!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "1. Test your application"
echo "2. Set up domain (if using custom domain)"
echo "3. Create admin account"
echo "4. Enable monitoring"
echo ""
echo "For detailed help, see DEPLOY_ONLINE.md"
echo ""

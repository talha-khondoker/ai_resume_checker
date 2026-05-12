#!/bin/bash

# AI Resume Analyzer - DigitalOcean Deployment Script
# Run this on a fresh Ubuntu 22.04 droplet

set -e

echo "=========================================="
echo "AI Resume Analyzer - DigitalOcean Setup"
echo "=========================================="

# Update system
sudo apt update
sudo apt upgrade -y

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt install -y git curl

# Install Certbot for SSL
echo "Installing Certbot..."
sudo apt install -y certbot

# Clone repository
echo "Please enter your GitHub repository URL:"
read REPO_URL

git clone $REPO_URL
cd ai-resume-analyzer

# Setup environment
echo "Setting up environment..."
cp .env.production .env

# Get domain
echo "Enter your domain name (e.g., yourdomain.com):"
read DOMAIN

# Update .env with domain
sed -i "s/yourdomain.com/$DOMAIN/g" .env
sed -i "s/CHANGE_ME_TO_STRONG_PASSWORD_32_CHARS_MIN/$(openssl rand -base64 32)/g" .env
sed -i "s/CHANGE_ME_TO_STRONG_SECRET_KEY_MINIMUM_32_CHARACTERS/$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')/g" .env

# Update nginx config
sed -i "s/yourdomain.com/$DOMAIN/g" nginx.prod.conf

echo ""
echo "Edit .env file and update these values:"
cat .env | grep "CHANGE_ME"

echo ""
echo "Press Enter after updating .env"
read

# Create SSL certificate
echo "Creating SSL certificate for $DOMAIN..."
mkdir -p ssl
sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN
sudo cp /etc/letsencrypt/live/$DOMAIN/cert.pem ssl/
sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ssl/
sudo chown $USER:$USER ssl/*

# Create backup directory
mkdir -p backups

# Deploy application
echo "Deploying application..."
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo "Application URL: https://$DOMAIN"
echo "API Docs: https://$DOMAIN/api/docs"
echo ""
echo "Useful commands:"
echo "  View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  Stop app: docker-compose -f docker-compose.prod.yml down"
echo "  Restart: docker-compose -f docker-compose.prod.yml restart"
echo "  Database backup: docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U \$DB_USER \$DB_NAME > backups/backup-\$(date +%Y%m%d).sql"
echo ""

#!/bin/bash

# AI Resume Analyzer - AWS EC2 Deployment Script
# Run this on a fresh Ubuntu 22.04 EC2 instance

set -e

echo "=========================================="
echo "AI Resume Analyzer - AWS EC2 Setup"
echo "=========================================="

# Update system
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y docker.io docker-compose git curl wget certbot

# Add user to docker group
sudo usermod -aG docker $USER

# Clone repository
echo "Please enter your GitHub repository URL:"
read REPO_URL

git clone $REPO_URL
cd ai-resume-analyzer

# Setup environment
cp .env.production .env

# Get domain or use EC2 DNS
echo "Enter your domain name (or leave empty to use EC2 DNS):"
read DOMAIN

if [ -z "$DOMAIN" ]; then
    DOMAIN=$(curl http://169.254.169.254/latest/meta-data/public-ipv4)
fi

# Update .env
sed -i "s/yourdomain.com/$DOMAIN/g" .env
sed -i "s/CHANGE_ME_TO_STRONG_PASSWORD_32_CHARS_MIN/$(openssl rand -base64 32)/g" .env
sed -i "s/CHANGE_ME_TO_STRONG_SECRET_KEY_MINIMUM_32_CHARACTERS/$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')/g" .env

# Create directories
mkdir -p ssl backups

# Create SSL certificate (if domain)
if [[ $DOMAIN != *.compute* ]]; then
    echo "Creating SSL certificate..."
    sudo certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN
    sudo cp /etc/letsencrypt/live/$DOMAIN/cert.pem ssl/
    sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ssl/
    sudo chown $USER:$USER ssl/*
    sed -i "s/yourdomain.com/$DOMAIN/g" nginx.prod.conf
fi

# Deploy
echo "Deploying application..."
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Setup SSL renewal cron job
if [[ $DOMAIN != *.compute* ]]; then
    cat > renew-cert.sh << 'EOF'
#!/bin/bash
sudo certbot renew --quiet
sudo cp /etc/letsencrypt/live/$DOMAIN/cert.pem /home/ubuntu/ai-resume-analyzer/ssl/
sudo cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /home/ubuntu/ai-resume-analyzer/ssl/
docker-compose -f /home/ubuntu/ai-resume-analyzer/docker-compose.prod.yml restart nginx
EOF
    chmod +x renew-cert.sh
    (crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/ai-resume-analyzer/renew-cert.sh") | crontab -
fi

echo ""
echo "=========================================="
echo "✅ AWS Deployment Complete!"
echo "=========================================="
echo "Application URL: https://$DOMAIN"
echo ""
echo "Next steps:"
echo "1. Update your security group to allow HTTPS (port 443)"
echo "2. Create RDS database for production use"
echo "3. Update .env with RDS credentials"
echo ""

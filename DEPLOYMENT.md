# AI Resume Analyzer - Deployment Guide

Complete guide for deploying the AI Resume Analyzer application to production environments.

## Table of Contents
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deployment Options](#deployment-options)
3. [Option 1: AWS EC2](#option-1-aws-ec2)
4. [Option 2: Heroku](#option-2-heroku)
5. [Option 3: DigitalOcean](#option-3-digitalocean)
6. [Option 4: Google Cloud](#option-4-google-cloud)
7. [Option 5: Docker Hub + Any VPS](#option-5-docker-hub--any-vps)
8. [Post-Deployment](#post-deployment)
9. [Monitoring & Maintenance](#monitoring--maintenance)
10. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Strong database password (32+ characters)
- [ ] Strong SECRET_KEY for JWT (use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- [ ] Domain name registered (e.g., yourdomain.com)
- [ ] SSL certificate (Let's Encrypt is free)
- [ ] Updated `.env.production` with all production values
- [ ] Updated `nginx.prod.conf` with your domain
- [ ] GitHub account (for version control)
- [ ] Backup strategy planned

### Generate Secure Keys

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate DB_PASSWORD
openssl rand -base64 32
```

---

## Deployment Options

| Platform | Cost | Difficulty | Recommendation |
|----------|------|------------|-----------------|
| AWS EC2 | $10-30/month | Medium | Best for scalability |
| Heroku | Free-$50/month | Easy | Best for quick deployment |
| DigitalOcean | $4-24/month | Medium | Best value for money |
| Google Cloud | $10-50/month | Medium | Best integration |
| Self-hosted VPS | $5-20/month | Hard | Best for cost control |

---

## Option 1: AWS EC2

### Step 1: Create EC2 Instance

1. Go to [AWS Console](https://console.aws.amazon.com)
2. Navigate to EC2 > Instances
3. Click "Launch Instance"
4. **Choose AMI**: Ubuntu Server 22.04 LTS
5. **Instance Type**: t3.medium (for starter) or t3.large (for production)
6. **Storage**: 30GB gp3
7. **Security Group**: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
8. Create or use key pair (download `.pem` file)

### Step 2: Connect to Instance

```bash
# On your local machine
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Install Docker and Docker Compose

```bash
sudo apt update
sudo apt install -y docker.io docker-compose git curl

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

### Step 4: Set Up Application

```bash
# Clone your repository
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer

# Copy production env file
cp .env.production .env

# Edit .env with your production values
nano .env
```

### Step 5: Set Up SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Certificates will be in:
# /etc/letsencrypt/live/yourdomain.com/cert.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

### Step 6: Copy SSL Certificates to Project

```bash
# Create ssl directory
mkdir -p ssl

# Copy certificates (from /etc/letsencrypt)
sudo cp /etc/letsencrypt/live/yourdomain.com/cert.pem ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/
sudo chown $USER:$USER ssl/*
```

### Step 7: Create Database (AWS RDS - Optional but Recommended)

1. Go to AWS RDS Console
2. Create PostgreSQL database
3. Note the endpoint URL
4. Update `.env` with RDS connection details

Or use local PostgreSQL in container (less reliable for production).

### Step 8: Deploy Application

```bash
# Build and start containers
docker-compose -f docker-compose.prod.yml up -d

# Check logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop containers
docker-compose -f docker-compose.prod.yml down
```

### Step 9: Set Up Auto-Renewal for SSL

```bash
# Create renewal script
cat > /home/ubuntu/renew-cert.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/ai-resume-analyzer
sudo certbot renew --quiet
sudo cp /etc/letsencrypt/live/yourdomain.com/cert.pem ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/
docker-compose -f docker-compose.prod.yml restart nginx
EOF

chmod +x /home/ubuntu/renew-cert.sh

# Add to crontab
(crontab -l 2>/dev/null; echo "0 2 * * * /home/ubuntu/renew-cert.sh") | crontab -
```

---

## Option 2: Heroku (Easiest for Beginners)

### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Verify
heroku --version
```

### Step 2: Create Heroku App

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0

# Check database URL
heroku config | grep DATABASE_URL
```

### Step 3: Set Environment Variables

```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_ORIGINS="https://your-app-name.herokuapp.com"
heroku config:set NEXT_PUBLIC_API_URL="https://your-app-name.herokuapp.com"
```

### Step 4: Create Procfile

```bash
cat > Procfile << 'EOF'
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF
```

### Step 5: Deploy

```bash
# Add to git
git add .
git commit -m "Deploy to Heroku"

# Push to Heroku
git push heroku main

# View logs
heroku logs --tail
```

### Step 6: Set Up Custom Domain (Optional)

```bash
# Add domain
heroku domains:add yourdomain.com

# Add CNAME record to your DNS provider pointing to:
# yourdomain.com.herokudns.com
```

---

## Option 3: DigitalOcean

### Step 1: Create Droplet

1. Go to [DigitalOcean](https://www.digitalocean.com)
2. Create > Droplets
3. **Image**: Ubuntu 22.04
4. **Size**: Basic ($4-24/month)
5. **Region**: Closest to you
6. Add SSH key

### Step 2: Install Docker

```bash
# SSH into droplet
ssh root@your_droplet_ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 3: Set Up Domain & SSL

```bash
# Update your domain DNS to point to droplet IP

# Install Certbot
apt update && apt install -y certbot

# Get SSL certificate
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

### Step 4: Deploy Application

```bash
# Clone and setup
git clone your-repo-url
cd ai-resume-analyzer
cp .env.production .env
nano .env  # Edit with production values

# Copy SSL certificates
mkdir -p ssl
cp /etc/letsencrypt/live/yourdomain.com/cert.pem ssl/
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps
```

---

## Option 4: Google Cloud (Run + SQL)

### Step 1: Create Cloud SQL Instance

```bash
# Install gcloud CLI and authenticate
gcloud init

# Create PostgreSQL instance
gcloud sql instances create ai-resume-db \
  --database-version POSTGRES_15 \
  --tier db-f1-micro \
  --region us-central1

# Create database
gcloud sql databases create ai_resume_analyzer \
  --instance ai-resume-db
```

### Step 2: Deploy to Cloud Run

```bash
# Create dockerfile at root
# (already have it at backend/Dockerfile)

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/your-project-id/ai-resume-backend

# Deploy to Cloud Run
gcloud run deploy ai-resume-backend \
  --image gcr.io/your-project-id/ai-resume-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL=postgresql://user:pass@cloud-sql-ip/ai_resume_analyzer
```

---

## Option 5: Docker Hub + Any VPS

### Step 1: Push to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag images
docker tag ai-resume-backend:latest your-username/ai-resume-backend:latest
docker tag ai-resume-frontend:latest your-username/ai-resume-frontend:latest

# Push images
docker push your-username/ai-resume-backend:latest
docker push your-username/ai-resume-frontend:latest
```

### Step 2: Update docker-compose.prod.yml

```yaml
services:
  backend:
    image: your-username/ai-resume-backend:latest
  frontend:
    image: your-username/ai-resume-frontend:latest
```

### Step 3: Deploy on Any VPS

```bash
# SSH into VPS
ssh user@vps-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Clone repo
git clone your-repo-url
cd ai-resume-analyzer

# Create .env file
cp .env.production .env
# Edit .env with production values

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

## Post-Deployment

### 1. Verify Application

```bash
# Check if all containers are running
docker-compose -f docker-compose.prod.yml ps

# Check application logs
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend

# Test API
curl https://yourdomain.com/api/health

# Test frontend
# Open https://yourdomain.com in browser
```

### 2. Database Backup

```bash
# Create backup directory
mkdir -p backups

# Backup database
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U $DB_USER $DB_NAME > backups/backup-$(date +%Y%m%d-%H%M%S).sql

# Restore database
docker-compose -f docker-compose.prod.yml exec postgres psql -U $DB_USER $DB_NAME < backups/backup-file.sql
```

### 3. Create Admin User

```bash
# Access backend container
docker-compose -f docker-compose.prod.yml exec backend bash

# Create admin user (use API or direct Python script)
python -c "
from app.db.database import SessionLocal, engine
from app.models.models import User, Base
from app.core.security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()
admin = User(
    name='Admin',
    email='admin@yourdomain.com',
    hashed_password=get_password_hash('strong-password'),
    role='admin',
    is_active=True
)
db.add(admin)
db.commit()
"

# Exit container
exit
```

### 4. Setup Monitoring

```bash
# Check disk space
df -h

# Check memory usage
free -h

# Monitor logs in real-time
docker-compose -f docker-compose.prod.yml logs -f --tail=100
```

---

## Monitoring & Maintenance

### Automatic Health Checks

The application has built-in health endpoints:

```bash
# Backend health
curl https://yourdomain.com/api/health

# Frontend health
curl https://yourdomain.com/
```

### Set Up Monitoring Alerts

**Option 1: Using Uptime Robot (Free)**

1. Go to [Uptime Robot](https://uptimerobot.com)
2. Add monitoring for `https://yourdomain.com/api/health`
3. Set alert to your email

**Option 2: Using Datadog**

```bash
# Add Datadog container to docker-compose.prod.yml
datadog:
  image: datadog/agent:latest
  environment:
    DD_API_KEY: your-datadog-api-key
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```

### Regular Maintenance

```bash
# View logs
docker-compose -f docker-compose.prod.yml logs --tail=50

# Restart application
docker-compose -f docker-compose.prod.yml restart

# Update containers
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Clean up unused Docker resources
docker system prune -a

# Check disk space and clean old backups
du -sh backups/
rm backups/backup-older-than-30-days.sql
```

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Verify environment variables
docker-compose -f docker-compose.prod.yml config | grep -i secret_key

# Rebuild containers
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### Database Connection Error

```bash
# Test database connection
docker-compose -f docker-compose.prod.yml exec postgres psql -U $DB_USER -c "SELECT 1"

# Check DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Verify credentials
docker-compose -f docker-compose.prod.yml config | grep -A3 "postgres:"
```

### SSL Certificate Issues

```bash
# Check certificate expiration
openssl x509 -in ssl/cert.pem -noout -dates

# Renew certificate
sudo certbot renew --force-renewal

# Copy new certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/cert.pem ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/

# Restart nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

### High Memory Usage

```bash
# Check container memory
docker stats

# Reduce worker processes in docker-compose.prod.yml
# Change: WORKERS: 4 -> WORKERS: 2

# Restart containers
docker-compose -f docker-compose.prod.yml up -d
```

### File Upload Not Working

```bash
# Check upload folder permissions
docker-compose -f docker-compose.prod.yml exec backend ls -la /app/app/uploads

# Fix permissions
docker-compose -f docker-compose.prod.yml exec backend chmod 755 /app/app/uploads

# Check available disk space
docker exec ai-resume-backend-prod df -h
```

---

## Performance Optimization

### 1. Enable Caching

Update `nginx.prod.conf`:
```nginx
location / {
    expires 1d;
    add_header Cache-Control "public, immutable";
}
```

### 2. Enable Database Pooling

Already configured in `backend/app/db/database.py` with SQLAlchemy pooling.

### 3. Use CDN for Static Assets

```bash
# Update frontend .env
NEXT_PUBLIC_CDN_URL=https://cdn.yourdomain.com
```

### 4. Increase Upload Limit (if needed)

Edit `.env`:
```
MAX_UPLOAD_SIZE=52428800  # 50MB instead of 10MB
```

---

## Rollback Procedure

```bash
# Keep previous image version
docker tag ai-resume-backend:latest ai-resume-backend:backup

# In case of issues, rollback to previous version
docker-compose -f docker-compose.prod.yml down
docker tag ai-resume-backend:backup ai-resume-backend:latest
docker-compose -f docker-compose.prod.yml up -d
```

---

## Security Checklist

- [ ] HTTPS enabled with valid SSL certificate
- [ ] SECRET_KEY is strong and unique
- [ ] Database password is strong (32+ characters)
- [ ] Database backups are automated
- [ ] Firewall configured (only ports 22, 80, 443 open)
- [ ] SSH key-only access (no password)
- [ ] Regular security updates applied
- [ ] Admin credentials changed from defaults
- [ ] CORS origins whitelisted
- [ ] File upload limits enforced

---

## Support & Additional Resources

- **Documentation**: See README.md and PROJECT_SUMMARY.md
- **API Reference**: https://yourdomain.com/api/docs
- **Docker Docs**: https://docs.docker.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs
- **Next.js Deployment**: https://nextjs.org/docs/deployment

---

## Cost Estimation

| Platform | Monthly Cost | Annual Cost |
|----------|--------------|------------|
| AWS EC2 t3.medium | $15-20 | $180-240 |
| DigitalOcean | $12-24 | $144-288 |
| Heroku (paid plan) | $50-100 | $600-1200 |
| Google Cloud | $15-40 | $180-480 |
| Self-hosted VPS | $5-15 | $60-180 |

---

**Ready to deploy? Start with the option that best fits your needs and budget!**

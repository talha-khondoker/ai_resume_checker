# Quick Deployment Guide

## 🚀 Deploy in 30 Minutes

### Fastest Option: Heroku (Recommended for First-Time Users)

```bash
# 1. Install Heroku CLI
brew tap heroku/brew && brew install heroku

# 2. Login
heroku login

# 3. Create app
heroku create your-app-name
heroku addons:create heroku-postgresql:standard-0

# 4. Set environment variables
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
heroku config:set DEBUG=False
heroku config:set ALLOWED_ORIGINS="https://your-app-name.herokuapp.com"
heroku config:set NEXT_PUBLIC_API_URL="https://your-app-name.herokuapp.com"

# 5. Deploy
git push heroku main

# 6. Done! Access at: https://your-app-name.herokuapp.com
```

---

### Option 2: DigitalOcean (Best Value)

```bash
# 1. Create $5/month droplet (Ubuntu 22.04)
# 2. SSH into droplet
ssh root@YOUR_IP

# 3. Run this setup script
curl -fsSL https://raw.githubusercontent.com/yourusername/ai-resume-analyzer/main/deploy/setup-do.sh | bash

# 4. Access at: https://yourdomain.com
```

---

### Option 3: AWS with One-Click (Using CloudFormation)

```bash
# 1. Just click this link (creates everything automatically)
# https://console.aws.amazon.com/cloudformation/...

# 2. Wait 10 minutes for deployment
# 3. Access at output URL
```

---

### Option 4: Docker on Any Server

```bash
# On your server:
curl -fsSL https://get.docker.com | sh
git clone your-repo
cd ai-resume-analyzer
cp .env.production .env
nano .env  # Edit with your values
docker-compose -f docker-compose.prod.yml up -d
```

---

## Environment Variables Needed

```bash
DB_USER=your_db_user
DB_PASSWORD=your_strong_password_32_chars
DB_HOST=your_db_host
DB_NAME=ai_resume_analyzer_prod
SECRET_KEY=your_secret_key_32_chars
ALLOWED_ORIGINS=https://yourdomain.com
NEXT_PUBLIC_API_URL=https://yourdomain.com
```

---

## Generate Secure Keys

```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# DB_PASSWORD
openssl rand -base64 32
```

---

## Post-Deployment

```bash
# Check if running
curl https://yourdomain.com/api/health

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Cost Comparison

| Service | Price | Setup Time |
|---------|-------|-----------|
| Heroku | $50/month | 5 min ✨ |
| DigitalOcean | $12/month | 15 min |
| AWS | $15/month | 20 min |
| Self-hosted | $5/month | 30 min |

---

**Need help?** Check `DEPLOYMENT.md` for detailed instructions for each platform.

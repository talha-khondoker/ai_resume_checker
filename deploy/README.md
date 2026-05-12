# Deployment Configuration

This directory contains deployment scripts and configurations for different cloud platforms.

## Quick Start

### 1. Heroku (Easiest - 5 minutes)
```bash
bash setup-heroku.sh
```

### 2. DigitalOcean (Best Value - 15 minutes)
```bash
bash setup-do.sh
```

### 3. AWS (Most Scalable - 20 minutes)
```bash
bash setup-aws.sh
```

### 4. Render + Vercel (GitHub Push Deployment)

Before you use this method, add the required GitHub secrets to your repository:

- `RENDER_API_KEY`
- `RENDER_SERVICE_ID`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

Then push to `main` and GitHub Actions will run the workflow in `.github/workflows/render-vercel.yml`.

Your backend deploys to Render and your frontend deploys to Vercel automatically.

### 5. Generate Configuration for Any Platform
```bash
python generate_config.py --platform heroku --domain yourdomain.com
python generate_config.py --platform all --domain yourdomain.com
```

## Files in This Directory

- `setup-heroku.sh` - Heroku deployment script
- `setup-do.sh` - DigitalOcean deployment script
- `setup-aws.sh` - AWS EC2 deployment script
- `generate_config.py` - Configuration generator for any platform
- `docker-compose.prod.yml` - Production docker compose (in root)
- `.env.production` - Production environment template (in root)

## Deployment Comparison

| Platform | Cost | Effort | Best For |
|----------|------|--------|----------|
| Heroku | $50/mo | ⭐ | Beginners |
| DigitalOcean | $12/mo | ⭐⭐ | Best Value |
| AWS | $15/mo | ⭐⭐⭐ | Scale |
| Google Cloud | $10/mo | ⭐⭐ | Integration |

## Environment Setup

Before deploying:

1. Generate strong keys:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Update `.env.production` with:
   - DB_PASSWORD
   - SECRET_KEY
   - Domain name
   - CORS origins

3. Run appropriate setup script

## Post-Deployment

```bash
# Verify deployment
curl https://yourdomain.com/api/health

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Database backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U $DB_USER $DB_NAME > backup.sql
```

## Support

For detailed instructions, see `DEPLOYMENT.md` in the root directory.

@echo off
REM Interactive Deployment Setup for Windows
REM This script helps you choose and configure your deployment

cls

echo.
echo ====================================================
echo   AI Resume Analyzer - Deployment Setup Wizard
echo ====================================================
echo.

echo Which platform would you like to deploy to?
echo.
echo 1) Heroku (Easiest - 5 minutes)
echo 2) DigitalOcean (Best Value - 15 minutes)
echo 3) AWS (Most Powerful - 20 minutes)
echo 4) Google Cloud (Enterprise - 15 minutes)
echo 5) Manual Setup (Any VPS)
echo.

set /p platform_choice="Enter your choice (1-5): "

if "%platform_choice%"=="1" (
    echo.
    echo Launching Heroku setup instructions...
    echo.
    echo 1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
    echo 2. Run: heroku login
    echo 3. Run: heroku create your-app-name
    echo 4. Run: heroku addons:create heroku-postgresql:standard-0
    echo 5. Set env vars and deploy
    echo.
    pause
) else if "%platform_choice%"=="2" (
    echo.
    echo DigitalOcean Setup:
    echo 1. Create Droplet: https://cloud.digitalocean.com
    echo 2. Choose Ubuntu 22.04, $12/month size
    echo 3. SSH into droplet: ssh root@YOUR_IP
    echo 4. Download: deploy/setup-do.sh (Windows Subsystem for Linux)
    echo 5. Or manually follow DEPLOYMENT.md
    echo.
    pause
) else if "%platform_choice%"=="3" (
    echo.
    echo AWS Setup:
    echo 1. Create EC2 Instance: https://console.aws.amazon.com/ec2
    echo 2. Choose Ubuntu 22.04, t3.medium
    echo 3. SSH into instance
    echo 4. Follow AWS setup in DEPLOYMENT.md
    echo 5. Or use deploy/setup-aws.sh (Windows Subsystem for Linux)
    echo.
    pause
) else if "%platform_choice%"=="4" (
    echo.
    echo Google Cloud Setup:
    echo 1. Go to https://console.cloud.google.com
    echo 2. Create new project
    echo 3. Enable Cloud SQL and Cloud Run APIs
    echo 4. Follow DEPLOYMENT.md for detailed steps
    echo.
    pause
) else if "%platform_choice%"=="5" (
    echo.
    echo Manual VPS Setup:
    echo 1. SSH into your server
    echo 2. Install Docker and Docker Compose
    echo 3. Clone repository: git clone your-repo
    echo 4. Update .env with production values
    echo 5. Run: docker-compose -f docker-compose.prod.yml up -d
    echo.
    echo See DEPLOYMENT.md for detailed instructions
    echo.
    pause
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)

echo.
echo ====================================================
echo Deployment setup complete!
echo ====================================================
echo.
echo For detailed help, see DEPLOY_ONLINE.md
echo.
pause

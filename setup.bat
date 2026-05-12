@echo off
echo ======================================
echo AI Resume Analyzer - Setup Script
echo ======================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo x Docker is not installed. Please install Docker first.
    exit /b 1
)
echo + Docker found

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo x Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)
echo + Docker Compose found
echo.

REM Copy environment files if they don't exist
if not exist ".env" (
    echo Copying .env file from .env.example...
    copy .env.example .env
    echo + .env created. Please update with your configuration.
)

if not exist "backend\.env" (
    echo Copying backend\.env file from backend\.env.example...
    copy backend\.env.example backend\.env
)

if not exist "frontend\.env.local" (
    echo Copying frontend\.env.local file from frontend\.env.example...
    copy frontend\.env.example frontend\.env.local
)

echo.
echo Building Docker images...
docker-compose build

echo.
echo Starting services...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10

echo.
echo All services started!
echo.
echo Access the application at:
echo   - Frontend: http://localhost:3000
echo   - Backend API: http://localhost:8000
echo   - API Documentation: http://localhost:8000/api/docs
echo.

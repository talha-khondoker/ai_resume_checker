# Development Setup Guide

This guide helps you set up the AI Resume Analyzer for local development.

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: 10GB free space
- **Internet**: Required for downloading dependencies

### Required Software

#### 1. Python 3.11+
```bash
# Verify installation
python --version

# Download: https://www.python.org/downloads/
```

#### 2. Node.js 18+
```bash
# Verify installation
node --version
npm --version

# Download: https://nodejs.org/
```

#### 3. PostgreSQL 15
```bash
# Verify installation
psql --version

# Download: https://www.postgresql.org/download/
```

#### 4. Git
```bash
# Verify installation
git --version

# Download: https://git-scm.com/
```

#### 5. Docker & Docker Compose (Optional but Recommended)
```bash
# Verify installation
docker --version
docker-compose --version

# Download: https://www.docker.com/products/docker-desktop
```

## Backend Development Setup

### Step 1: Clone Repository
```bash
cd /path/to/workspace
git clone <repository-url>
cd "ai resume"
```

### Step 2: Create Virtual Environment
```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download ML Models
```bash
python -m spacy download en_core_web_sm
```

### Step 5: Setup Environment Variables
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/ai_resume_analyzer
SECRET_KEY=your-development-secret-key
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Step 6: Initialize Database
```bash
# Start PostgreSQL
# Windows: Start service or run: pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql

# Create database
createdb ai_resume_analyzer

# Or using psql
psql -U postgres
CREATE DATABASE ai_resume_analyzer;
\q

# Tables will be created automatically on first run
```

### Step 7: Run Backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend is now running at:** http://localhost:8000

**API Documentation:** http://localhost:8000/api/docs

## Frontend Development Setup

### Step 1: Navigate to Frontend Directory
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Setup Environment Variables
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 4: Run Development Server
```bash
npm run dev
```

**Frontend is now running at:** http://localhost:3000

### Step 5: Build for Production (Optional)
```bash
npm run build
npm start
```

## Database Setup for Development

### Using PostgreSQL Client
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE ai_resume_analyzer;

# Connect to new database
\c ai_resume_analyzer

# Verify connection
\dt
```

### Using pgAdmin (GUI Tool)
1. Download pgAdmin from https://www.pgadmin.org/download/
2. Launch pgAdmin
3. Create new server: localhost:5432
4. Create new database: ai_resume_analyzer

### Sample Data (Optional)
```python
# Run from backend directory with activated venv
python
>>> from app.core.security import get_password_hash
>>> from app.db.database import SessionLocal
>>> from app.models.models import User, UserRole
>>>
>>> db = SessionLocal()
>>> user = User(
...     name="Test User",
...     email="test@example.com",
...     password=get_password_hash("password123"),
...     role=UserRole.USER
... )
>>> db.add(user)
>>> db.commit()
>>> exit()
```

## Development Workflow

### Backend Development
```bash
# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start development server (auto-reloads on file changes)
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

### Frontend Development
```bash
# Navigate to frontend
cd frontend

# Start development server (auto-reloads on file changes)
npm run dev

# Run linting
npm run lint

# Run tests
npm test

# Run tests in watch mode
npm run test:watch
```

### Database Changes
When you modify models in `backend/app/models/models.py`:

1. SQLAlchemy will automatically create/modify tables on application startup
2. For more complex migrations, use Alembic (optional setup):
```bash
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new column"

# Apply migration
alembic upgrade head
```

## Debugging

### Backend Debugging

#### Using Print Statements
```python
# In your code
print(f"Debug value: {variable}")

# View in terminal running uvicorn
```

#### Using PyCharm Debugger
1. Set breakpoints in code
2. Run: Debug configuration for FastAPI
3. Use Debug console

#### Using VS Code Debugger
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

### Frontend Debugging

#### Using Browser DevTools
- Press F12 or Right-click → Inspect
- Use Console tab for JavaScript errors
- Use Network tab for API calls
- Use React DevTools extension

#### Using VS Code Debugger
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "chrome",
      "request": "launch",
      "name": "Launch Chrome",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend"
    }
  ]
}
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'spacy'"
**Solution:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Issue: "ERROR: could not translate host name 'postgres' to address"
**Solution:** Ensure PostgreSQL is running
```bash
# Windows
pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start

# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Issue: "CORS error when frontend calls backend"
**Solution:** Update ALLOWED_ORIGINS in backend `.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000
```

### Issue: "npm ERR! code ERESOLVE"
**Solution:**
```bash
npm install --legacy-peer-deps
```

## Performance Tips

1. **Backend:**
   - Use connection pooling (configured in database.py)
   - Enable query caching with Redis (optional)
   - Profile with: `python -m cProfile -s cumtime app/main.py`

2. **Frontend:**
   - Use React DevTools Profiler
   - Check Network tab for slow requests
   - Use `next/image` for optimized images
   - Implement code splitting

3. **Database:**
   - Create indexes on frequently queried columns
   - Use EXPLAIN ANALYZE for slow queries
   - Regular vacuum and analyze

## Resources

- FastAPI Documentation: https://fastapi.tiangolo.com/
- Next.js Documentation: https://nextjs.org/docs
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- spaCy Documentation: https://spacy.io/

## Getting Help

- Check existing issues on GitHub
- Review API documentation at http://localhost:8000/api/docs
- Consult framework documentation
- Ask in development channels/forums

---

Happy coding! 🚀

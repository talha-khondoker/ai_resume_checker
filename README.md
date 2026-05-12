# AI Resume Analyzer

A production-ready AI-powered resume analysis system that helps users optimize their resumes and match them with job descriptions.

## 🚀 Features

### Core Features
- **Resume Upload**: Support for PDF and DOCX files with secure storage
- **ATS Score Calculation**: Analyze resume compatibility with Applicant Tracking Systems (0-100%)
- **Resume Parsing**: Extract name, email, phone, skills, education, experience, and certifications
- **Job Description Matching**: Match resume with job descriptions and get match percentage
- **AI-Powered Analysis**: NLP-based skill extraction and semantic matching
- **Smart Suggestions**: Generate improvement recommendations based on analysis
- **Role Recommendations**: Suggest suitable job roles based on detected skills

### Advanced Features
- **Skill Gap Analysis**: Identify missing skills with importance levels
- **Resume Strength Assessment**: Classify as weak/moderate/strong
- **Semantic Similarity Matching**: Beyond keyword matching using sentence embeddings
- **Grammar & Structure Feedback**: Resume quality assessment
- **Dashboard**: User-friendly interface for managing resumes and viewing analytics

### Admin Features
- **User Management**: View and manage registered users
- **System Statistics**: Monitor total users, resumes, and average ATS scores
- **Resume Monitoring**: Track all uploaded resumes and user activity
- **Analytics**: Access detailed reports on system usage

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework with SSR
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - Lightweight state management
- **Axios** - HTTP client
- **React Dropzone** - File upload handling
- **Chart.js** - Data visualization

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Relational database
- **Pydantic** - Data validation
- **JWT** - Authentication tokens

### AI/ML
- **spaCy** - NLP for named entity recognition
- **scikit-learn** - Machine learning utilities
- **Sentence Transformers** - Semantic embeddings
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX file parsing

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy

## 📋 Project Structure

```
ai resume/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── routes/
│   │   │       ├── auth.py   # Authentication endpoints
│   │   │       ├── resume.py # Resume management
│   │   │       └── admin.py  # Admin endpoints
│   │   ├── core/              # Core configuration
│   │   │   ├── config.py     # Settings
│   │   │   └── security.py   # JWT & security
│   │   ├── db/                # Database
│   │   │   └── database.py   # Connection & session
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   ├── auth_service.py
│   │   │   └── resume_service.py
│   │   ├── ml/                # AI/ML modules
│   │   │   └── analyzer.py   # Analysis logic
│   │   ├── utils/             # Utilities
│   │   │   └── file_handler.py
│   │   └── main.py           # FastAPI app entry
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile            # Docker image config
│   └── .gitignore
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── pages/            # Next.js pages
│   │   │   ├── index.tsx     # Landing page
│   │   │   ├── dashboard/    # User dashboard
│   │   │   ├── resume/       # Resume pages
│   │   │   └── auth/         # Auth pages
│   │   ├── components/       # React components
│   │   ├── services/         # API client
│   │   ├── context/          # State management
│   │   ├── hooks/            # Custom hooks
│   │   └── styles/           # Global styles
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── Dockerfile
│   └── .gitignore
├── docker-compose.yml         # Docker Compose config
├── nginx.conf                # Nginx configuration
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)

### Option 1: Using Docker Compose (Recommended)

1. **Clone and setup environment**
```bash
cd "e:\SDE\ai resume"
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. **Configure environment variables**
```bash
# backend/.env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ai_resume_analyzer
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,http://localhost
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Initialize database** (first time only)
```bash
docker-compose exec backend python -c "from app.db.database import Base, engine; from app.models.models import *; Base.metadata.create_all(bind=engine)"
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Nginx Proxy: http://localhost

### Option 2: Local Development Setup

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file
cp .env.example .env

# Run database migrations (optional - SQLAlchemy auto-creates tables)
python app/main.py  # This creates tables on first run

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Start development server
npm run dev
```

#### Database Setup (PostgreSQL)
```bash
# Create database
createdb ai_resume_analyzer

# Or using PostgreSQL client
psql -U postgres -c "CREATE DATABASE ai_resume_analyzer;"
```

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}

Response: 200 OK
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Resume Endpoints

#### Upload Resume
```http
POST /api/resume/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: <binary>

Response: 200 OK
{
  "id": 1,
  "filename": "resume.pdf",
  "file_path": "app/uploads/uuid.pdf",
  "is_processed": false,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Get Resume History
```http
GET /api/resume/history?skip=0&limit=50
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "id": 1,
    "filename": "resume.pdf",
    "ats_score": 85.5,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Analyze Resume
```http
POST /api/resume/analyze
Authorization: Bearer {token}
Content-Type: application/json

{
  "resume_id": 1,
  "job_description": "We are looking for a Senior Python Developer...",
  "analyze_type": "full"
}

Response: 200 OK
{
  "id": 1,
  "resume_id": 1,
  "ats_score": 85.5,
  "match_score": 75.2,
  "matching_skills": [
    {"skill": "python", "match_percentage": 100, "relevance": "high"}
  ],
  "missing_skills": ["kubernetes", "aws"],
  "suggestions": ["Add more technical skills..."],
  "resume_strength": "strong",
  "recommended_roles": ["Senior Python Developer", "Backend Engineer"]
}
```

#### Match with Job
```http
POST /api/resume/job-match
Authorization: Bearer {token}
Content-Type: application/json

{
  "resume_id": 1,
  "job_description": "Senior Backend Engineer needed..."
}

Response: 200 OK
{
  "match_score": 78.5,
  "matching_skills": [...],
  "missing_skills": [...],
  "skill_gaps": [...],
  "recommendations": [...]
}
```

### Admin Endpoints

#### Get Statistics
```http
GET /api/admin/stats
Authorization: Bearer {admin-token}

Response: 200 OK
{
  "total_users": 150,
  "active_users": 145,
  "total_resumes": 342,
  "average_ats_score": 72.5
}
```

#### Get Users Report
```http
GET /api/admin/users?skip=0&limit=50
Authorization: Bearer {admin-token}
```

#### Delete User
```http
DELETE /api/admin/users/{user_id}
Authorization: Bearer {admin-token}
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **CORS Protection**: Configured CORS headers
- **Input Validation**: Pydantic schemas for request validation
- **File Upload Sanitization**: Secure file handling with validation
- **Rate Limiting**: Ready for implementation
- **HTTPS Support**: Configured for production SSL/TLS
- **Environment Variables**: Sensitive data in .env files

## 🤖 AI/ML Features

### Resume Parsing
- Named entity recognition for extracting names
- Email and phone number extraction using regex
- Structured section detection (experience, education, etc.)

### Skill Extraction
- Technical skill recognition from text
- Multi-word skill detection
- Skill matching against comprehensive database

### ATS Score Calculation
- Text quality assessment
- Keyword density analysis
- Format compatibility checking
- Standard structure validation

### Job Matching
- TF-IDF keyword matching
- Semantic similarity using sentence embeddings
- Skill gap analysis with importance levels
- Combined scoring mechanism

### Recommendations
- Dynamic suggestion generation based on analysis
- Role recommendations using skill mapping
- Improvement suggestions for ATS optimization

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  role ENUM('user', 'admin'),
  is_active BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Resumes Table
```sql
CREATE TABLE resumes (
  id SERIAL PRIMARY KEY,
  user_id INTEGER FOREIGN KEY,
  filename VARCHAR(255),
  file_path VARCHAR(512),
  extracted_text TEXT,
  ats_score FLOAT,
  is_processed BOOLEAN,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

### Analysis Reports Table
```sql
CREATE TABLE analysis_reports (
  id SERIAL PRIMARY KEY,
  resume_id INTEGER FOREIGN KEY,
  job_description TEXT,
  match_score FLOAT,
  matching_skills TEXT (JSON),
  missing_skills TEXT (JSON),
  suggestions TEXT (JSON),
  resume_strength VARCHAR(50),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/
pytest tests/ -v  # Verbose
pytest tests/ --cov  # With coverage
```

### Run Frontend Tests
```bash
cd frontend
npm test
npm run test:watch
```

## 📈 Performance Optimization

- **Database Indexing**: Indexes on frequently queried columns
- **Query Optimization**: Efficient SQLAlchemy queries
- **Caching**: Browser caching for static assets
- **Code Splitting**: Next.js automatic code splitting
- **Image Optimization**: Next.js image optimization
- **Lazy Loading**: Component-level lazy loading

## 🔧 Configuration

### Environment Variables

#### Backend
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ai_resume_analyzer

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000

# File Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_FOLDER=app/uploads
ALLOWED_EXTENSIONS=pdf,docx

# ML Model
SPACY_MODEL=en_core_web_sm
SIMILARITY_THRESHOLD=0.6
```

#### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 Deployment

### Docker Deployment

1. **Build images**
```bash
docker-compose build
```

2. **Run containers**
```bash
docker-compose up -d
```

3. **Scale backend**
```bash
docker-compose up -d --scale backend=3
```

### Production Deployment (AWS)

1. **Push images to ECR**
```bash
aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
docker tag ai-resume-backend <account-id>.dkr.ecr.<region>.amazonaws.com/ai-resume-backend:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/ai-resume-backend:latest
```

2. **Deploy using ECS/EKS**
- Configure ECS task definitions
- Set up load balancer
- Configure auto-scaling policies

3. **Set up RDS for PostgreSQL**
- Create managed PostgreSQL instance
- Update DATABASE_URL in environment

4. **Configure S3 for file storage**
- Create S3 bucket for resume uploads
- Update file upload configuration

## 🐛 Troubleshooting

### Backend Issues

**Port already in use**
```bash
lsof -i :8000
kill -9 <PID>
```

**Database connection error**
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure database exists

**spaCy model not found**
```bash
python -m spacy download en_core_web_sm
```

### Frontend Issues

**Port already in use**
```bash
lsof -i :3000
kill -9 <PID>
```

**Module not found**
```bash
npm install
npm install --save react-dropzone zustand
```

## 📧 Support & Contribution

For issues, questions, or contributions, please:
1. Check existing issues
2. Create a detailed issue report
3. Submit pull requests with improvements

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- spaCy for NLP capabilities
- Sentence Transformers for embeddings
- FastAPI for the web framework
- Next.js for the frontend framework
- The open-source community

---

**Built with ❤️ for better resumes**

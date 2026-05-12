# Quick Reference Guide

## 🚀 Start Application

### Docker (Recommended)
```bash
cd "e:\SDE\ai resume"
docker-compose up -d
```

### Local Development
```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 🌐 Access Points

| Service | URL | Notes |
|---------|-----|-------|
| Frontend | http://localhost:3000 | Main app |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/api/docs | Swagger UI |
| ReDoc | http://localhost:8000/api/redoc | API documentation |
| Health Check | http://localhost:8000/api/health | Health status |

---

## 📝 Common Commands

### Backend

#### Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### Development
```bash
uvicorn app.main:app --reload
```

#### Database
```bash
createdb ai_resume_analyzer
psql -U postgres -d ai_resume_analyzer
```

#### Tests
```bash
pytest
pytest --cov
```

### Frontend

#### Setup
```bash
cd frontend
npm install
```

#### Development
```bash
npm run dev
```

#### Build
```bash
npm run build
npm start
```

#### Tests
```bash
npm test
npm run test:watch
```

---

## 📚 Key Files

### Backend
- `app/main.py` - FastAPI application
- `app/core/config.py` - Configuration
- `app/core/security.py` - Authentication
- `app/models/models.py` - Database models
- `app/ml/analyzer.py` - AI/ML logic
- `app/api/routes/` - API endpoints

### Frontend
- `src/pages/index.tsx` - Landing page
- `src/pages/dashboard/` - Dashboard
- `src/pages/resume/` - Resume pages
- `src/services/api.ts` - API client
- `src/context/` - State management

---

## 🔑 Environment Variables

### Backend `.env`
```env
DATABASE_URL=postgresql://user:password@localhost:5432/db
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 Testing API

### Using Postman
1. Import `API_COLLECTION.postman_collection.json`
2. Update variables (tokens, IDs)
3. Run requests

### Using cURL
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"test123"}'
```

---

## 🐛 Debugging

### Backend
- Logs in terminal running `uvicorn`
- Use `print()` statements
- Check FastAPI docs at `/api/docs`

### Frontend
- Browser DevTools (F12)
- Network tab for API calls
- Console for JavaScript errors
- React DevTools extension

---

## 📊 Project Structure

```
ai resume/
├── backend/              # FastAPI backend
│   ├── app/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/             # Next.js frontend
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── README.md
├── DEVELOPMENT.md
└── PROJECT_SUMMARY.md
```

---

## 🔐 Security Checklist

- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False for production
- [ ] Update ALLOWED_ORIGINS
- [ ] Use strong database password
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Regular security updates

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
lsof -i :8000        # Find process
kill -9 <PID>        # Kill process
```

### Database Connection Error
- Check PostgreSQL is running
- Verify DATABASE_URL
- Check database exists

### Dependencies Error
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Frontend Module Not Found
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 📈 Performance Tips

1. **Database**: Add indexes on frequently queried columns
2. **Backend**: Enable caching with Redis
3. **Frontend**: Use React DevTools Profiler
4. **Network**: Monitor with browser Network tab

---

## 🚀 Deployment

### Docker Compose
```bash
docker-compose up -d              # Start
docker-compose down               # Stop
docker-compose logs -f backend    # View logs
```

### Scale Backend
```bash
docker-compose up -d --scale backend=3
```

### Push to Docker Hub
```bash
docker tag ai-resume-backend username/ai-resume:latest
docker push username/ai-resume:latest
```

---

## 📞 Quick Help

### API Response Format
```json
{
  "data": {...},
  "message": "Success",
  "status": 200
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

### Token Format
```
Authorization: Bearer <token>
```

---

## 📚 Resources

- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/
- PostgreSQL: https://www.postgresql.org/
- Docker: https://www.docker.com/

---

## ✨ Tips & Tricks

1. **Reload on Changes**: Backend auto-reloads with `--reload`
2. **Fast Iteration**: Use Postman for API testing
3. **Database Shell**: `psql -U postgres -d ai_resume_analyzer`
4. **View Container Logs**: `docker logs <container_id>`
5. **Database Client**: Use pgAdmin for GUI management

---

## 🎯 Next Steps

1. [ ] Run setup script
2. [ ] Create test account
3. [ ] Upload a resume
4. [ ] Run analysis
5. [ ] Test job matching
6. [ ] Deploy to production

---

**Happy coding! 🚀**

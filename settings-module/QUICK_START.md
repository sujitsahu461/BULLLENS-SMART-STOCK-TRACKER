# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Node.js 14+ and npm 6+
- MongoDB (local or Atlas)
- Git

### Backend Setup

```bash
# 1. Navigate to backend
cd settings-module/backend

# 2. Install dependencies
npm install

# 3. Create .env file
cat > .env << EOF
PORT=5000
NODE_ENV=development
MONGODB_URI=mongodb://localhost:27017/stock-predictor-settings
JWT_SECRET=your_secret_key_here
JWT_REFRESH_SECRET=your_refresh_secret_here
FRONTEND_URL=http://localhost:3000
EOF

# 4. Start server
npm run dev
```

Backend ready at: `http://localhost:5000`

### Frontend Setup

```bash
# 1. Navigate to frontend
cd settings-module/frontend

# 2. Install dependencies
npm install

# 3. Create .env.local
cat > .env.local << EOF
REACT_APP_API_URL=http://localhost:5000/api
EOF

# 4. Start development server
npm start
```

Frontend ready at: `http://localhost:3000`

### Verify Installation

```bash
# Check backend health
curl http://localhost:5000/api/health

# Response should be:
{
  "status": "OK",
  "uptime": 123.456,
  "mongodb": "Connected"
}
```

---

## 📝 First Time Setup Checklist

```
Backend
  ✓ Install Node.js
  ✓ Install MongoDB
  ✓ npm install dependencies
  ✓ Create .env file
  ✓ Start server (npm run dev)
  ✓ Verify /health endpoint

Frontend
  ✓ npm install dependencies
  ✓ Create .env.local
  ✓ Start app (npm start)
  ✓ Test login/register

Database
  ✓ MongoDB running locally or connect to Atlas
  ✓ Database created automatically
  ✓ Collections created on first write
```

---

## 🔧 Common Commands

### Backend
```bash
# Development
npm run dev

# Production
NODE_ENV=production npm start

# Tests
npm test

# Linting
npm run lint
```

### Frontend
```bash
# Start development
npm start

# Build for production
npm run build

# Tests
npm test

# Eject (irreversible!)
npm run eject
```

---

## 🛠️ Troubleshooting

### Backend won't start
```bash
# Check MongoDB connection
mongosh

# Check port 5000 is free
lsof -i :5000

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Frontend won't compile
```bash
# Clear cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install

# Clear React cache
rm -rf src\.react-cache
```

### API calls failing
```bash
# Check BACKEND is running on 5000
# Check FRONTEND_URL in .env matches origin
# Check CORS is enabled
# Verify MongoDB connection string
```

---

## 📚 Default Test Credentials

After creating a user:

```json
{
  "email": "test@example.com",
  "password": "Test123!",
  "username": "testuser"
}
```

---

## 🎯 Next Steps

1. **Customize Styling**
   - Edit `frontend/tailwind.config.js`
   - Modify colors in `frontend/src/styles/index.css`

2. **Add More Settings Categories**
   - Create new component in `frontend/src/components/`
   - Add controller in `backend/controllers/`
   - Create route in `backend/routes/`

3. **Integrate with Main App**
   - Mount API routes
   - Share authentication context
   - Import React components

4. **Deploy**
   - Follow [DEPLOYMENT.md](./DEPLOYMENT.md)
   - Set up CI/CD pipeline
   - Configure production environment

---

## 📞 Support

- Check [README.md](./README.md) for full documentation
- Review [API_CONTRACT.md](./API_CONTRACT.md) for API details
- See [ARCHITECTURE.md](./ARCHITECTURE.md) for design overview

---

Version 1.0.0 | April 5, 2026

# Deployment Guide

## Production Deployment

### Backend Deployment (MongoDB Atlas + Heroku/AWS)

#### 1. Prepare MongoDB Atlas
```bash
# Create MongoDB Atlas cluster
# Get connection string: mongodb+srv://user:pass@cluster.mongodb.net/dbname
```

#### 2. Environment Configuration
```bash
# .env (Production)
NODE_ENV=production
PORT=5000
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/stock-predictor
JWT_SECRET=your_super_secure_secret_key_HERE
JWT_REFRESH_SECRET=your_super_secure_refresh_key_HERE
FRONTEND_URL=https://yourdomain.com
```

#### 3. Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create stock-predictor-settings-api

# Add environment variables
heroku config:set NODE_ENV=production
heroku config:set MONGODB_URI=your_connection_string
heroku config:set JWT_SECRET=your_secret

# Deploy
git push heroku main
```

#### 4. Deploy to AWS (EC2)
```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Clone repository
git clone your-repo
cd settings-module/backend

# Install dependencies
npm install

# Start with PM2
npm install -g pm2
pm2 start server.js --name "settings-api"
pm2 startup
pm2 save
```

### Frontend Deployment (Vercel/Netlify)

#### 1. Build for Production
```bash
cd settings-module/frontend
npm run build
```

#### 2. Deploy to Vercel
```bash
npm install -g vercel
vercel
```

#### 3. Environment Variables
```bash
REACT_APP_API_URL=https://api.yourdomain.com/api
```

#### 4. Deploy to Netlify
```bash
# Option 1: CLI
npm install -g netlify-cli
netlify deploy --prod --dir=build

# Option 2: Git push (connect repo to Netlify)
```

### Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production

COPY . .

EXPOSE 5000

CMD ["node", "server.js"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      MONGODB_URI: mongodb://root:password@mongodb:27017/stock-predictor
      NODE_ENV: production
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://backend:5000/api

volumes:
  mongodb_data:
```

### Production Checklist

- [ ] Set strong JWT secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up MongoDB backups
- [ ] Enable rate limiting
- [ ] Configure logging and monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Enable security headers (Helmet)
- [ ] Configure email service for alerts
- [ ] Set up CDN for frontend assets
- [ ] Enable database indexing
- [ ] Configure caching strategy
- [ ] Set up CI/CD pipeline
- [ ] Enable database encryption
- [ ] Regular security audits

### Monitoring & Logging

```javascript
// Configure Winston for logging
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

### Backup Strategy

```bash
# Automated MongoDB backup
mongodump --uri="mongodb://user:pass@host:port/dbname" --out=/backups/$(date +%Y%m%d)

# Schedule with cron
0 2 * * * mongodump --uri="..." --out=/backups/$(date +\%Y\%m\%d)
```

### Performance Optimization

1. **Database Optimization**
   - Add indexes on frequently queried fields
   - Set TTL on audit logs (90 days)

2. **API Optimization**
   - Enable compression (gzip)
   - Cache responses
   - Pagination for large datasets

3. **Frontend Optimization**
   - Code splitting
   - Lazy loading
   - Image optimization
   - CSS minification

---

Deployment Version: 1.0.0
Last Updated: April 5, 2026

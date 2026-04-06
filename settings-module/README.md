# Settings Module - Stock Market Predictor

A comprehensive, production-ready settings system for the Stock Market Prediction application built with React, Node.js, Express, and MongoDB.

## 🎯 Features

### 1. **User Profile Settings**
- User information management
- Risk profile selection (Beginner, Moderate, Aggressive)
- Currency preference
- Brokerage account linking

### 2. **Prediction Preferences**
- Model selection (LSTM, ML, Hybrid)
- Prediction horizon configuration
- Confidence threshold adjustment
- Volatility filtering

### 3. **Notifications & Alerts**
- Price alerts with custom thresholds
- Buy/Sell prediction alerts
- News-based alerts
- Multiple notification channels (Email, Push, SMS)
- Quiet hours configuration

### 4. **Portfolio Settings**
- Real portfolio synchronization
- Demo mode toggle
- P&L auto-tracking
- Risk exposure limits

### 5. **Dashboard Customization**
- Default homepage selection
- Chart type preferences
- Timeframe defaults
- Dark/Light mode toggle
- Compact view option

### 6. **AI Behavior Settings**
- Explanation levels (Simple, Intermediate, Technical)
- AI transparency mode
- Risk warnings toggle
- Auto-suggestion configuration

### 7. **Data & Market Settings**
- Market selection (NSE, BSE, Crypto, US)
- Data refresh frequency
- Global indicators toggle

### 8. **Security Settings**
- Two-Factor Authentication (2FA)
- Login alerts
- Device/session management
- API key management

### 9. **Localization**
- Multi-language support
- Timezone configuration
- Market hours synchronization

### 10. **Advanced Features**
- Custom indicators
- Backtesting configuration
- Strategy builder support
- Audit logging
- Settings export/import

## 🏗️ Architecture

```
settings-module/
├── backend/
│   ├── config/              # Configuration files
│   ├── controllers/         # Business logic
│   │   ├── authController.js
│   │   ├── userController.js
│   │   └── settingsController.js
│   ├── models/              # MongoDB schemas
│   │   ├── User.js
│   │   ├── Settings.js
│   │   └── Audit.js
│   ├── middleware/          # Express middleware
│   │   ├── auth.js
│   │   ├── errorHandler.js
│   │   ├── logger.js
│   │   └── validation.js
│   ├── routes/              # API routes
│   │   ├── authRoutes.js
│   │   ├── userRoutes.js
│   │   └── settingsRoutes.js
│   ├── utils/               # Utility functions
│   ├── server.js            # Express app entry
│   ├── package.json
│   └── .env.example
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/      # React components
    │   │   ├── UI.jsx       # Reusable UI components
    │   │   ├── ProfileSettings.jsx
    │   │   ├── PredictionSettings.jsx
    │   │   ├── NotificationSettings.jsx
    │   │   ├── DashboardSettings.jsx
    │   │   ├── AIBehaviorSettings.jsx
    │   │   ├── LocalizationSettings.jsx
    │   │   └── SecuritySettings.jsx
    │   ├── pages/
    │   │   └── SettingsPage.jsx
    │   ├── context/
    │   │   └── store.js     # Zustand state management
    │   ├── utils/
    │   │   └── api.js       # API client
    │   ├── styles/
    │   │   └── index.css
    │   ├── App.jsx
    │   ├── index.js
    │   └── package.json
    ├── tailwind.config.js
    └── public/index.html
```

## 📋 Database Schema

### User Schema
```javascript
{
  username: String (unique, required),
  email: String (unique, required),
  password: String (hashed),
  firstName: String,
  lastName: String,
  profilePhoto: {
    url: String,
    uploadedAt: Date
  },
  emailVerified: Boolean,
  twoFactorEnabled: Boolean,
  loginAttempts: Number,
  lastLogin: Date,
  settings: ObjectId (ref: Settings),
  createdAt: Date,
  updatedAt: Date
}
```

### Settings Schema
Comprehensive settings document with nested structures:
- `profile`: User profile settings
- `predictions`: Prediction model configuration
- `notifications`: Alert and notification preferences
- `portfolio`: Portfolio tracking settings
- `dashboard`: UI customization
- `aiBehavior`: AI behavior configuration
- `market`: Market data settings
- `security`: Security preferences
- `advanced`: Advanced features
- `localization`: Language and timezone
- `auditLog`: Changes history

### Audit Schema
```javascript
{
  userId: ObjectId (ref: User),
  action: String (CREATE, UPDATE, DELETE, LOGIN, etc),
  resourceType: String (Settings, User, etc),
  resourceId: String,
  changes: Mixed,
  ipAddress: String,
  userAgent: String,
  timestamp: Date (TTL: 90 days),
  status: String (Success, Failed)
}
```

## 🚀 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh-token` - Refresh access token
- `POST /api/auth/logout` - User logout
- `POST /api/auth/2fa/enable` - Enable 2FA
- `POST /api/auth/2fa/disable` - Disable 2FA

### User Management
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update profile
- `POST /api/users/change-password` - Change password
- `GET /api/users/login-history` - Login history
- `DELETE /api/users/account` - Delete account

### Settings
- `GET /api/settings` - Get all settings
- `PATCH /api/settings` - Update multiple settings
- `PUT /api/settings/profile` - Update profile settings
- `PUT /api/settings/predictions` - Update prediction settings
- `PUT /api/settings/notifications` - Update notification settings
- `PUT /api/settings/dashboard` - Update dashboard settings
- `PUT /api/settings/ai-behavior` - Update AI behavior
- `PUT /api/settings/localization` - Update localization
- `POST /api/settings/reset` - Reset to defaults
- `GET /api/settings/audit-log` - Get audit log

## 🛠️ Setup & Installation

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd settings-module/backend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start development server:**
```bash
npm run dev
```

Backend runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd settings-module/frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create .env.local:**
```bash
REACT_APP_API_URL=http://localhost:5000/api
```

4. **Start development server:**
```bash
npm start
```

Frontend runs on `http://localhost:3000`

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt with salting
- **2FA Support**: TOTP, Email, SMS options
- **Account Lockout**: Automatic lockout after failed attempts
- **Audit Logging**: Track all setting changes
- **Rate Limiting**: Prevent brute force attacks
- **CORS Protection**: Configured CORS headers
- **Helmet.js**: Security headers
- **Input Validation**: Joi schema validation
- **SQL Injection Protection**: Mongoose parameterized queries

## 📊 State Management

Using **Zustand** for lightweight, performant state management:

```javascript
// Authentication store
- user
- accessToken
- isLoading
- error

// Settings store
- settings
- isLoading
- isDirty
- error

// Notification store
- notifications array
```

## 🎨 UI Components

### Reusable Components (UI.jsx)
- `Toggle`: Binary on/off switch
- `Slider`: Value range selector
- `Dropdown`: Select from options
- `Card`: Container with title
- `Button`: Various button styles
- `Tooltip`: Contextual help
- `Badge`: Status indicators

### Features
- Smooth animations (Framer Motion)
- Responsive design (Tailwind CSS)
- Dark mode support
- Accessibility compliant
- Toast notifications

## 🧪 Testing

### Backend Tests
```bash
npm test
```

### Frontend Tests
```bash
npm test
```

## 📦 Deployment

### Backend (Node.js)
```bash
# Build for production
npm run build

# Start production server
NODE_ENV=production npm start
```

### Frontend (React)
```bash
# Build static files
npm run build

# Deploy 'build' folder to static hosting
```

## 🔄 Integration with Main App

To integrate the settings module with your existing Stock Market Predictor:

1. **Backend Integration:**
   - Mount settings API routes to your main Express app
   - Share MongoDB instance
   - Integrate authentication system

2. **Frontend Integration:**
   - Embed SettingsPage in your routing
   - Share authentication context
   - Use same styling system

## 📈 Performance Optimization

- MongoDB indexing on frequently queried fields
- Server-side pagination for audit logs
- Client-side caching with Zustand
- Lazy loading of components
- Code splitting with React Router
- Image optimization for profile photos

## 🐛 Error Handling

- Comprehensive error messages
- User-friendly notifications
- Proper HTTP status codes
- Detailed server logging
- Try-catch blocks in async operations

## 📝 Best Practices

- RESTful API design
- Separation of concerns
- DRY principle
- Proper naming conventions
- Environment variable configuration
- Security best practices
- Code documentation
- Audit trails

## 🚢 Scaling Considerations

- Database sharding for large user bases
- Redis caching for settings
- Load balancing for API
- CDN for frontend assets
- Microservices architecture
- Message queues for notifications

## 📚 Additional Resources

- [Express.js Documentation](https://expressjs.com)
- [React Documentation](https://react.dev)
- [MongoDB Documentation](https://docs.mongodb.com)
- [Tailwind CSS](https://tailwindcss.com)
- [Zustand](https://github.com/pmndrs/zustand)

## 📄 License

MIT License - Feel free to use this in your projects

## 👥 Contributors

Stock Predictor Team

## 💬 Support

For issues or questions, please create an issue in the repository.

---

**Last Updated**: April 5, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅

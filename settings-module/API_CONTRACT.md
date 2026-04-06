# API Contract & Documentation

## Overview
Complete REST API for the Settings Module. All endpoints require authentication via Bearer token (JWT) unless specified.

## Base URL
```
http://localhost:5000/api
```

## Authentication
All protected endpoints require:
```
Authorization: Bearer {accessToken}
```

## Response Format
### Success Response (200)
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error description",
  "errors": ["field1: error", "field2: error"]
}
```

---

## Authentication Endpoints

### 1. Register User
**POST** `/auth/register`

Request:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

Response (201):
```json
{
  "success": true,
  "data": {
    "userId": "user_id",
    "username": "john_doe",
    "email": "john@example.com",
    "accessToken": "jwt_token",
    "refreshToken": "refresh_token"
  }
}
```

---

### 2. Login
**POST** `/auth/login`

Request:
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

Response (200):
```json
{
  "success": true,
  "data": {
    "userId": "user_id",
    "username": "john_doe",
    "email": "john@example.com",
    "accessToken": "jwt_token",
    "refreshToken": "refresh_token"
  }
}
```

---

### 3. Refresh Token
**POST** `/auth/refresh-token`

Request:
```json
{
  "refreshToken": "old_refresh_token"
}
```

Response (200):
```json
{
  "success": true,
  "data": {
    "accessToken": "new_access_token",
    "refreshToken": "new_refresh_token"
  }
}
```

---

### 4. Logout
**POST** `/auth/logout` (Protected)

Response (200):
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### 5. Enable 2FA
**POST** `/auth/2fa/enable` (Protected)

Request:
```json
{
  "method": "TOTP | Email | SMS"
}
```

Response (200):
```json
{
  "success": true,
  "message": "2FA enabled with TOTP"
}
```

---

## User Management Endpoints

### 1. Get Profile
**GET** `/users/profile` (Protected)

Response (200):
```json
{
  "success": true,
  "data": {
    "id": "user_id",
    "username": "john_doe",
    "email": "john@example.com",
    "firstName": "John",
    "lastName": "Doe",
    "profilePhoto": {
      "url": "https://...",
      "uploadedAt": "2024-01-01T12:00:00Z"
    },
    "emailVerified": true,
    "twoFactorEnabled": false,
    "createdAt": "2024-01-01T12:00:00Z"
  }
}
```

---

### 2. Update Profile
**PUT** `/users/profile` (Protected)

Request:
```json
{
  "firstName": "Jonathan",
  "lastName": "Doe",
  "preferredCurrency": "USD"
}
```

Response (200):
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": "user_id",
    "username": "john_doe",
    "email": "john@example.com",
    "firstName": "Jonathan",
    "lastName": "Doe"
  }
}
```

---

### 3. Change Password
**POST** `/users/change-password` (Protected)

Request:
```json
{
  "currentPassword": "OldPass123!",
  "newPassword": "NewPass456!"
}
```

Response (200):
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

## Settings Endpoints

### 1. Get All Settings
**GET** `/settings` (Protected)

Response (200):
```json
{
  "success": true,
  "data": {
    "_id": "settings_id",
    "userId": "user_id",
    "profile": {
      "riskProfile": "Moderate",
      "preferredCurrency": "INR",
      "brokerageAccounts": []
    },
    "predictions": {
      "modelSelection": "Hybrid",
      "predictionHorizon": "Short-term",
      "confidenceThreshold": 60,
      "volatilityFilterEnabled": true
    },
    "notifications": { /* ... */ },
    "dashboard": { /* ... */ },
    "aiBehavior": { /* ... */ },
    "localization": { /* ... */ },
    "createdAt": "2024-01-01T12:00:00Z",
    "updatedAt": "2024-01-01T12:00:00Z"
  }
}
```

---

### 2. Update Profile Settings
**PUT** `/settings/profile` (Protected)

Request:
```json
{
  "riskProfile": "Aggressive",
  "preferredCurrency": "USD",
  "brokerageAccounts": [
    {
      "accountName": "Zerodha",
      "brokerName": "ZERODHA",
      "accountNumber": "1234567890",
      "isLinked": true
    }
  ]
}
```

Response (200):
```json
{
  "success": true,
  "message": "Profile settings updated",
  "data": {
    "riskProfile": "Aggressive",
    "preferredCurrency": "USD",
    "brokerageAccounts": [...]
  }
}
```

---

### 3. Update Prediction Settings
**PUT** `/settings/predictions` (Protected)

Request:
```json
{
  "modelSelection": "LSTM",
  "predictionHorizon": "Long-term",
  "confidenceThreshold": 75,
  "volatilityFilterEnabled": true,
  "volatilityThreshold": 25
}
```

Response (200):
```json
{
  "success": true,
  "message": "Prediction settings updated",
  "data": {
    "modelSelection": "LSTM",
    "predictionHorizon": "Long-term",
    "confidenceThreshold": 75,
    "volatilityFilterEnabled": true
  }
}
```

---

### 4. Update Notification Settings
**PUT** `/settings/notifications` (Protected)

Request:
```json
{
  "priceAlerts": {
    "enabled": true,
    "threshold": 5
  },
  "predictionAlerts": {
    "enabled": true,
    "buySellHints": true
  },
  "channels": {
    "email": true,
    "push": false,
    "sms": false,
    "inApp": true
  },
  "quietHours": {
    "enabled": true,
    "startTime": "22:00",
    "endTime": "08:00"
  }
}
```

Response (200):
```json
{
  "success": true,
  "message": "Notification settings updated",
  "data": { /* notification settings */ }
}
```

---

### 5. Update Dashboard Settings
**PUT** `/settings/dashboard` (Protected)

Request:
```json
{
  "defaultHomepage": "Portfolio",
  "chartType": "Candlestick",
  "defaultTimeframe": "1D",
  "darkMode": true,
  "compactView": false
}
```

Response (200):
```json
{
  "success": true,
  "message": "Dashboard settings updated",
  "data": { /* dashboard settings */ }
}
```

---

### 6. Update AI Behavior
**PUT** `/settings/ai-behavior` (Protected)

Request:
```json
{
  "explanationLevel": "Technical",
  "transparencyMode": true,
  "showRiskWarnings": true,
  "autoSuggestions": false
}
```

Response (200):
```json
{
  "success": true,
  "message": "AI behavior settings updated",
  "data": { /* AI behavior settings */ }
}
```

---

### 7. Update Localization
**PUT** `/settings/localization` (Protected)

Request:
```json
{
  "language": "hi",
  "timezone": "Asia/Kolkata",
  "marketHoursSync": true
}
```

Response (200):
```json
{
  "success": true,
  "message": "Localization settings updated",
  "data": { /* localization settings */ }
}
```

---

### 8. Reset to Defaults
**POST** `/settings/reset` (Protected)

Response (200):
```json
{
  "success": true,
  "message": "Settings reset to defaults",
  "data": { /* default settings */ }
}
```

---

### 9. Get Audit Log
**GET** `/settings/audit-log?limit=50&page=1` (Protected)

Response (200):
```json
{
  "success": true,
  "data": [
    {
      "_id": "audit_id",
      "userId": "user_id",
      "action": "UPDATE",
      "resourceType": "Settings",
      "changes": { /* changes object */ },
      "ipAddress": "192.168.1.1",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 100,
    "pages": 2
  }
}
```

---

## Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | Internal server error |

---

## Validation Rules

### Password
- Minimum 6 characters
- Should contain uppercase, lowercase, numbers
- Recommended: 12+ characters with special chars

### Email
- Valid email format
- Unique in database

### Username
- 3-30 alphanumeric characters
- Unique in database
- Lowercase preferred

### Confidence Threshold
- Range: 0-100 (percentage)

### Risk Profile
- Enum: `Beginner`, `Moderate`, `Aggressive`

### Languages Supported
- en, hi, es, fr, de, zh, ja

---

## Rate Limiting

- **General**: 100 requests per 15 minutes per IP
- **Auth**: 5 requests per minute per IP
- **Status**: 429 Too Many Requests with Retry-After header

---

## CORS Configuration

Allowed Origins:
- http://localhost:3000 (development)
- https://stockpredictor.com (production)

Allowed Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS

---

Version: 1.0.0  
Last Updated: April 5, 2026

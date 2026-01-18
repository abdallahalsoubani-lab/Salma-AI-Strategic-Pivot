# Salma AI Gateway - Authentication & Core Gateway System

بوابة سلمى - نظام الذكاء الاصطناعي الموحد

## Overview

Salma AI Gateway is a comprehensive platform that provides:
- **Authentication System**: Secure user registration, login, and API key management
- **AI Provider Gateway**: Unified interface to multiple AI providers (Claude, OpenAI, Jais)
- **Cost Tracking**: Estimate and monitor costs across different AI models
- **Arabic-First Interface**: Full RTL support with Arabic translations

## Architecture

```
┌─────────────────────┐
│   React Frontend    │
│   (RTL Arabic UI)   │
└──────────┬──────────┘
           │
           ├─── JWT/API Key Auth
           │
┌──────────▼──────────┐
│  FastAPI Backend    │
│  - Auth & Routes    │
│  - API Key Mgmt     │
│  - Gateway Logic    │
└──────────┬──────────┘
           │
           ├─── User DB
           ├─── API Keys
           └─── Logs
```

## Features

### 1. Authentication
- ✅ User Registration with validation
- ✅ Email/Password Login
- ✅ JWT Token Management (Access + Refresh)
- ✅ API Key Generation and Management
- ✅ Rate Limiting on Login
- ✅ Auth Logs

### 2. API Gateway
- ✅ Unified Chat Interface
- ✅ Multiple AI Provider Support (Claude, OpenAI, Jais)
- ✅ Cost Estimation
- ✅ Token Usage Tracking
- ✅ Request/Response Logging

### 3. Frontend
- ✅ Arabic RTL Interface
- ✅ Login & Registration Pages
- ✅ Dashboard
- ✅ API Keys Management
- ✅ Protected Routes
- ✅ Responsive Design

## Project Structure

```
Salma-AI-Strategic-Pivot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── api_keys.py      # API key management
│   │   │   │   └── gateway.py       # AI Gateway endpoints
│   │   │   └── dependencies.py      # Auth middleware
│   │   ├── core/
│   │   │   ├── config.py            # Configuration
│   │   │   └── security.py          # JWT & crypto
│   │   ├── models/
│   │   │   ├── user.py              # Database models
│   │   │   └── schemas.py           # Pydantic models
│   │   ├── services/
│   │   │   └── gateway_service.py   # Gateway logic
│   │   ├── db/
│   │   │   └── session.py           # Database setup
│   │   └── main.py                  # FastAPI app
│   ├── tests/
│   │   ├── test_auth.py
│   │   └── test_api_keys.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx          # Navigation
│   │   │   └── ProtectedRoute.tsx   # Route protection
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx      # Auth state management
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── ApiKeys.tsx
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── api.ts               # API client
│   │   ├── i18n/
│   │   │   └── locales/
│   │   │       └── ar.json          # Arabic translations
│   │   ├── App.tsx                  # Main app
│   │   └── main.tsx                 # Entry point
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations (if applicable)
# python app/main.py would create tables automatically

# Start server
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Start development server
npm run dev
```

Frontend runs on `http://localhost:3000`

### Using Docker

```bash
# Build and run both services
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/me` - Update profile

### API Keys
- `POST /api/keys` - Create API key
- `GET /api/keys` - List API keys
- `DELETE /api/keys/{key_id}` - Delete API key
- `GET /api/keys/{key_id}/usage` - Get usage stats

### Gateway
- `POST /api/gateway/chat` - Send chat request
- `POST /api/gateway/chat/stream` - Chat with streaming
- `GET /api/gateway/providers` - List available providers
- `POST /api/gateway/estimate` - Estimate cost

## Authentication Methods

### 1. JWT Token (for UI)
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/gateway/chat
```

### 2. API Key (for programmatic access)
```bash
curl -H "X-API-Key: sk_live_xxxxx" \
  http://localhost:8000/api/gateway/chat
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Configuration

### Backend (.env)
```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./salma_gateway.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CLAUDE_API_KEY=sk_live_xxx
OPENAI_API_KEY=sk_xxx
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## Available Providers

1. **Claude (Anthropic)** - Active
   - Claude 3.5 Sonnet
   - Claude Opus 4.1

2. **OpenAI** - Active
   - GPT-4 Turbo
   - GPT-4o

3. **Jais (G42)** - Coming Soon
   - Jais 30B Chat

## Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ API key hashing and masking
- ✅ Rate limiting on login attempts
- ✅ CORS protection
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection (React escaping)
- ✅ CSRF-safe design (token-based)

## Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Manual Deployment

**Backend (Production)**
```bash
cd backend
pip install -r requirements.txt
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

**Frontend (Production)**
```bash
cd frontend
npm install
npm run build
npm run preview
```

## Internationalization

All UI text is in Arabic (RTL layout). Translations are stored in:
- `frontend/src/i18n/locales/ar.json`

To add more languages, create a new JSON file and update the i18n config.

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Submit pull request

## Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

### Frontend won't compile
- Delete `node_modules` and reinstall: `npm install`
- Clear vite cache: `rm -rf .vite`
- Check Node.js version (18+)

### Database issues
- Delete `.db` files and restart server
- Run migrations if applicable

## License

Proprietary - Salma AI Strategic Pivot

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@salma-ai.local

---

**Last Updated**: January 2026
**Status**: Production Ready for Prompt 2

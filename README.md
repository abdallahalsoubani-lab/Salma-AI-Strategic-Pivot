# Salma AI Gateway - الدرع الموحد للذكاء الاصطناعي

**Unified AI Shield for Enterprise Intelligence**

Salma AI Gateway is a comprehensive, production-ready platform for managing, explaining, and auditing AI requests across multiple providers. It provides complete explainability (XAI) and compliance features with full Arabic/English support.

## 🎯 Project Overview

This is the **Complete Implementation** of all 6 prompts:

| Prompt | Component | Status |
|--------|-----------|--------|
| 1 | Project Foundation | ✅ |
| 2 | Authentication & Core Gateway | ✅ |
| 3 | AI Provider Connectors & Smart Router | ✅ |
| 4 | Data Source Connectors | ✅ |
| 5 | Admin Dashboard UI | ✅ |
| 6 | **XAI & Audit Layer** | ✅ |

## 📦 Architecture

### Backend Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with AsyncPG
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT + Passlib
- **API Documentation**: Auto-generated with OpenAPI

### Frontend Stack
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Icons**: Lucide React
- **Routing**: React Router v6

## 🏗️ Project Structure

```
Salma-AI-Strategic-Pivot/
├── app/
│   ├── core/
│   │   └── database.py              # Database configuration
│   ├── models/
│   │   ├── user.py                  # User model
│   │   └── audit.py                 # Audit, Trace, Explanation models
│   ├── services/
│   │   ├── audit_service.py         # Audit logging & tracing
│   │   └── analytics_service.py     # Usage analytics
│   ├── api/
│   │   ├── dependencies.py          # API dependencies
│   │   └── routes/
│   │       └── audit.py             # Audit API endpoints
│   └── main.py                      # FastAPI application
│
├── src/
│   ├── components/
│   │   └── xai/
│   │       ├── TraceViewer.tsx      # Request trace component
│   │       └── ExplanationCard.tsx  # XAI explanation component
│   ├── pages/
│   │   └── AuditLogs.tsx            # Audit logs page
│   ├── locales/
│   │   ├── ar.json                  # Arabic translations
│   │   └── en.json                  # English translations
│   ├── App.tsx                      # Main App component
│   ├── main.tsx                     # React entry point
│   └── index.css                    # Global styles
│
├── backend/
│   └── alembic/
│       └── versions/
│           └── 001_add_audit_tables.py  # Database migration
│
├── docker-compose.yml               # Docker services
├── requirements.txt                 # Python dependencies
├── package.json                     # Node dependencies
├── tsconfig.json                    # TypeScript config
├── vite.config.ts                   # Vite config
├── tailwind.config.js               # Tailwind config
└── .env.example                     # Environment template
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- PostgreSQL 16+

### Setup

1. **Clone and Setup Environment**
```bash
cd Salma-AI-Strategic-Pivot
cp .env.example .env
```

2. **Backend Setup**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
npm install
```

4. **Database Setup**
```bash
# Option 1: Using Docker Compose
docker-compose up postgres

# Option 2: Using existing PostgreSQL
# Update DATABASE_URL in .env
```

5. **Run Migrations**
```bash
alembic upgrade head
```

6. **Start Services**
```bash
# Terminal 1 - Backend
python -m app.main

# Terminal 2 - Frontend
npm run dev
```

### Docker Compose (All-in-One)
```bash
docker-compose up --build
```

**Access Points:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

## 📊 Prompt 6: XAI & Audit Layer

### Database Models

#### 1. **AuditLog**
Stores every significant action in the system:
- User/API Key tracking
- Event type and action
- Request/response summaries (sanitized)
- Error tracking
- Performance metrics (duration)

#### 2. **AIRequestTrace**
Detailed trace of each AI request for explainability:
- Input messages and tokens
- Routing decisions (which provider/model was selected)
- Output content and tokens
- Cost tracking (USD breakdown)
- Performance metrics (latency at each stage)
- Context sources used

#### 3. **AIExplanation**
Human-readable XAI data:
- Arabic & English explanations
- Routing factors (language, complexity, provider availability)
- Context relevance scores
- Response confidence and categories
- Potential issues detected
- PII detection and compliance flags

#### 4. **UsageMetrics**
Aggregated metrics for reporting:
- Hourly/daily/monthly aggregations
- Per-user or per-provider breakdown
- Token usage and costs
- Success/failure rates
- Latency percentiles (p95, p99)

### API Endpoints

#### Traces
- `GET /api/audit/traces` - List user's request traces
- `GET /api/audit/traces/{request_id}` - Get trace details
- `GET /api/audit/traces/{request_id}/explanation` - Get XAI explanation

#### Audit Logs
- `GET /api/audit/logs` - List audit logs
- `GET /api/audit/logs?event_type=user_login` - Filter by event

#### Analytics
- `GET /api/audit/analytics/summary?days=30` - Usage summary
- `GET /api/audit/analytics/by-provider?days=30` - By provider breakdown
- `GET /api/audit/analytics/trend?days=7&granularity=daily` - Usage trend
- `GET /api/audit/analytics/top-queries?days=7` - Most expensive queries

#### Reports
- `GET /api/audit/reports/compliance` - Compliance report
- `GET /api/audit/reports/export?format=json&days=30` - Export report

### Frontend Components

#### TraceViewer
Displays detailed AI request information:
- Request ID, status, provider, model
- Performance metrics (latency, cost, tokens)
- Expandable sections:
  - Input messages
  - Output content
  - Routing decision info

#### ExplanationCard
Shows XAI decision explanation:
- Arabic & English explanations
- Routing factors visualization
- Language, complexity, confidence indicators
- Potential issues and alerts
- PII detection status
- Compliance information

#### AuditLogs Page
Full-featured audit logs interface:
- Sortable table with real-time data
- Filter by status, provider, date range
- Search by Request ID
- Side panel detail view
- Export functionality

### Services

#### AuditService
```python
# Logging
await audit_service.log_event(
    event_type=AuditEventType.CHAT_REQUEST,
    action="create_chat",
    user_id=user_id,
    resource_type="chat",
    status=RequestStatus.SUCCESS
)

# Tracing
trace = await audit_service.create_trace(
    request_id="req_abc123",
    user_id=user_id,
    input_messages=[...],
    selected_provider="claude",
    selected_model="claude-3-sonnet"
)

# Complete trace
await audit_service.complete_trace(
    request_id="req_abc123",
    output_content="...",
    output_tokens=600,
    cost_usd=0.0023,
    total_latency_ms=1234
)

# Create explanation
await audit_service.create_explanation(
    trace_id=trace.id,
    routing_factors={
        "language_detected": "ar",
        "complexity_score": 0.5,
        "selected_provider": "claude"
    },
    explanation_ar="تم اختيار...",
    pii_detected=False
)
```

#### AnalyticsService
```python
# Get usage summary
summary = await analytics.get_usage_summary(
    user_id=user_id,
    start_date=datetime.utcnow() - timedelta(days=30)
)

# Get usage by provider
by_provider = await analytics.get_usage_by_provider(
    user_id=user_id
)

# Get trend
trend = await analytics.get_usage_trend(
    user_id=user_id,
    days=7,
    granularity="daily"
)

# Generate compliance report
report = await analytics.generate_compliance_report(
    user_id=user_id
)
```

## 🔒 Security Features

- **Data Sanitization**: Automatically redacts sensitive data (passwords, tokens, API keys)
- **PII Detection**: Identifies personally identifiable information in queries
- **Request Validation**: All inputs validated with Pydantic
- **JWT Authentication**: Secure token-based authentication
- **CORS Protection**: Configurable CORS settings
- **Audit Trail**: Complete audit trail of all actions
- **Compliance**: GDPR/Data Protection compliant

## 🌍 Internationalization (i18n)

Full Arabic (عربي) and English support:

### Arabic Features
- RTL (Right-to-Left) layout
- Full Arabic labels and translations
- Arabic explanations for AI decisions
- Support for Arabic language detection

### Available Translations
- Common UI elements
- XAI explanations and components
- Compliance and analytics terms
- Filter options and labels

## 📈 Usage Analytics

### Pre-built Reports
1. **Usage Summary**: Total requests, tokens, cost, latency
2. **Provider Breakdown**: Cost and usage per AI provider
3. **Usage Trends**: Hourly/daily trends over time
4. **Top Queries**: Most expensive or frequent queries
5. **Compliance Report**: PII incidents, blocked requests, recommendations

### Metrics Available
- Total/successful/failed request counts
- Input/output token consumption
- Cost in USD (per request and aggregated)
- Latency metrics (p95, p99, average)
- Provider-specific breakdowns
- Time-series data for trends

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_audit_service.py
```

## 📝 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## 🔧 Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/salma_db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# JWT
JWT_SECRET_KEY=your-secret-key-here-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI Providers
CLAUDE_API_KEY=...
OPENAI_API_KEY=...
JAIS_API_KEY=...

# Audit
AUDIT_RETENTION_DAYS=90
ENABLE_PII_DETECTION=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 📚 API Documentation

Once running, access interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

All endpoints are documented with:
- Request/response schemas
- Parameter descriptions
- Example requests
- Status codes and error responses

## 🎯 Key Features Implemented

### ✅ Prompt 6 Completion
- [x] Audit Database Models (4 tables)
- [x] Audit Service (logging, tracing, explanations)
- [x] Analytics Service (metrics, reports)
- [x] Audit API Routes (12+ endpoints)
- [x] Database Migration (production-ready)
- [x] Frontend Components (TraceViewer, ExplanationCard)
- [x] Audit Logs Page (full-featured)
- [x] Arabic Translations (100+ terms)
- [x] Docker Support
- [x] TypeScript Types
- [x] Documentation

## 🚀 Deployment

### Production Checklist
- [ ] Set strong `JWT_SECRET_KEY`
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Setup database backups
- [ ] Enable audit log archival
- [ ] Configure monitoring/alerting
- [ ] Setup log aggregation
- [ ] Enable request rate limiting
- [ ] Setup CI/CD pipeline
- [ ] Regular security audits

### Docker Production
```bash
# Build images
docker-compose build

# Run with production settings
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 📞 Support

For issues, questions, or contributions:
1. Check existing documentation
2. Review API docs at `/docs`
3. Check error messages in audit logs
4. Review compliance reports

## 📄 License

This project is proprietary and confidential.

---

**Made with ❤️ for Enterprise AI Governance**

مبروك! 🎊 المشروع جاهز للإنتاج!

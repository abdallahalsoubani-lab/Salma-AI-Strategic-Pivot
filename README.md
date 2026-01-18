# Salma AI Gateway - AI Connectors & Smart Router

## Overview

Salma AI Gateway is a unified interface for interacting with multiple AI providers. It includes intelligent routing that automatically selects the best provider based on:

- **Language Detection**: Arabic queries prefer Jais, English queries use Claude/OpenAI
- **Complexity Analysis**: Simple queries use faster/cheaper models, complex queries use more powerful models
- **Cost Optimization**: Optional cost-optimized routing
- **Provider Availability**: Falls back to available providers
- **Token Estimation**: Calculates costs per request

## Architecture

### Components

```
app/
├── connectors/ai/
│   ├── base.py          # Base class for all providers
│   ├── claude.py        # Anthropic Claude connector
│   ├── openai.py        # OpenAI GPT connector
│   ├── jais.py          # G42 Jais connector (Arabic-first)
│   └── router.py        # Smart router for provider selection
├── models/
│   ├── schemas.py       # Pydantic schemas for API
│   └── database.py      # SQLAlchemy database models
├── services/
│   └── gateway_service.py  # Main gateway service
├── core/
│   └── database.py      # Database configuration
└── config.py            # Application settings
```

## AI Providers

### 1. Claude (Anthropic)

**Models:**
- `claude-sonnet-4-20250514` (Balanced) - $3/$15 per 1M tokens
- `claude-haiku-3-5-20241022` (Fast) - $0.80/$4 per 1M tokens
- `claude-opus-4-20250514` (Powerful) - $15/$75 per 1M tokens

**Features:**
- Context window: 200K tokens
- Strong reasoning capabilities
- Arabic support

**Setup:**
```bash
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 2. OpenAI

**Models:**
- `gpt-4o` (Balanced) - $2.50/$10 per 1M tokens
- `gpt-4o-mini` (Fast) - $0.15/$0.60 per 1M tokens
- `gpt-4-turbo` (Powerful) - $10/$30 per 1M tokens

**Features:**
- Context window: 128K tokens
- Excellent general-purpose capabilities
- Fast inference

**Setup:**
```bash
OPENAI_API_KEY=sk-xxxxx
```

### 3. Jais (G42)

**Models:**
- `jais-30b-chat` (Arabic) - Free tier
- `jais-13b-chat` (Arabic Fast) - Free tier

**Features:**
- Arabic-first LLM
- Bilingual support (Arabic + English)
- Optimized for Arabic understanding
- Lower context window (8K tokens)

**Setup:**
```bash
JAIS_API_KEY=  # Optional
```

## Smart Router

The router intelligently selects providers based on:

### Language Detection
```
Arabic text (>30% Arabic chars) → Prefer Jais → Claude → OpenAI
English text → Claude → OpenAI
```

### Complexity Classification
```
Simple (< 500 chars)  → Fast tier models (Haiku, GPT-4o-mini, Jais-13B)
Medium (500-2000 chars) → Balanced tier (Sonnet, GPT-4o)
Complex (> 2000 chars or keywords) → Powerful tier (Opus, GPT-4-Turbo)
```

### Routing Strategies
- `auto` (default): Language + complexity-based routing
- `cost`: Cost-optimized (Jais → OpenAI → Claude)
- `quality`: Quality-first (Claude → OpenAI → Jais)

## Usage

### Basic Chat Request

```bash
curl -X POST http://localhost:8000/api/gateway/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "مرحبا، كيف حالك؟"}
    ]
  }'
```

### Response

```json
{
  "id": "req_a1b2c3d4e5f6",
  "response": "مرحباً! أنا بخير، شكراً للسؤال...",
  "provider": "jais",
  "model": "jais-30b-chat",
  "usage": {
    "input_tokens": 15,
    "output_tokens": 45,
    "cost": "0.0"
  },
  "latency_ms": 1250,
  "created_at": "2025-01-18T16:00:00Z"
}
```

### Complex English Query

```bash
curl -X POST http://localhost:8000/api/gateway/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Analyze the strategic implications of AI adoption in MENA banking sector"
      }
    ],
    "temperature": 0.8,
    "max_tokens": 2000
  }'
```

**Expected routing:** Claude Opus (for complex analysis)

### Specify Provider

```json
{
  "messages": [...],
  "provider": "claude",
  "model": "claude-sonnet-4-20250514"
}
```

## Configuration

Create `.env` file:

```env
# Application
APP_NAME=Salma AI Gateway
DEBUG=False
LOG_LEVEL=INFO

# AI Providers
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
JAIS_API_KEY=  # Optional
```

## Frontend Integration

### Provider Selector Component

```tsx
import { ProviderSelector } from '@/components/ProviderSelector';

<ProviderSelector
  selectedProvider="auto"
  onProviderChange={(id) => console.log(id)}
  providers={[
    { id: 'claude', name: 'Claude', nameAr: 'كلود', status: 'active' },
    { id: 'openai', name: 'OpenAI', nameAr: 'أوبن إيه آي', status: 'active' },
    { id: 'jais', name: 'Jais', nameAr: 'جيس', status: 'active', badge: 'الأفضل للعربية' }
  ]}
  isArabic={true}
/>
```

### Multilingual Support

- **Arabic (`ar.json`)**: Complete Arabic translations
- **English (`en.json`)**: Complete English translations
- **RTL Support**: Automatic RTL direction for Arabic UI

## Cost Calculation

Each response includes cost calculation:

```python
def calculate_cost(input_tokens, output_tokens, model):
    model_info = MODELS[model]
    input_cost = (input_tokens / 1_000_000) * model_info["input_price"]
    output_cost = (output_tokens / 1_000_000) * model_info["output_price"]
    return round(input_cost + output_cost, 6)
```

Example: 100 input + 200 output tokens with Claude Sonnet:
- Input: 100/1,000,000 × $3 = $0.0003
- Output: 200/1,000,000 × $15 = $0.003
- **Total: $0.0033**

## Get Provider Status

```bash
curl -X GET http://localhost:8000/api/gateway/providers \
  -H "Authorization: Bearer <token>"
```

Response:
```json
{
  "providers": [
    {
      "id": "claude",
      "name": "Claude (Anthropic)",
      "name_ar": "كلود (أنثروبيك)",
      "status": "active",
      "models": [...]
    },
    {
      "id": "openai",
      "name": "OpenAI",
      "name_ar": "أوبن إيه آي",
      "status": "active",
      "models": [...]
    },
    {
      "id": "jais",
      "name": "Jais (G42)",
      "name_ar": "جيس (جي42)",
      "status": "active",
      "models": [...]
    }
  ]
}
```

## Routing Examples

### Example 1: Simple Arabic Query
```
Input: "مرحبا"
Language: Arabic
Complexity: Simple
Route: Jais 13B Chat → Claude Haiku → OpenAI Mini
Cost: $0 (Jais)
```

### Example 2: Complex English Query
```
Input: "Provide detailed analysis of quantum computing applications in cryptography..."
Language: English
Complexity: Complex
Route: Claude Opus → GPT-4-Turbo
Cost: ~$0.05-0.08
```

### Example 3: Cost-Optimized Strategy
```
Strategy: "cost"
Route: Jais → OpenAI (mini) → Claude (haiku)
```

## Error Handling

### Missing API Key
```json
{
  "error": "Provider not configured",
  "provider": "openai",
  "message": "OPENAI_API_KEY not set in environment"
}
```

### Provider Fallback
If preferred provider fails:
1. Try next provider in routing order
2. Log attempt
3. Return response from working provider

## Token Estimation

Rough estimation for token counting:

```python
# Claude: ~3 chars per token
def estimate_tokens(text):
    return len(text) // 3

# OpenAI: ~4 chars per token
def estimate_tokens(text):
    return len(text) // 4

# Jais (Arabic): ~2 chars per token
def estimate_tokens(text):
    return len(text) // 2
```

## Testing

```bash
# Simple test
curl -X POST http://localhost:8000/api/gateway/chat \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "hello"}]}'

# Arabic test
curl -X POST http://localhost:8000/api/gateway/chat \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "أين أنت من؟"}]}'

# Explicit provider test
curl -X POST http://localhost:8000/api/gateway/chat \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "test"}],
    "provider": "claude",
    "model": "claude-sonnet-4-20250514"
  }'
```

## Next Steps

1. ✅ AI Provider connectors
2. ✅ Smart router
3. ✅ Cost calculation
4. ✅ Frontend components
5. 🔲 API endpoint implementation
6. 🔲 Authentication integration
7. 🔲 Database logging
8. 🔲 Monitoring & analytics

## Notes

- Jais connector uses OpenAI-compatible API format
- All async/await for performance
- Stream support for long responses
- Language detection uses regex for Arabic Unicode ranges
- Token estimation is approximate (use actual token counters for accuracy)

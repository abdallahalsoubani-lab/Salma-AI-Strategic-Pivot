# بوابة سلمى للذكاء الاصطناعي

**Salma AI Gateway** - منصة بوابة ذكية توصل الأنظمة المؤسسية في منطقة الشرق الأوسط وشمال أفريقيا بخدمات الذكاء الاصطناعي.

## 📋 نظرة عامة

بوابة سلمى هي حل شامل يوفر:

- ✨ واجهة عربية (RTL) سهلة الاستخدام
- 🔌 وصول موحد لمختلف مزودي خدمات الذكاء الاصطناعي
- 🔐 إدارة آمنة للمفاتيح والاتصالات
- 📊 مراقبة الاستخدام والتكاليف
- 🚀 أداء عالي وقابلية للتوسع
- 🌍 دعم قواعد البيانات المختلفة

## 🏗️ البنية المعمارية

```
salma-gateway/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes and endpoints
│   │   ├── core/        # Core utilities (security, database)
│   │   ├── models/      # Database models and schemas
│   │   ├── services/    # Business logic
│   │   └── connectors/  # External integrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── locales/     # Arabic translations
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🚀 البدء السريع

### المتطلبات

- Docker و Docker Compose
- أو تثبيت يدوي: Python 3.11+, Node.js 20+, PostgreSQL 15+, Redis 7+

### التثبيت والتشغيل مع Docker

#### 1. استنساخ المشروع

```bash
git clone <repository-url>
cd salma-gateway
```

#### 2. إعداد متغيرات البيئة

```bash
cp .env.example .env
```

تأكد من تعديل القيم الحساسة في الملف `.env`، خاصة:
- `SECRET_KEY` - استخدم مفتاح عشوائي قوي
- `ANTHROPIC_API_KEY` - أضف مفتاح Anthropic الخاص بك
- `OPENAI_API_KEY` - أضف مفتاح OpenAI الخاص بك

#### 3. تشغيل التطبيق

```bash
docker-compose up --build
```

سيتم تشغيل جميع الخدمات:
- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### التثبيت اليدوي

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # أو: venv\Scripts\activate على Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 📝 متغيرات البيئة

### إعدادات التطبيق

```env
APP_NAME=بوابة سلمى للذكاء الاصطناعي
APP_VERSION=0.1.0
DEBUG=false
```

### إعدادات قاعدة البيانات

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database
REDIS_URL=redis://host:6379/0
```

### الأمان

```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### مفاتيح الخدمات الخارجية

```env
ANTHROPIC_API_KEY=your-api-key
OPENAI_API_KEY=your-api-key
```

### CORS

```env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 🔌 نقاط نهاية API

### فحص الصحة

```bash
GET /api/health
```

الاستجابة:
```json
{
  "status": "healthy",
  "service": "salma-gateway",
  "version": "0.1.0",
  "database": "connected",
  "timestamp": "2026-01-18T10:30:00+00:00"
}
```

### المصادقة (قيد التطوير)

- `POST /api/auth/login` - تسجيل الدخول
- `POST /api/auth/register` - إنشاء حساب
- `POST /api/auth/logout` - تسجيل الخروج

### البوابة (قيد التطوير)

- `POST /api/gateway/query` - إرسال استعلام
- `GET /api/gateway/connections` - قائمة الاتصالات
- `POST /api/gateway/connections` - إنشاء اتصال

## 📊 قاعدة البيانات

### الجداول الرئيسية

#### Users (المستخدمون)
- معلومات المستخدم الأساسية
- الأدوار والصلاحيات
- حالة التنشيط

#### API Keys (مفاتيح API)
- إدارة المفاتيح
- تتبع آخر استخدام
- صلاحيات الانتهاء

#### Connections (الاتصالات)
- معلومات الاتصال بمصادر البيانات
- أنواع الدعم: Oracle, PostgreSQL, MySQL, REST API
- تكوين آمن مشفر

#### Request Logs (سجلات الطلبات)
- تتبع الطلبات
- استهلاك الرموز (Tokens)
- حساب التكاليف
- قياس الأداء (Latency)

## 🎨 واجهة المستخدم

### الميزات

- ✅ واجهة عربية كاملة (RTL)
- ✅ خط Cairo للنصوص العربية
- ✅ تصميم استجابي (Responsive)
- ✅ نمط Tailwind CSS
- ✅ تجربة مستخدم حديثة

### الصفحات

- لوحة التحكم - نظرة عامة على الاستخدام
- مصادر البيانات - إدارة الاتصالات
- الاستخدام - إحصائيات وتقارير
- الإعدادات - إدارة الحساب
- مفاتيح API - إدارة المفاتيح

## 🔐 الأمان

### أفضل الممارسات المطبقة

- 🔒 تشفير كلمات المرور بـ bcrypt
- 🔐 JWT للمصادقة
- 🛡️ حماية CORS
- 🔑 إدارة مفاتيح آمنة
- 📝 سجلات شاملة للطلبات
- ⚠️ معالجة آمنة للأخطاء

## 📈 الأداء والقابلية للتوسع

- استخدام AsyncIO في Python
- قاعدة بيانات PostgreSQL موثوقة
- Redis للتخزين المؤقت
- استعلامات محسنة مع الفهرسة
- دعم الحمل العالي

## 🧪 الاختبار

### تشغيل الاختبارات (قريباً)

```bash
cd backend
pytest

cd ../frontend
npm test
```

## 📚 التوثيق

### Swagger API Documentation

بعد تشغيل Backend، زر:
```
http://localhost:8000/docs
```

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. Fork المستودع
2. إنشاء فرع للميزة (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push للفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT.

## 👥 الفريق

يتم تطوير هذا المشروع كجزء من مشروع Salma AI Strategic Pivot.

## 📞 الدعم

للأسئلة والدعم، يرجى فتح Issue في المستودع.

## 🎯 خريطة الطريق

- [ ] تطبيق المصادقة الكاملة
- [ ] نماذج AI Provider
- [ ] واجهة عرض الاستعلامات
- [ ] نظام الفواتير
- [ ] لوحة معلومات متقدمة
- [ ] اختبارات شاملة
- [ ] توثيق مفصل

---

صُنع مع ❤️ لخدمة المؤسسات في MENA

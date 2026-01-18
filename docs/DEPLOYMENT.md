# دليل النشر - Deployment Guide

## نظرة عامة | Overview

هذا الدليل يشرح طرق نشر بوابة سلمى للذكاء الاصطناعي.

This guide explains how to deploy Salma AI Gateway.

---

## خيارات النشر | Deployment Options

### 1. Docker Compose (Recommended for small deployments)

```bash
# Clone repository
git clone https://github.com/your-org/salma-gateway.git
cd salma-gateway

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

### 2. Kubernetes (Recommended for production)

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (edit first!)
kubectl apply -f k8s/secrets.yaml

# Deploy all components
kubectl apply -f k8s/

# Check status
kubectl get pods -n salma-gateway
```

### 3. On-Premise (Air-Gapped)

```bash
# On internet-connected machine:
./scripts/create-airgap-package.sh

# Transfer to air-gapped system, then:
tar -xzf salma-gateway-airgap-1.0.0.tar.gz
cd salma-gateway-airgap-1.0.0
./install.sh
```

---

## متطلبات النظام | System Requirements

### Minimum (Development)
- CPU: 2 cores
- RAM: 4 GB
- Storage: 20 GB

### Recommended (Production)
- CPU: 8 cores
- RAM: 16 GB
- Storage: 100 GB SSD

### High Availability
- 3+ nodes
- Load balancer
- Shared storage (for uploads)

---

## الأمان | Security

### SSL/TLS
- Always use HTTPS in production
- Use valid certificates (not self-signed)

### Network
- Restrict database access to internal network
- Use firewall rules
- Enable rate limiting

### Secrets
- Use strong passwords (32+ characters)
- Rotate API keys regularly
- Use secret management (Vault, etc.)

---

## النسخ الاحتياطي | Backup

### Database
```bash
# Manual backup
docker-compose exec postgres pg_dump -U $DB_USER $DB_NAME > backup.sql

# Restore
cat backup.sql | docker-compose exec -T postgres psql -U $DB_USER $DB_NAME
```

### Uploads
```bash
tar -czf uploads_backup.tar.gz ./data/uploads
```

---

## المراقبة | Monitoring

### Prometheus Metrics
- http://localhost:9090

### Grafana Dashboard
- http://localhost:3001
- Default: admin/admin

### Health Endpoints
- `/api/health` - Basic health check
- `/api/health/detailed` - Component status
- `/api/status` - System statistics

---

## استكشاف الأخطاء | Troubleshooting

### Container won't start
```bash
docker-compose logs backend
```

### Database connection failed
```bash
docker-compose exec postgres pg_isready -U salma_user
```

### Out of memory
- Increase container memory limits
- Check for memory leaks

### Slow responses
- Check database indexes
- Review slow query logs
- Scale horizontally

---

## الدعم | Support

- Documentation: https://docs.salma.ai
- Email: support@salma.ai

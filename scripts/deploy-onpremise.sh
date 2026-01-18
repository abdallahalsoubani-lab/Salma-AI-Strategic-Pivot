#!/bin/bash
#
# سكريبت النشر المحلي
# On-Premise Deployment Script for KSA
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Salma AI Gateway - On-Premise Setup  ${NC}"
echo -e "${GREEN}========================================${NC}"

# Check requirements
check_requirements() {
    echo -e "\n${YELLOW}Checking requirements...${NC}"

    command -v docker >/dev/null 2>&1 || { echo -e "${RED}Docker is required but not installed.${NC}"; exit 1; }
    command -v docker-compose >/dev/null 2>&1 || { echo -e "${RED}Docker Compose is required but not installed.${NC}"; exit 1; }

    echo -e "${GREEN}✓ All requirements met${NC}"
}

# Create directories
create_directories() {
    echo -e "\n${YELLOW}Creating directories...${NC}"

    mkdir -p ./data/postgres
    mkdir -p ./data/redis
    mkdir -p ./data/uploads
    mkdir -p ./logs
    mkdir -p ./backups
    mkdir -p ./ssl

    chmod 700 ./data ./logs ./backups ./ssl

    echo -e "${GREEN}✓ Directories created${NC}"
}

# Generate secrets
generate_secrets() {
    echo -e "\n${YELLOW}Generating secrets...${NC}"

    if [ ! -f .env ]; then
        cp .env.example .env

        # Generate random secret key
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=${SECRET_KEY}/" .env

        # Generate random DB password
        DB_PASSWORD=$(openssl rand -base64 24 | tr -dc 'a-zA-Z0-9' | head -c 32)
        sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=${DB_PASSWORD}/" .env

        echo -e "${GREEN}✓ Secrets generated${NC}"
        echo -e "${YELLOW}⚠ Please edit .env file to add your API keys${NC}"
    else
        echo -e "${YELLOW}⚠ .env file already exists, skipping${NC}"
    fi
}

# Setup SSL certificates
setup_ssl() {
    echo -e "\n${YELLOW}Setting up SSL...${NC}"

    read -p "Do you have SSL certificates? (y/n): " has_ssl

    if [ "$has_ssl" = "y" ]; then
        echo "Please copy your certificates to ./ssl/"
        echo "  - ssl/cert.pem (certificate)"
        echo "  - ssl/key.pem (private key)"
    else
        echo "Generating self-signed certificate for testing..."

        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ./ssl/key.pem \
            -out ./ssl/cert.pem \
            -subj "/C=SA/ST=Riyadh/L=Riyadh/O=SalmaAI/CN=salma.local"

        echo -e "${YELLOW}⚠ Self-signed certificate created (for testing only)${NC}"
    fi

    chmod 600 ./ssl/*.pem
    echo -e "${GREEN}✓ SSL configured${NC}"
}

# Build images
build_images() {
    echo -e "\n${YELLOW}Building Docker images...${NC}"

    docker-compose -f docker-compose.prod.yml build

    echo -e "${GREEN}✓ Images built${NC}"
}

# Start services
start_services() {
    echo -e "\n${YELLOW}Starting services...${NC}"

    docker-compose -f docker-compose.prod.yml up -d

    echo "Waiting for services to be ready..."
    sleep 10

    # Check health
    if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
        echo -e "${GREEN}✓ Backend is healthy${NC}"
    else
        echo -e "${RED}✗ Backend health check failed${NC}"
    fi

    if curl -s http://localhost/health | grep -q "healthy"; then
        echo -e "${GREEN}✓ Frontend is healthy${NC}"
    else
        echo -e "${RED}✗ Frontend health check failed${NC}"
    fi
}

# Run migrations
run_migrations() {
    echo -e "\n${YELLOW}Running database migrations...${NC}"

    docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

    echo -e "${GREEN}✓ Migrations completed${NC}"
}

# Create admin user
create_admin() {
    echo -e "\n${YELLOW}Creating admin user...${NC}"

    read -p "Admin email: " admin_email
    read -s -p "Admin password: " admin_password
    echo

    docker-compose -f docker-compose.prod.yml exec backend python -c "
from app.services.user_service import create_admin_user
import asyncio
asyncio.run(create_admin_user('${admin_email}', '${admin_password}'))
print('Admin user created successfully')
"

    echo -e "${GREEN}✓ Admin user created${NC}"
}

# Backup script
setup_backup() {
    echo -e "\n${YELLOW}Setting up backup cron job...${NC}"

    cat > ./scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup PostgreSQL
docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U $DB_USER $DB_NAME > ${BACKUP_DIR}/db_${TIMESTAMP}.sql

# Backup uploads
tar -czf ${BACKUP_DIR}/uploads_${TIMESTAMP}.tar.gz ./data/uploads

# Keep only last 7 days
find ${BACKUP_DIR} -type f -mtime +7 -delete

echo "Backup completed: ${TIMESTAMP}"
EOF

    chmod +x ./scripts/backup.sh

    # Add to crontab (daily at 2 AM)
    (crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/scripts/backup.sh") | crontab -

    echo -e "${GREEN}✓ Backup configured (daily at 2 AM)${NC}"
}

# Main
main() {
    check_requirements
    create_directories
    generate_secrets
    setup_ssl
    build_images
    start_services
    run_migrations

    read -p "Create admin user now? (y/n): " create_admin_now
    if [ "$create_admin_now" = "y" ]; then
        create_admin
    fi

    read -p "Setup automatic backups? (y/n): " setup_backup_now
    if [ "$setup_backup_now" = "y" ]; then
        setup_backup
    fi

    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}   Deployment Complete!                  ${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e ""
    echo -e "Access the application:"
    echo -e "  - Frontend: https://localhost"
    echo -e "  - API: https://localhost/api"
    echo -e "  - Health: https://localhost/api/health"
    echo -e ""
    echo -e "Monitoring:"
    echo -e "  - Prometheus: http://localhost:9090"
    echo -e "  - Grafana: http://localhost:3001"
    echo -e ""
    echo -e "${YELLOW}⚠ Remember to:${NC}"
    echo -e "  1. Update .env with your API keys"
    echo -e "  2. Replace SSL certificates for production"
    echo -e "  3. Configure firewall rules"
    echo -e "  4. Setup reverse proxy if needed"
}

main "$@"

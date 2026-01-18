#!/bin/bash
#
# إنشاء حزمة التثبيت بدون إنترنت
# Create Air-Gapped Installation Package for KSA On-Premise
#

set -e

PACKAGE_NAME="salma-gateway-airgap"
VERSION=$(git describe --tags --always 2>/dev/null || echo "1.0.0")
OUTPUT_DIR="./dist/${PACKAGE_NAME}-${VERSION}"

echo "Creating air-gapped installation package..."

# Create output directory
mkdir -p ${OUTPUT_DIR}

# Save Docker images
echo "Saving Docker images..."
docker-compose -f docker-compose.prod.yml build

docker save \
    salma-gateway/backend:latest \
    salma-gateway/frontend:latest \
    pgvector/pgvector:pg16 \
    redis:7-alpine \
    prom/prometheus:latest \
    grafana/grafana:latest \
    | gzip > ${OUTPUT_DIR}/images.tar.gz

# Copy configuration files
echo "Copying configuration files..."
cp -r k8s ${OUTPUT_DIR}/
cp docker-compose.prod.yml ${OUTPUT_DIR}/
cp .env.example ${OUTPUT_DIR}/
cp -r monitoring ${OUTPUT_DIR}/
cp -r scripts ${OUTPUT_DIR}/

# Copy documentation
cp README.md ${OUTPUT_DIR}/
cp -r docs ${OUTPUT_DIR}/ 2>/dev/null || true

# Create installation script
cat > ${OUTPUT_DIR}/install.sh << 'EOF'
#!/bin/bash
echo "Loading Docker images..."
gunzip -c images.tar.gz | docker load

echo "Starting installation..."
./scripts/deploy-onpremise.sh

echo "Installation complete!"
EOF
chmod +x ${OUTPUT_DIR}/install.sh

# Create archive
echo "Creating archive..."
cd ./dist
tar -czf ${PACKAGE_NAME}-${VERSION}.tar.gz ${PACKAGE_NAME}-${VERSION}
cd ..

# Generate checksum
sha256sum ./dist/${PACKAGE_NAME}-${VERSION}.tar.gz > ./dist/${PACKAGE_NAME}-${VERSION}.sha256

echo ""
echo "Air-gapped package created:"
echo "  - ./dist/${PACKAGE_NAME}-${VERSION}.tar.gz"
echo "  - ./dist/${PACKAGE_NAME}-${VERSION}.sha256"
echo ""
echo "To install on air-gapped system:"
echo "  1. Copy the tar.gz file to the target system"
echo "  2. Extract: tar -xzf ${PACKAGE_NAME}-${VERSION}.tar.gz"
echo "  3. Run: cd ${PACKAGE_NAME}-${VERSION} && ./install.sh"

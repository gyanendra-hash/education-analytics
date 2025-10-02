# Education Analytics Data Warehouse - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Education Analytics Data Warehouse in various environments, from local development to production.

## Prerequisites

### System Requirements

#### Minimum Requirements
- **CPU**: 4 cores
- **RAM**: 8GB
- **Storage**: 100GB SSD
- **OS**: Linux (Ubuntu 20.04+), macOS (10.15+), or Windows 10+

#### Recommended Requirements
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Storage**: 500GB+ SSD
- **OS**: Linux (Ubuntu 22.04 LTS)

### Software Dependencies

#### Required Software
- **Python**: 3.9 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **Git**: 2.30 or higher
- **PostgreSQL**: 13 or higher
- **MongoDB**: 5.0 or higher
- **Redis**: 6.0 or higher

#### Optional Software
- **Kubernetes**: 1.20 or higher (for production)
- **Helm**: 3.0 or higher (for Kubernetes)
- **Nginx**: 1.18 or higher (for reverse proxy)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/education-analytics.git
cd education-analytics
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

**Required Environment Variables:**
```env
# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=education_analytics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# MongoDB Configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=education_analytics

# Application Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Education Analytics Data Warehouse

# CORS Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Logging
LOG_LEVEL=INFO
```

### 5. Start Database Services

```bash
# Start PostgreSQL and MongoDB using Docker Compose
docker-compose up -d postgres mongodb redis

# Wait for services to be ready
docker-compose logs -f postgres mongodb
```

### 6. Initialize Database

```bash
# Run database initialization script
python scripts/init_database.py

# Or run migrations manually
alembic upgrade head
```

### 7. Generate Sample Data

```bash
# Generate sample data
python data/sample_data.py

# Load sample data into database
python scripts/load_sample_data.py
```

### 8. Start the Application

```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start dashboard (in another terminal)
python -m app.dashboards.dashboard
```

### 9. Verify Installation

```bash
# Test API endpoints
curl http://localhost:8000/health

# Test dashboard
open http://localhost:8000/dashboard

# Test API documentation
open http://localhost:8000/docs
```

## Docker Deployment

### 1. Build Docker Images

```bash
# Build application image
docker build -t education-analytics:latest .

# Build with specific tag
docker build -t education-analytics:v1.0.0 .
```

### 2. Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Production Docker Compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: education_analytics
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    ports:
      - "5432:5432"
    restart: unless-stopped

  mongodb:
    image: mongo:5.0
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGODB_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    ports:
      - "27017:27017"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

  app:
    image: education-analytics:latest
    environment:
      - POSTGRES_HOST=postgres
      - MONGODB_HOST=mongodb
      - REDIS_HOST=redis
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - mongodb
      - redis
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  mongodb_data:
  redis_data:
```

## Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl create namespace education-analytics
```

### 2. Create ConfigMap

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: education-analytics-config
  namespace: education-analytics
data:
  POSTGRES_HOST: postgres-service
  MONGODB_HOST: mongodb-service
  REDIS_HOST: redis-service
  LOG_LEVEL: INFO
```

### 3. Create Secrets

```yaml
# secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: education-analytics-secrets
  namespace: education-analytics
type: Opaque
data:
  POSTGRES_PASSWORD: <base64-encoded-password>
  MONGODB_PASSWORD: <base64-encoded-password>
  SECRET_KEY: <base64-encoded-secret>
```

### 4. Deploy Database Services

```yaml
# postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: education-analytics
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: education_analytics
        - name: POSTGRES_USER
          value: postgres
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: education-analytics-secrets
              key: POSTGRES_PASSWORD
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: education-analytics
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
```

### 5. Deploy Application

```yaml
# app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: education-analytics-app
  namespace: education-analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: education-analytics-app
  template:
    metadata:
      labels:
        app: education-analytics-app
    spec:
      containers:
      - name: app
        image: education-analytics:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: education-analytics-config
        - secretRef:
            name: education-analytics-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: education-analytics-service
  namespace: education-analytics
spec:
  selector:
    app: education-analytics-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 6. Deploy with Helm

```bash
# Create Helm chart
helm create education-analytics

# Install with Helm
helm install education-analytics ./education-analytics \
  --namespace education-analytics \
  --set image.tag=latest \
  --set postgres.password=your-password \
  --set mongodb.password=your-password
```

## Production Deployment

### 1. Infrastructure Setup

#### AWS Deployment
```bash
# Create EKS cluster
eksctl create cluster --name education-analytics --region us-west-2

# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier education-analytics-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username postgres \
  --master-user-password your-password

# Create DocumentDB MongoDB cluster
aws docdb create-db-cluster \
  --db-cluster-identifier education-analytics-mongodb \
  --engine docdb \
  --master-username admin \
  --master-user-password your-password
```

#### Azure Deployment
```bash
# Create AKS cluster
az aks create \
  --resource-group education-analytics-rg \
  --name education-analytics-cluster \
  --node-count 3 \
  --enable-addons monitoring

# Create PostgreSQL database
az postgres flexible-server create \
  --resource-group education-analytics-rg \
  --name education-analytics-db \
  --admin-user postgres \
  --admin-password your-password
```

### 2. Security Configuration

#### SSL/TLS Setup
```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configure Nginx with SSL
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://education-analytics-service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Firewall Configuration
```bash
# Configure UFW (Ubuntu)
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable

# Configure iptables
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### 3. Monitoring Setup

#### Prometheus Configuration
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'education-analytics'
    static_configs:
      - targets: ['education-analytics-service:80']
    metrics_path: /metrics
    scrape_interval: 5s
```

#### Grafana Dashboard
```bash
# Install Grafana
helm install grafana stable/grafana \
  --namespace monitoring \
  --set adminPassword=admin \
  --set service.type=LoadBalancer
```

### 4. Backup Configuration

#### Database Backups
```bash
# PostgreSQL backup script
#!/bin/bash
pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB > backup_$(date +%Y%m%d_%H%M%S).sql

# MongoDB backup script
#!/bin/bash
mongodump --host $MONGODB_HOST --db $MONGODB_DB --out backup_$(date +%Y%m%d_%H%M%S)
```

#### Automated Backups
```yaml
# backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: education-analytics
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:13
            command:
            - /bin/bash
            - -c
            - |
              pg_dump -h postgres-service -U postgres education_analytics > /backup/backup_$(date +%Y%m%d_%H%M%S).sql
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

## Environment-Specific Configurations

### Development Environment
```env
# .env.development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://postgres:password@localhost:5432/education_analytics_dev
MONGODB_URL=mongodb://localhost:27017/education_analytics_dev
REDIS_URL=redis://localhost:6379/0
```

### Staging Environment
```env
# .env.staging
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://postgres:password@staging-db:5432/education_analytics_staging
MONGODB_URL=mongodb://staging-mongodb:27017/education_analytics_staging
REDIS_URL=redis://staging-redis:6379/0
```

### Production Environment
```env
# .env.production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://postgres:password@prod-db:5432/education_analytics_prod
MONGODB_URL=mongodb://prod-mongodb:27017/education_analytics_prod
REDIS_URL=redis://prod-redis:6379/0
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database connectivity
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1;"

# Check MongoDB connectivity
mongo $MONGODB_HOST/$MONGODB_DB --eval "db.stats()"
```

#### Application Startup Issues
```bash
# Check application logs
docker-compose logs app

# Check database migrations
alembic current
alembic history
```

#### Performance Issues
```bash
# Check database performance
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT * FROM pg_stat_activity;"

# Check Redis performance
redis-cli -h $REDIS_HOST info memory
```

### Health Checks

#### Application Health
```bash
# Check API health
curl http://localhost:8000/health

# Check database health
curl http://localhost:8000/api/v1/health/database

# Check MongoDB health
curl http://localhost:8000/api/v1/health/mongodb
```

#### System Health
```bash
# Check system resources
htop
df -h
free -h

# Check Docker containers
docker ps
docker stats
```

## Maintenance

### Regular Maintenance Tasks

#### Database Maintenance
```bash
# Update database statistics
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "ANALYZE;"

# Vacuum database
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "VACUUM ANALYZE;"

# Reindex database
psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c "REINDEX DATABASE education_analytics;"
```

#### Application Maintenance
```bash
# Update application
git pull origin main
docker-compose build
docker-compose up -d

# Clear caches
redis-cli -h $REDIS_HOST FLUSHALL
```

#### Backup Verification
```bash
# Verify backup integrity
pg_restore --list backup_file.sql

# Test restore
pg_restore --create --clean --if-exists -d postgres backup_file.sql
```

## Scaling

### Horizontal Scaling
```yaml
# Scale application replicas
kubectl scale deployment education-analytics-app --replicas=5

# Scale database read replicas
kubectl scale deployment postgres-read-replica --replicas=3
```

### Vertical Scaling
```yaml
# Increase resource limits
apiVersion: apps/v1
kind: Deployment
metadata:
  name: education-analytics-app
spec:
  template:
    spec:
      containers:
      - name: app
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

This deployment guide provides comprehensive instructions for deploying the Education Analytics Data Warehouse in various environments, from local development to production-scale deployments.

# FastAPI Docker Application - Complete CRUD with Monitoring & CI/CD

> A production-grade FastAPI application demonstrating full CRUD operations, comprehensive error handling, enterprise security, and complete monitoring with Prometheus & Grafana. Fully containerized with Docker Compose and CI/CD pipeline using Jenkins.

## Features

### Core Functionality
- **Full CRUD Operations**: Create, Read, Update, Delete users with auto-incrementing IDs
- **Input Validation**: Pydantic models with email uniqueness, age constraints (0-150), name validation
- **Error Handling**: Custom exceptions mapped to HTTP status codes (409, 404, 422, 429)
- **Health Checks**: Liveness, readiness, and status endpoints (Kubernetes-ready)
- **Rate Limiting**: DDoS protection (100-1000 req/min per endpoint)
- **CORS Security**: Cross-origin resource sharing configured

### Monitoring & Observability
- **Prometheus Metrics**: Automatic collection of application metrics
- **Grafana Dashboard**: Auto-provisioned monitoring visualization
- **Metrics Endpoint**: `/metrics` for Prometheus scraping
- **Request Tracing**: Built-in request instrumentation

### Infrastructure
- **Docker Compose**: 3-service orchestration (FastAPI, Prometheus, Grafana)
- **Named Volumes**: Data persistence across container restarts
- **Bridge Network**: Isolated monitoring network
- **Auto Provisioning**: Grafana datasources and dashboards auto-configured

### CI/CD Pipeline
- **Jenkins Pipeline**: 5-stage automation
  1. Checkout from GitHub
  2. Build Docker image with build number tagging
  3. Push to Docker Hub
  4. Deploy to remote server via SSH
  5. Health check verification
- **Environment Variables**: Easy configuration for different deployments

---

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- Git (for cloning)

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/RohitPatil18/docker-fastapi-test.git
cd docker-fastapi-test
\`\`\`

### 2. Start Services
\`\`\`bash
docker compose up -d --build
\`\`\`

### 3. Test API
\`\`\`bash
# Health check
curl http://localhost:8000/health | jq .

# Create a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","age":30}'

# Get all users
curl http://localhost:8000/users | jq .

# Access Swagger UI
open http://localhost:8000/docs
\`\`\`

### 4. Access Services
| Service | URL | Credentials |

| FastAPI | http://localhost:8000 | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin123 |

---

## Example Usage

### Create User
\`\`\`bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice@example.com",
    "age": 28
  }'

# Response: {"id":1,"first_name":"Alice",...}
\`\`\`

### Get All Users
\`\`\`bash
curl http://localhost:8000/users | jq .
# Response: {"data":[...],"count":1}
\`\`\`

### Update User
\`\`\`bash
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Alicia","last_name":"Smith","email":"alicia@example.com","age":29}'
\`\`\`

### Delete User
\`\`\`bash
curl -X DELETE http://localhost:8000/users/1
# Response: {"success":true,"message":"User 1 deleted successfully"}
\`\`\`

---

## API Endpoints

| Method | Endpoint | Status Codes |

| POST | /users | 201, 409, 422 |
| GET | /users | 200 |
| GET | /users/{id} | 200, 404 |
| PUT | /users/{id} | 200, 404, 409, 422 |
| DELETE | /users/{id} | 200, 404 |
| GET | /health | 200 |
| GET | /ready | 200, 503 |
| GET | /status | 200 |
| GET | /metrics | 200 |
| GET | /docs | 200 (Swagger UI) |

---

## Project Structure

\`\`\`
docker-fastapi-test/
├── Dockerfile                    # Python 3.11-slim
├── docker-compose.yml            # 3 services: fastapi, prometheus, grafana
├── Jenkinsfile                   # 5-stage CI/CD pipeline
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── app/
│   ├── main.py                   # FastAPI app + endpoints
│   ├── schema.py                 # Pydantic models
│   ├── services.py               # CRUD business logic
│   └── data/                     # Auto-created for JSON persistence
└── monitoring/
    ├── prometheus.yml            # Prometheus config
    └── grafana/
        └── provisioning/         # Auto-configuration
            ├── datasources/prometheus.yml
            └── dashboards/dashboards.yml
\`\`\`

---

## Data Persistence

Data persists across container restarts thanks to **named volumes**:

\`\`\`bash
# Data is preserved across restarts
docker compose down
docker compose up -d --build

# All users still there!
curl http://localhost:8000/users
\`\`\`

---

##  Security Features

- **Rate Limiting**: 100-1000 req/min per endpoint
- **Input Validation**: Pydantic models enforce data integrity
- **Email Uniqueness**: No duplicate emails allowed
- **CORS Enabled**: Cross-origin requests supported
- **Error Handling**: Consistent, descriptive error responses

---

##  Monitoring

### Prometheus (http://localhost:9090)
- Scrapes metrics every 10 seconds
- Auto-discovers FastAPI service
- Stores time-series data

### Grafana (http://localhost:3000)
- Default: admin / admin123
- Auto-provisioned Prometheus datasource
- Ready for custom dashboards

---

## Deployment with Jenkins

1. Create Jenkins credentials: `dockerhub-credentials`, `deploy-server-ssh`
2. Update `Jenkinsfile` environment variables
3. Pipeline automatically:
   - Builds Docker image
   - Pushes to Docker Hub
   - Deploys to remote server
   - Verifies health

---

## 

- **Production-Grade Architecture** with clean separation of concerns
- **Complete Error Handling** with custom exceptions and proper HTTP status codes
- **Enterprise Security** featuring rate limiting, CORS, and comprehensive validation
- **Kubernetes-Ready** with health and readiness probes
- **Full Monitoring Stack** with Prometheus and Grafana
- **Data Persistence** guaranteed across container lifecycle
- **CI/CD Ready** with complete Jenkins pipeline
- **Auto-Generated Documentation** via Swagger UI and ReDoc


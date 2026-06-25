# FastAPI E-commerce Backend — A to Z Project README & Interview Guide

> Project Status: Stable learning project. Current test result target: `44 passed`.
>
> Purpose: This README documents the complete FastAPI backend learning journey, project architecture, module-wise implementation, daily commands, Docker/Deployment workflow, troubleshooting, and interview questions a candidate may face.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [What We Built](#2-what-we-built)
3. [Technology Stack](#3-technology-stack)
4. [Learning Roadmap Covered](#4-learning-roadmap-covered)
5. [Project Architecture](#5-project-architecture)
6. [Folder Structure](#6-folder-structure)
7. [Environment Setup](#7-environment-setup)
8. [How to Run the Project](#8-how-to-run-the-project)
9. [Docker Workflow](#9-docker-workflow)
10. [PostgreSQL with Docker Compose](#10-postgresql-with-docker-compose)
11. [Alembic Migration Commands](#11-alembic-migration-commands)
12. [Testing Commands](#12-testing-commands)
13. [API Modules](#13-api-modules)
14. [Database Models and Relationships](#14-database-models-and-relationships)
15. [Authentication and JWT](#15-authentication-and-jwt)
16. [Background Tasks](#16-background-tasks)
17. [Configuration and Environment Variables](#17-configuration-and-environment-variables)
18. [CORS](#18-cors)
19. [Logging](#19-logging)
20. [Gunicorn and Uvicorn Workers](#20-gunicorn-and-uvicorn-workers)
21. [Nginx Reverse Proxy](#21-nginx-reverse-proxy)
22. [HTTPS / SSL Concept](#22-https--ssl-concept)
23. [Git Workflow](#23-git-workflow)
24. [Windows Setup After Git Clone](#24-windows-setup-after-git-clone)
25. [Common Troubleshooting](#25-common-troubleshooting)
26. [Interview Questions by Module](#26-interview-questions-by-module)
27. [Candidate Interview Answer Scripts](#27-candidate-interview-answer-scripts)
28. [What Is Still Missing Before Real Production](#28-what-is-still-missing-before-real-production)
29. [Next Roadmap: AI Engineering with FastAPI](#29-next-roadmap-ai-engineering-with-fastapi)
30. [Final Checklist](#30-final-checklist)

---

## 1. Project Overview

This project is a **Mini E-commerce Backend API** built with **FastAPI**. It was developed as a backend learning project to understand production-grade FastAPI development step by step.

The project covers:

- Python backend fundamentals
- FastAPI routing
- Pydantic request/response schemas
- CRUD API design
- SQLModel / SQLAlchemy database integration
- Alembic migrations
- PostgreSQL production-style connection
- JWT authentication
- Service-repository architecture
- Background tasks
- Testing with pytest
- Docker and Docker Compose
- Gunicorn with Uvicorn workers
- Nginx reverse proxy
- Environment variables
- Logging
- CORS
- HTTPS deployment concept

The goal is not only to build APIs, but to understand how a backend developer should structure, test, run, and prepare a FastAPI project for real deployment.

---

## 2. What We Built

We built the following modules:

| Module           |       Status | Description                                                                 |
| ---------------- | -----------: | --------------------------------------------------------------------------- |
| Health Check     |         Done | Basic app running check                                                     |
| Product          |         Done | Product CRUD with filtering, sorting, pagination                            |
| Customer         |         Done | Customer creation and listing with BD phone validation                      |
| Order            |         Done | Order creation, stock validation, transaction behavior                      |
| Payment          |         Done | COD/online payment method handling                                          |
| Voucher          |         Done | Voucher create and apply logic                                              |
| Auth             |         Done | Register, login, JWT token, `/auth/me`                                      |
| Background Tasks |         Done | Email log, notification queue log, report generation, AI parsing simulation |
| Testing          |         Done | API tests, service tests, database tests, auth tests, background task tests |
| Docker           |         Done | Dockerfile and docker-compose                                               |
| PostgreSQL       |         Done | PostgreSQL DB container with API container                                  |
| Gunicorn         |         Done | Production command using Uvicorn worker                                     |
| Nginx            |         Done | Reverse proxy concept and Docker Nginx container                            |
| HTTPS            | Concept Done | SSL handled by Nginx/Certbot on real server                                 |

---

## 3. Technology Stack

### Backend

- Python 3.9
- FastAPI
- Pydantic v2
- SQLModel
- SQLAlchemy
- Alembic
- python-jose
- passlib[bcrypt]
- pytest
- FastAPI TestClient

### Database

- SQLite for early/local learning
- PostgreSQL for production-style Docker environment

### Deployment / DevOps

- Docker
- Docker Compose
- Gunicorn
- Uvicorn Worker
- Nginx
- Environment variables
- Certbot / Let’s Encrypt concept

---

## 4. Learning Roadmap Covered

### Phase 0: Python Backend Foundation

Covered concepts:

- Python syntax
- Functions
- Type hints
- Optional values
- Class basics
- Exception handling
- Virtual environment
- pip package management

Example:

```python
def calculate_total(price: float, quantity: int) -> float:
    total = price * quantity
    return total
```

Why it matters:

FastAPI heavily uses Python type hints. Without type hints, request validation, documentation, and response modeling become weak.

---

### Phase 1: FastAPI Basic

Covered:

- `FastAPI()` app create
- GET API
- POST API
- Path parameter
- Query parameter
- Request body
- Response model
- Swagger docs

Run command:

```bash
python -m uvicorn app.main:app --reload
```

Swagger URL:

```text
http://127.0.0.1:8000/docs
```

---

### Phase 2: API Design Properly

Covered CRUD style:

```text
GET    /products
GET    /products/{product_id}
POST   /products
PUT    /products/{product_id}
PATCH  /products/{product_id}
DELETE /products/{product_id}
```

Business modules practiced:

- Product
- Customer
- Order
- Order Item
- Payment
- Voucher

---

### Phase 3: Pydantic Schema / DTO

Covered:

- Request schema
- Response schema
- Field validation
- Email validation
- Phone validation
- Error formatting

Example:

```python
from pydantic import BaseModel, Field

class ProductCreateRequest(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_qty: int = Field(..., ge=0)
```

Important concept:

```text
Request schema = frontend থেকে data নেওয়ার model
Response schema = frontend-এ data return করার model
```

---

### Phase 4: Database Integration

Covered:

- SQLModel
- SQLAlchemy engine/session
- Database dependency
- Alembic migration
- SQLite
- PostgreSQL
- Relationship
- Transaction concept

Recommended learning order:

```text
SQLite → PostgreSQL → MySQL
```

---

### Phase 5: Dependency Injection

Covered:

- `Depends`
- Database session dependency
- Auth dependency
- Current user dependency

Example:

```python
from fastapi import Depends

@app.get("/profile")
def get_profile(current_user=Depends(get_current_user)):
    return current_user
```

---

### Phase 6: Authentication & Authorization

Covered:

- Password hashing
- JWT access token
- Protected route
- `/auth/register`
- `/auth/login`
- `/auth/me`

---

### Phase 7: Service Layer Architecture

Covered production-style architecture:

```text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

Why:

- Router handles HTTP only
- Service handles business logic
- Repository handles DB query
- Model represents database table
- Schema represents request/response DTO

---

### Phase 8: Background Tasks

Covered:

- Email task simulation
- Notification queue simulation
- Report generation trigger
- PDF processing trigger
- AI parsing trigger simulation

FastAPI BackgroundTasks is useful for lightweight post-response tasks.

Example flow:

```text
Order create
   ↓
Response immediately return
   ↓
Background task writes email/notification log
```

---

### Phase 9: Testing

Covered:

- pytest
- TestClient
- API test
- Service test
- Auth test
- Database test
- Background task test
- Mocking background task

Current expected result:

```text
44 passed
```

---

### Phase 10: Deployment

Covered:

- Uvicorn
- Docker
- Docker Compose
- Environment variables
- PostgreSQL production-style connection
- Logging
- CORS
- Gunicorn
- Nginx reverse proxy
- HTTPS concept

Still remaining for real production:

- Actual Linux VPS deployment
- Real domain DNS setup
- Real Certbot SSL certificate
- Production monitoring
- CI/CD pipeline

---

## 5. Project Architecture

High-level flow:

```text
Client / Swagger / Frontend
        ↓
FastAPI Router
        ↓
Service Layer
        ↓
Repository Layer
        ↓
SQLModel / SQLAlchemy
        ↓
Database
```

Production deployment flow:

```text
Browser / Frontend
        ↓
Nginx reverse proxy
        ↓
Gunicorn master process
        ↓
Uvicorn workers
        ↓
FastAPI app
        ↓
PostgreSQL
```

---

## 6. Folder Structure

Recommended project structure:

```text
fastapi-ecommerce/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exception_handlers.py
│   │   ├── logger.py
│   │   └── security.py
│   ├── db/
│   │   └── session.py
│   ├── dependencies/
│   │   └── auth_dependency.py
│   ├── models/
│   │   ├── product_model.py
│   │   ├── customer_model.py
│   │   ├── order_model.py
│   │   ├── payment_model.py
│   │   ├── voucher_model.py
│   │   └── user_model.py
│   ├── schemas/
│   │   ├── common_schema.py
│   │   ├── product_schema.py
│   │   ├── customer_schema.py
│   │   ├── order_schema.py
│   │   ├── payment_schema.py
│   │   ├── voucher_schema.py
│   │   ├── background_schema.py
│   │   └── auth_schema.py
│   ├── repositories/
│   │   ├── product_repository.py
│   │   ├── customer_repository.py
│   │   ├── order_repository.py
│   │   ├── payment_repository.py
│   │   ├── voucher_repository.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── product_service.py
│   │   ├── customer_service.py
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   ├── voucher_service.py
│   │   └── auth_service.py
│   ├── tasks/
│   │   ├── order_tasks.py
│   │   ├── email_tasks.py
│   │   ├── notification_tasks.py
│   │   ├── report_tasks.py
│   │   ├── pdf_tasks.py
│   │   └── ai_tasks.py
│   └── api/
│       └── v1/
│           ├── product_routes.py
│           ├── customer_routes.py
│           ├── order_routes.py
│           ├── payment_routes.py
│           ├── voucher_routes.py
│           ├── background_routes.py
│           └── auth_routes.py
├── migrations/
├── tests/
├── nginx/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
├── requirements.txt
├── alembic.ini
├── .env.example
├── .env.production.example
└── README.md
```

---

## 7. Environment Setup

### Create virtual environment

macOS/Linux:

```bash
python3.9 -m venv venv
source venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.9 -m venv venv
.\venv\Scripts\activate
```

### Install packages

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Freeze packages

```bash
python -m pip freeze > requirements.txt
```

---

## 8. How to Run the Project

### Local development without Docker

```bash
source venv/bin/activate
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

### Local test command

```bash
python -m pytest -v
```

---

## 9. Docker Workflow

### Build and run development stack

```bash
docker compose up -d --build
```

### See logs

```bash
docker compose logs -f api
```

### Run migration inside Docker

```bash
docker compose exec api python -m alembic upgrade head
```

### Run tests inside Docker

```bash
docker compose exec api python -m pytest -v
```

### Stop containers

```bash
docker compose down
```

### Rebuild cleanly

```bash
docker compose down
docker compose up -d --build
```

---

## 10. PostgreSQL with Docker Compose

Development compose can run API + PostgreSQL:

```text
FastAPI API container → PostgreSQL DB container
```

Important rule:

Inside Docker Compose, API should connect to DB using service name:

```text
postgresql://postgres:postgres@db:5432/fastapi_ecommerce
```

Not:

```text
postgresql://postgres:postgres@localhost:5432/fastapi_ecommerce
```

Because `localhost` inside API container means the API container itself, not the DB container.

### Check DB containers

```bash
docker compose ps
```

### Enter PostgreSQL shell

```bash
docker compose exec db psql -U postgres -d fastapi_ecommerce
```

Inside psql:

```sql
\dt
SELECT * FROM alembic_version;
\q
```

### Run psql command directly

```bash
docker compose exec db psql -U postgres -d fastapi_ecommerce -c "\dt"
```

```bash
docker compose exec db psql -U postgres -d fastapi_ecommerce -c "SELECT * FROM alembic_version;"
```

---

## 11. Alembic Migration Commands

### Create migration

```bash
python -m alembic revision --autogenerate -m "create product table"
```

### Apply migration

```bash
python -m alembic upgrade head
```

### Check current migration

```bash
python -m alembic current
```

### Check history

```bash
python -m alembic history
```

### Docker migration commands

```bash
docker compose exec api python -m alembic current
```

```bash
docker compose exec api python -m alembic upgrade head
```

### Important Alembic notes

If migration file uses:

```python
sqlmodel.sql.sqltypes.AutoString()
```

Then add:

```python
import sqlmodel
```

SQLite cannot easily add a NOT NULL column to an existing table without default. Use `server_default` or create proper migration.

---

## 12. Testing Commands

### Run all tests

```bash
python -m pytest -v
```

Docker:

```bash
docker compose exec api python -m pytest -v
```

Production compose:

```bash
docker compose -f docker-compose.prod.yml exec api python -m pytest -v
```

### Run specific test file

```bash
python -m pytest tests/test_auth_api.py -v
```

Docker:

```bash
docker compose exec api python -m pytest tests/test_auth_api.py -v
```

### Expected final result

```text
44 passed
```

---

## 13. API Modules

## 13.1 Health Check

Endpoint:

```text
GET /
```

Response:

```json
{
  "message": "FastAPI is running"
}
```

Purpose:

- Verify app is running
- Useful for Docker/Nginx/server health check

---

## 13.2 Product Module

Endpoints:

```text
POST   /products
GET    /products
GET    /products/{product_id}
PUT    /products/{product_id}
PATCH  /products/{product_id}
DELETE /products/{product_id}
```

Features:

- Product create
- Product update
- Product partial update
- Product delete
- Product list
- Product details
- Search
- Min/max price filter
- Pagination
- Sorting

Sort options:

```text
default
high_to_low
low_to_high
newly_added
```

Important validation:

- Product name min/max length
- Price greater than 0
- Stock quantity greater than or equal 0

Candidate should understand:

- Difference between PUT and PATCH
- Why response model is used
- Why validation belongs in schema
- Why business logic should be in service

---

## 13.3 Customer Module

Endpoints:

```text
POST /customers
GET  /customers
GET  /customers/{customer_id}
```

Features:

- Customer create
- Customer list
- Customer detail
- Bangladeshi phone number validation
- Email validation

Phone validation regex:

```python
BD_PHONE_REGEX = r"^01[3-9]\d{8}$"
```

Example valid phone:

```text
01700000000
```

Candidate should understand:

- Why phone validation is in schema
- Why EmailStr is used
- Difference between required and optional field

---

## 13.4 Order Module

Endpoints:

```text
POST /orders
GET  /orders
GET  /orders/{order_id}
```

Features:

- Create order
- Validate customer
- Validate product exists
- Validate stock quantity
- Reduce product stock after order
- Store order items
- Transaction rollback if error happens
- Order list filtering

Order statuses:

```text
PLACED
PROCESSING
SHIPPED
DELIVERED
CANCELLED
```

Order create response:

```json
{
  "message": "Order placed successfully",
  "order_no": "ORD-..."
}
```

Candidate should understand:

- Why order creation must be transactional
- Why stock reduction and order insert should happen together
- Why background task should not block order response

---

## 13.5 Payment Module

Payment methods:

```text
COD
BKASH
NAGAD
CARD
```

Features:

- COD payment creates pending payment
- Online payment requires transaction number
- Online payment can mark payment as paid
- Duplicate transaction number should be blocked
- Duplicate paid payment should be blocked

Candidate should understand:

- Payment status lifecycle
- Why transaction number must be unique
- Why real payment gateway integration needs callback/webhook verification

---

## 13.6 Voucher Module

Endpoints:

```text
POST /vouchers
GET  /vouchers
POST /vouchers/apply
```

Discount types:

```text
FLAT
PERCENTAGE
```

Features:

- Create voucher
- Duplicate voucher code blocked
- Apply voucher to order
- Validate active date range
- Validate min order amount
- Validate usage limit
- Max discount cap

Candidate should understand:

- Difference between flat and percentage discount
- Why max discount cap is needed
- Why voucher usage limit is required
- Why order amount should be recalculated on backend, not trusted from frontend

---

## 13.7 Auth Module

Endpoints:

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

Features:

- Register user
- Hash password
- Login with email/password
- Generate JWT token
- Decode JWT token
- Protected current-user endpoint

Important files:

```text
app/core/security.py
app/dependencies/auth_dependency.py
app/services/auth_service.py
app/repositories/user_repository.py
```

Candidate should understand:

- Never store plain password
- JWT contains subject/user id
- Token must expire
- Protected routes use dependency injection

---

## 13.8 Background Tasks Module

Endpoints:

```text
POST /background/email/send
POST /background/notifications/enqueue
POST /background/reports/sales-summary
POST /background/pdf/process
POST /background/ai/parse-text
```

Tasks:

- Email sending simulation
- Notification queue simulation
- CSV report generation
- PDF processing
- AI parsing simulation

Candidate should understand:

- BackgroundTasks run after response
- Good for lightweight tasks
- Heavy tasks should use Celery/Redis/RabbitMQ/Kafka later

---

## 14. Database Models and Relationships

Main tables:

```text
users
products
customers
orders
order_items
payments
vouchers
alembic_version
```

Important relationships:

```text
Customer → Orders
Order → OrderItems
Product → OrderItems
Order → Payment
Order → Voucher apply
```

Important database concepts learned:

- Primary key
- Foreign key
- Relationship
- Transaction
- Migration
- Database session
- Rollback
- Commit
- Refresh

---

## 15. Authentication and JWT

### Password Hashing

Function:

```python
def hash_password(password: str) -> str:
    return password_context.hash(password)
```

### Password Verification

```python
def verify_password(plain_password: str, password_hash: str) -> bool:
    return password_context.verify(plain_password, password_hash)
```

### Create Token

```python
def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
```

### Decode Token

```python
def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
```

---

## 16. Background Tasks

FastAPI BackgroundTasks example:

```python
from fastapi import BackgroundTasks

@router.post("/orders")
def create_order(request: OrderCreateRequest, background_tasks: BackgroundTasks):
    order = order_service.create_order(request)
    background_tasks.add_task(send_order_confirmation_notification, order.order_no)
    return {"message": "Order placed successfully", "order_no": order.order_no}
```

Use cases:

- Send email after order
- Notify admin
- Generate report
- Process uploaded file
- Trigger AI parsing

Do not use BackgroundTasks for:

- Long-running heavy processing
- Payment settlement
- Critical guaranteed jobs
- High-volume queue processing

Use later:

```text
Celery
Redis Queue
RabbitMQ
Kafka
```

---

## 17. Configuration and Environment Variables

Important config values:

```env
APP_NAME=FastAPI Ecommerce
APP_ENV=local
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///./ecommerce.db
SECRET_KEY=CHANGE_THIS_SECRET_KEY_FOR_PRODUCTION
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Production example:

```env
APP_NAME=FastAPI Ecommerce
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://postgres:STRONG_PASSWORD@db:5432/fastapi_ecommerce
SECRET_KEY=VERY_STRONG_RANDOM_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://admin.your-frontend-domain.com
```

Do not commit real `.env`.

Commit:

```text
.env.example
.env.production.example
```

Do not commit:

```text
.env
.env.production
```

---

## 18. CORS

CORS allows frontend domains to call backend from browser.

Example:

```text
Frontend: http://localhost:3000
Backend:  http://127.0.0.1:8000
```

FastAPI setup:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Important:

CORS is not authentication. CORS allows browser request. JWT decides user authorization.

---

## 19. Logging

Logging is used to debug production issues.

Safe logs:

```text
HTTP method
Path
Status code
Response time
Error stack trace
Order no
User id
Request id
```

Never log:

```text
Password
JWT token full value
OTP
Secret key
Card number
Full sensitive request body
```

Docker-friendly logging should go to stdout/stderr so this works:

```bash
docker compose logs -f api
```

---

## 20. Gunicorn and Uvicorn Workers

Development command:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Production command:

```bash
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

Concept:

```text
Gunicorn = process manager
UvicornWorker = ASGI worker that runs FastAPI
```

Flow:

```text
Gunicorn master
 ├── Uvicorn worker 1
 ├── Uvicorn worker 2
 └── Uvicorn worker N
```

Do not use `--reload` in production.

---

## 21. Nginx Reverse Proxy

Nginx sits in front of FastAPI.

Flow:

```text
Browser
  ↓
Nginx
  ↓
Gunicorn + Uvicorn workers
  ↓
FastAPI
  ↓
PostgreSQL
```

Local Nginx URL:

```text
http://127.0.0.1:8080/docs
```

Important Nginx config:

```nginx
location / {
    proxy_pass http://api:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Docker service name:

```text
api
```

So Nginx can proxy to:

```text
http://api:8000
```

---

## 22. HTTPS / SSL Concept

HTTPS should be handled by Nginx, not FastAPI.

Production flow:

```text
Browser HTTPS request
        ↓
Nginx SSL termination
        ↓
FastAPI internal HTTP
```

Real VPS steps:

```bash
sudo apt update
sudo apt install nginx certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.yourdomain.com
sudo nginx -t
sudo systemctl reload nginx
```

Requirements for real HTTPS:

```text
Linux VPS / Cloud VM
Real domain/subdomain
DNS A record to server IP
Port 80 open
Port 443 open
Nginx running
Certbot installed
```

---

## 23. Git Workflow

### Check changes

```bash
git status
```

### Add important files

```bash
git add app tests migrations nginx Dockerfile docker-compose.yml docker-compose.prod.yml requirements.txt alembic.ini .env.example .env.production.example README.md
```

### Commit

```bash
git commit -m "Complete FastAPI ecommerce backend learning project"
```

### Push

```bash
git push
```

### Do not commit

```text
venv/
__pycache__/
.pytest_cache/
.env
.env.production
logs/
uploads/
generated_reports/
*.db
```

---

## 24. Windows Setup After Git Clone

Install:

```text
Git
Docker Desktop
VS Code
Python 3.9 if running without Docker
```

Clone:

```powershell
git clone YOUR_GIT_REPOSITORY_URL
cd fastapi-ecommerce
```

Run with Docker:

```powershell
docker compose up -d --build
docker compose exec api python -m alembic upgrade head
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Run tests:

```powershell
docker compose exec api python -m pytest -v
```

Run without Docker:

```powershell
py -3.9 -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m alembic upgrade head
python -m uvicorn app.main:app --reload
```

---

## 25. Common Troubleshooting

### Docker command not found

Problem:

```text
zsh: command not found: docker
```

Fix:

Install and start Docker Desktop.

---

### No compose file

Problem:

```text
no configuration file provided
```

Fix:

Make sure `docker-compose.yml` exists in project root.

---

### Empty compose file

Problem:

```text
empty compose file
```

Fix:

Check:

```bash
cat docker-compose.prod.yml
```

Recreate file if blank.

---

### YAML parse error

Cause:

You pasted terminal command into YAML file:

```yaml
cat > docker-compose.yml <<'EOF'
```

Fix:

YAML file must contain only YAML content.

---

### Alembic cannot import DATABASE_URL

Problem:

```text
ImportError: cannot import name 'DATABASE_URL'
```

Fix:

Use:

```python
from app.core.config import settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
```

---

### Docker heredoc stdin error

Problem:

```text
cannot attach stdin to a TTY-enabled container because stdin is not a terminal
```

Fix:

Use `-T`:

```bash
docker compose exec -T api python - <<'PY'
print("hello")
PY
```

---

### Auth test keyword mismatch

Problem:

```text
verify_password() got an unexpected keyword argument 'password_hash'
```

Fix:

Function signature and call must match:

```python
def verify_password(plain_password: str, password_hash: str) -> bool:
    return password_context.verify(plain_password, password_hash)
```

Or call positionally:

```python
verify_password(request.password, user.password_hash)
```

---

### create_access_token subject mismatch

Problem:

```text
create_access_token() got an unexpected keyword argument 'subject'
```

Fix:

```python
def create_access_token(subject: str) -> str:
    ...
```

---

### PostgreSQL psql command issue

Inside psql, run commands separately:

```sql
\dt
SELECT * FROM alembic_version;
\q
```

Do not paste all as `\dt SELECT ...`.

---

## 26. Interview Questions by Module

## 26.1 Python Backend Foundation

1. What are Python type hints?
2. Why does FastAPI depend heavily on type hints?
3. Difference between `Optional[str]` and `str`?
4. What is a virtual environment?
5. Why do we use `requirements.txt`?
6. What is exception handling?
7. Difference between list, dict, and tuple?
8. What is async/await?
9. Why should secrets not be hardcoded?
10. Why should backend code use clear function return types?

---

## 26.2 FastAPI Basic

1. What is FastAPI?
2. What is ASGI?
3. Difference between FastAPI and Flask?
4. What is Swagger/OpenAPI?
5. What is path parameter?
6. What is query parameter?
7. What is request body?
8. Why use response models?
9. What happens when request validation fails?
10. How does FastAPI generate API docs automatically?

---

## 26.3 Pydantic / Schema

1. What is Pydantic?
2. Difference between request schema and response schema?
3. What is `Field(..., gt=0)`?
4. Why should validation be in schema?
5. What is `EmailStr`?
6. How do custom validators work?
7. What is DTO?
8. Why should DB model and API schema be separate?
9. What is `from_attributes=True`?
10. How do you hide sensitive fields in API response?

---

## 26.4 CRUD API

1. What is CRUD?
2. Difference between PUT and PATCH?
3. Which status code should be returned after create?
4. How do you handle not found errors?
5. How do you implement pagination?
6. How do you implement sorting?
7. How do you implement filtering?
8. Why should delete return only a message?
9. Should frontend send product price for order total calculation?
10. Why should backend recalculate business totals?

---

## 26.5 Database / SQLModel / SQLAlchemy

1. What is SQLAlchemy?
2. What is SQLModel?
3. Difference between model and schema?
4. What is a database session?
5. What is transaction?
6. What is rollback?
7. What is primary key?
8. What is foreign key?
9. What is relationship?
10. What is N+1 query problem?
11. Why use indexes?
12. Difference between SQLite and PostgreSQL?
13. Why is PostgreSQL better for production?
14. Why should Alembic migrations be used?
15. What is `alembic_version` table?

---

## 26.6 Alembic Migration

1. What is Alembic?
2. Why do we need migration?
3. Difference between `revision` and `upgrade head`?
4. What is autogenerate?
5. Why should all models be imported in `migrations/env.py`?
6. How does Alembic know metadata?
7. What happens if migration fails halfway?
8. How do you check current migration?
9. How do you check migration history?
10. What migration issues can happen in SQLite?

---

## 26.7 Dependency Injection

1. What is dependency injection in FastAPI?
2. What is `Depends`?
3. How do you inject DB session?
4. How do you inject current user?
5. Why dependency injection helps testing?
6. How do you override dependencies in tests?
7. Why is dependency system important for auth?
8. What is reusable validation dependency?
9. What is role permission dependency?
10. How is DI different from manually creating objects?

---

## 26.8 Authentication / JWT

1. How does JWT authentication work?
2. What is password hashing?
3. Why should password not be encrypted but hashed?
4. What is bcrypt?
5. What is JWT subject claim?
6. What is token expiry?
7. Where should JWT secret be stored?
8. What happens when JWT is invalid?
9. Difference between authentication and authorization?
10. How do you protect a route?
11. What is refresh token?
12. Why should token not be logged?
13. What is role-based authorization?
14. What is permission-based authorization?
15. How would you implement admin-only route?

---

## 26.9 Service Repository Architecture

1. Why not write all logic inside router?
2. What is router responsibility?
3. What is service responsibility?
4. What is repository responsibility?
5. Why separate schema/model/service/repository?
6. How does architecture improve testing?
7. How does architecture improve maintainability?
8. Where should transaction logic stay?
9. Where should business validation stay?
10. Where should database query stay?

---

## 26.10 Background Tasks

1. What is FastAPI BackgroundTasks?
2. When should you use BackgroundTasks?
3. When should you not use BackgroundTasks?
4. Difference between BackgroundTasks and Celery?
5. What happens if background task fails?
6. Why email after order should be background task?
7. Why payment processing should not be simple BackgroundTasks?
8. What is queue?
9. What is RabbitMQ/Redis Queue/Celery?
10. How do you test background task behavior?

---

## 26.11 Testing

1. What is pytest?
2. What is FastAPI TestClient?
3. What is unit test?
4. What is integration test?
5. How do you test database logic?
6. Why use in-memory SQLite in tests?
7. What is dependency override?
8. What is mocking?
9. Why should auth API be tested?
10. Why should voucher apply logic be tested?
11. What does `44 passed` mean?
12. How do you run one test file?
13. How do you debug failing tests?
14. Why should tests run in Docker too?
15. What should be included in CI later?

---

## 26.12 Docker

1. What is Docker?
2. What is Docker image?
3. What is Docker container?
4. What is Dockerfile?
5. What is `.dockerignore`?
6. What is Docker Compose?
7. Difference between `docker compose up` and `up -d`?
8. Why use volume mount in development?
9. Why should production not use reload?
10. How does container networking work?
11. Why use service name `db` instead of localhost?
12. How do you see container logs?
13. How do you run commands inside container?
14. What is Docker volume?
15. What happens when you run `docker compose down -v`?

---

## 26.13 PostgreSQL Production Connection

1. Why PostgreSQL for production?
2. How does API container connect to DB container?
3. What is `DATABASE_URL`?
4. Why store DB URL in env variable?
5. What is `pg_isready`?
6. Why use healthcheck?
7. What is persistent volume?
8. How do you inspect PostgreSQL tables?
9. How do you run Alembic migration against PostgreSQL?
10. What issue occurs if port 5432 is already used?

---

## 26.14 Environment Variables

1. What is `.env`?
2. Why should `.env` not be committed?
3. What is `.env.example`?
4. What is difference between local and production env?
5. Why should secret key be environment variable?
6. How does Docker Compose load env file?
7. How does FastAPI read environment config?
8. What is debug mode?
9. Why should debug be false in production?
10. How would you add AI API key later?

---

## 26.15 CORS

1. What is CORS?
2. Why browser blocks cross-origin request?
3. How do you configure CORS in FastAPI?
4. What is allowed origin?
5. Is CORS authentication?
6. Why avoid wildcard in production?
7. How does CORS differ between browser and mobile app?
8. What happens if frontend origin is missing?
9. Why CORS origins should be environment-based?
10. How do you test CORS with curl?

---

## 26.16 Logging

1. Why logging is important?
2. What should be logged?
3. What should not be logged?
4. Why logs should go to stdout in Docker?
5. Difference between DEBUG, INFO, WARNING, ERROR?
6. How do you view Docker logs?
7. What is request logging middleware?
8. Why log response time?
9. Why should JWT token not be logged?
10. How would you add request id later?

---

## 26.17 Gunicorn / Uvicorn

1. What is Uvicorn?
2. What is Gunicorn?
3. Why use Gunicorn with UvicornWorker?
4. Why not use `--reload` in production?
5. What is worker process?
6. How many workers should be used?
7. What is timeout?
8. What happens if worker crashes?
9. Difference between development and production command?
10. Why FastAPI needs ASGI server?

---

## 26.18 Nginx

1. What is Nginx?
2. What is reverse proxy?
3. Why put Nginx in front of FastAPI?
4. What is `proxy_pass`?
5. Why set `X-Forwarded-For` header?
6. Why Nginx exposes public port but API stays internal?
7. How do you see Nginx logs?
8. How do you configure body size?
9. How do you configure timeout?
10. How does Nginx help with HTTPS?

---

## 26.19 HTTPS

1. What is HTTPS?
2. Where should SSL be handled?
3. Why FastAPI should not directly handle SSL in production?
4. What is SSL termination?
5. What is Certbot?
6. What is Let’s Encrypt?
7. What ports are required for HTTPS?
8. Why local 127.0.0.1 does not use real Let's Encrypt certificate?
9. What is DNS A record?
10. How do you renew SSL certificate?

---

## 27. Candidate Interview Answer Scripts

### FastAPI Project Summary Answer

> I built a mini e-commerce backend using FastAPI. The project includes product, customer, order, payment, voucher, authentication, and background task modules. I used Pydantic schemas for request and response validation, SQLModel with Alembic for database modeling and migration, JWT for authentication, and a service-repository architecture for clean separation of concerns. I also wrote pytest tests for APIs, services, auth, database behavior, and background tasks. Finally, I containerized the app using Docker and Docker Compose, connected it with PostgreSQL, and prepared production deployment using Gunicorn, Uvicorn workers, Nginx reverse proxy, environment variables, logging, CORS, and HTTPS concept.

### Architecture Answer

> The project follows Router → Service → Repository → Database architecture. Routers only handle HTTP request and response. Services contain business logic like stock validation, voucher validation, order processing, and authentication. Repositories handle database queries. This structure keeps the code maintainable, testable, and close to production standards.

### Docker Answer

> Docker allows the FastAPI app to run in a consistent environment independent of the developer machine. I created a Dockerfile for the API and Docker Compose to run API and PostgreSQL services together. The API connects to PostgreSQL using the Compose service name `db`, not localhost. This makes the setup easier to run on Mac, Windows, Linux, or production server.

### Testing Answer

> I used pytest and FastAPI TestClient to test the backend. The tests cover API behavior, validation errors, auth login, protected route access, order stock reduction, voucher application, service logic, and background tasks. I also used dependency overrides to inject a test database session. The current test suite has 44 passing tests.

### Deployment Answer

> For production deployment, I use Gunicorn as the process manager with Uvicorn workers to run FastAPI. Nginx works as a reverse proxy in front of the app and handles public HTTP/HTTPS traffic. Environment-specific values like database URL, secret key, CORS origins, and debug mode are loaded from environment variables. HTTPS is handled by Nginx with Certbot and Let’s Encrypt on a real Linux server.

---

## 28. What Is Still Missing Before Real Production

This project is strong for learning and interview preparation. But before real production, add:

```text
Real Linux VPS deployment
Real domain and DNS setup
Real HTTPS with Certbot
Production-grade secret management
Request ID middleware
Rate limiting
Refresh token
Role/permission authorization
CI/CD pipeline
Monitoring
Database backup strategy
Error tracking
Queue system for heavy tasks
```

---

## 29. Next Roadmap: AI Engineering with FastAPI

After this backend foundation, the next roadmap is AI Engineering.

### AI Phase 1: LLM API Wrapper

Build endpoints:

```text
POST /ai/generate-product-description
POST /ai/summarize-order-report
POST /ai/customer-support-reply
```

Learn:

```text
AI provider config
API key from env
Prompt template
AI request schema
AI response schema
Error handling
Logging without exposing API key
```

### AI Phase 2: PDF Parser API

Build:

```text
POST /documents/upload
POST /documents/parse-purchase-order
POST /documents/extract-tech-pack
```

Learn:

```text
File upload
PDF text extraction
Background processing
AI-based parsing
Structured JSON response
```

### AI Phase 3: RAG System

Learn:

```text
Embeddings
Vector database
Document chunking
Similarity search
RAG response generation
```

Build:

```text
Company document chatbot
ERP policy assistant
Product knowledge assistant
Customer support knowledge bot
```

### AI Phase 4: Business AI

Build:

```text
AI Sales Report Assistant
AI Voucher Fraud Detector
AI Product Recommendation API
AI Inventory Demand Forecasting
AI Customer Segmentation API
```

---

## 30. Final Checklist

Before pushing final code:

```bash
python -m pytest -v
```

Docker test:

```bash
docker compose exec api python -m pytest -v
```

Production compose test:

```bash
docker compose -f docker-compose.prod.yml exec api python -m pytest -v
```

Expected:

```text
44 passed
```

Git:

```bash
git status
git add app tests migrations nginx Dockerfile docker-compose.yml docker-compose.prod.yml requirements.txt alembic.ini .env.example .env.production.example README.md
git commit -m "Complete FastAPI ecommerce backend learning project"
git push
```

---

## Final Note

This project gives a complete foundation for becoming a backend developer with FastAPI. The most important learning is not only API creation, but also production-style thinking:

```text
Clean architecture
Validation
Database migration
Authentication
Testing
Dockerization
Environment separation
Production server process
Reverse proxy
Security awareness
Interview readiness
```

From here, the correct next step is to start the AI Engineering roadmap using the same clean architecture and testing discipline.

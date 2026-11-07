# 🚀 Premium Backend API (FastAPI + PostgreSQL)

[![Python](https://img.shields.io/badge/Python-3.11.9-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)](https://www.sqlalchemy.org/)
[![Pytest Coverage](https://img.shields.io/badge/Test_Coverage-99%25-brightgreen.svg)](https://docs.pytest.org/)
[![Code Style](https://img.shields.io/badge/Code_Style-Clean_Architecture-black.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 📖 Overview
This repository contains a production-grade RESTful API built with **FastAPI** and **Python 3.11.9**. Designed following **Clean Layered Architecture** principles, it provides a secure, scalable, and fully tested backend solution. Key features include JWT-based authentication, fine-grained Role-Based Access Control (RBAC), relational database models using SQLAlchemy 2.0, automated migrations with Alembic, and comprehensive integration test coverage using Pytest.

---

## 🛠️ Tech Stack & Dependencies

* **Framework:** FastAPI (Asynchronous Python Web Framework)
* **ASGI Server:** Uvicorn (High-performance ASGI server)
* **Database & ORM:** PostgreSQL 15 + SQLAlchemy 2.0 (Relational Mapping)
* **Migrations:** Alembic (Database schema version control)
* **Data Validation:** Pydantic v2 & Pydantic-Settings (Runtime type validation & configuration)
* **Security & Auth:** OAuth2 with Password Hashing (Bcrypt) & JSON Web Tokens (JWT via PyJWT/python-jose)
* **Testing:** PyTest + HTTPX + Pytest-Cov (Integration testing & coverage reporting)
* **Containerization:** Docker & Docker Desktop

---

## 📂 Project Architecture

The application adheres to a strict separation of concerns through a Clean Layered Architecture:

```text
backend-premium-api-2/
├── .github/
│   └── workflows/
│       └── pytest.yml # CI/CD Automation: Automated testing on push/PR
├── app/
│   ├── api/          # Transport layer: API endpoints, routing & dependency injection
│   │   ├── v1/       # API Version 1 endpoints (auth, users, items)
│   │   └── deps.py   # Global reusable dependencies (get_db, get_current_user)
│   ├── core/         # Core infrastructure: configuration, security & DB sessions
│   ├── models/       # Data layer: SQLAlchemy ORM relational models
│   ├── schemas/      # Domain layer: Pydantic schemas for request/response validation
│   └── tests/        # Quality assurance: Integration test suite (test_users, test_items)
├── alembic/          # Database revision scripts & migration metadata
├── Documentación/    # Project documentation and historical logs
├── .env              # Environment variables (Private config)
├── .env.example      # Environment variables template
├── .gitignore        # Version control exclusions
├── requirements.txt  # Production dependency manifest
└── README.md         # Project documentation
```

---

## ⚙️ Quick Start / Local Setup

### 1. Prerequisites
Ensure you have the following installed on your machine:
* **Python 3.11.9**
* **Docker Desktop** (For running local PostgreSQL instances)
* **Git**

---

### 2. Repository Cloning & Environment Setup

```bash
# Clone the repository
git clone <your-repository-url>
cd backend-premium-api-2

# Create and activate a Python 3.11 virtual environment
py -3.11 -m venv .venv

# Windows PowerShell activation:
.venv\Scripts\activate

# Linux/macOS activation:
source .venv/bin/activate
```

---

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Database Setup (Docker)

Spin up a PostgreSQL 15 container locally:

```bash
docker run --name postgres-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=backend_db \
  -p 5432:5432 \
  -d postgres:15
```

---

### 5. Environment Variables Configuration

Create a `.env` file in the root directory based on the `.env.example` template:

```env
PROJECT_NAME="Premium Backend API"
API_V1_STR="/api/v1"
SECRET_KEY="your-super-secret-key-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES=60
SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/backend_db"
```

---

### 6. Run Database Migrations

Apply database schema migrations using Alembic:

```bash
alembic upgrade head
```

---

### 7. Run Local Development Server

Start the application server using Uvicorn with hot-reload enabled:

```bash
uvicorn app.main:app --reload
```

The server will start running locally at: `http://127.0.0.1:8000`

---

## 📖 API Documentation & Swagger UI

FastAPI automatically generates interactive visual documentation. Once the server is running, explore and test the API directly from your browser:

* **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Alternative ReDoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Key Endpoints Overview:
* `POST /api/v1/auth/login/access-token` - OAuth2 compatible token login.
* `POST /api/v1/users/` - Public user registration.
* `GET /api/v1/users/me` - Fetch authenticated user profile.
* `GET /api/v1/items/` - List user owned items (or all items if superuser).
* `POST /api/v1/items/` - Create a new item linked to the authenticated user.

---

## 🧪 Testing & Code Coverage

The project includes an isolated testing pipeline powered by **Pytest** and an in-memory SQLite database (`StaticPool`) to ensure fast, repeatable execution without side effects on production data.

Run the test suite with line-by-line coverage analysis:

```bash
pytest --cov=app --cov-report=term-missing
```

### Coverage Results Highlights:
```text
======================== 16 passed in 9.46s ========================
TOTAL COVERAGE: 99%
- Core, Auth, Schemas & Routers: 100% Coverage
- Complete integration test suite covering Happy Paths, Bad Credentials, Duplicate Emails, Inactive Users, and fine-grained RBAC Superuser Permissions across users and items.
```
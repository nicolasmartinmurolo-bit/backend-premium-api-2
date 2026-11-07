# Premium Backend API

## 🚀 Overview
This repository contains the version 1 stable core of a production-grade RESTful API built with **FastAPI** and **Python 3.11.9**. It follows a Clean Layered Architecture to ensure separation of concerns, robust security, and maintainability.

## 🛠️ Prerequisites & Tech Stack
Ensure you have the following installed locally before setting up the project:
* **Python 3.11.9** (Runtime environment)
* **Docker Desktop** (For running the PostgreSQL container)
* **Git** (Version control)

## ⚙️ Quick Start / Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd backend-premium-api-2
Create and activate the virtual environment (Python 3.11.9):

Bash
py -3.11 -m venv .venv
# Windows PowerShell execution policy fix (if required):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\activate
Set up PostgreSQL via Docker:

Bash
docker run --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=backend_db -p 5432:5432 -d postgres:15
Install dependencies:

Python
python -m pip install --upgrade pip
pip install -r requirements.txt
Configure environment variables:
Create a .env file in the root directory based on the provided configuration template.

📂 Project Architecture
The project is structured following a Clean Layered Architecture:

Plaintext
backend-premium-api-2/
├── app/
│   ├── api/          # Transport layer & API routers
│   ├── core/         # Core configurations, database session, & security
│   ├── models/       # SQLAlchemy ORM database models
│   ├── schemas/      # Pydantic data validation schemas
│   └── tests/        # Automated integration tests
├── .env              # Environment variables (private)
├── requirements.txt  # Dependencies manifest
└── README.md         # Project documentation
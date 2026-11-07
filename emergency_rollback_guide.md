# 🚨 Emergency Rollback Routine (Restoring to v1.0.0-stable)

If a refactor or experimental feature breaks the project and you need to safely revert the entire system (Codebase + Database schema) back to the stable baseline (`v1.0.0-stable`), follow this strict step-by-step recovery procedure.

---

## 🛠️ Step 1: Stop and Reset Local Infrastructure Containers
Ensure no background database connections or active transactions block schema modifications.

```bash
# Stop the running database container
docker stop postgres-db-v2

# Remove the container to clear modified database states
docker rm postgres-db-v2
```

---

## 🧹 Step 2: Revert Codebase State via Git
Reset working directory changes and align your working branch strictly to the stable release tag.

```bash
# Discard all uncommitted local modifications (Use with caution)
git reset --hard

# Checkout the clean stable tag
git checkout v1.0.0-stable
```

---

## 🐳 Step 3: Re-instantiate Fresh PostgreSQL Container
Spin up a clean PostgreSQL instance with your defined environment configuration parameters.

```bash
docker run --name postgres-db-v2 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=backend_db_v2 \
  -p 5433:5432 \
  -d postgres:15
```

---

## 🐍 Step 4: Validate Virtual Environment & Dependencies
Ensure your Python runtime environment matches the exact requirement manifest.

```bash
# Activate your local virtual environment
.venv\Scripts\activate

# Update core packaging tools and verify installed dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🗄️ Step 5: Synchronize Database Schema via Alembic Migrations
Align the newly instantiated database container schema with the code models of `v1.0.0-stable`.

```bash
# Execute Alembic migrations to apply initial table structures
alembic upgrade head
```

---

## 🧪 Step 6: Execute Health Checks & Test Suite
Run full test coverage to confirm system stability and verify complete recovery.

```bash
# Run pytest with code coverage output
pytest --cov=app --cov-report=term-missing
```

*Expected Result:* **100% pass rate** on initial tests (`11 passed`) with 94% baseline coverage.
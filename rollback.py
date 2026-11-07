import subprocess
import sys
import os

def run_command(command, description, ignore_error=False):
    """Auxiliary function to execute shell commands with status reporting."""
    print(f"\n==================================================================")
    print(f"🚀 [STEP] {description}")
    print(f"🔧 [CMD]  {command}")
    print(f"==================================================================")
    
    result = subprocess.run(command, shell=True)
    if result.returncode != 0 and not ignore_error:
        print(f"\n❌ [ERROR] Failed during step: {description}")
        print("⚠️ Rollback process aborted to prevent inconsistent state.")
        sys.exit(1)
    elif result.returncode != 0 and ignore_error:
        print(f"\n⚠️ [WARNING] Non-zero exit code ignored for step: {description}")
    else:
        print(f"✅ [SUCCESS] {description} completed successfully.")

def main():
    print("==================================================================")
    print("🚨 EMERGENCY ROLLBACK EXECUTION SCRIPT (Restoring to v1.0.0-stable)")
    print("==================================================================")
    
    # Step 1: Stop and Remove Docker Container
    run_command("docker stop postgres-db-v2", "Stopping PostgreSQL Container", ignore_error=True)
    run_command("docker rm postgres-db-v2", "Removing PostgreSQL Container", ignore_error=True)

    # Step 2: Revert Git Repository State
    run_command("git reset --hard", "Hard Reset of Local Git Working Directory")
    run_command("git checkout v1.0.0-stable", "Checking out Git Tag v1.0.0-stable")

    # Step 3: Spin Up Fresh PostgreSQL Container
    docker_run_cmd = (
        "docker run --name postgres-db-v2 "
        "-e POSTGRES_USER=postgres "
        "-e POSTGRES_PASSWORD=postgres "
        "-e POSTGRES_DB=backend_db_v2 "
        "-p 5433:5432 -d postgres:15"
    )
    run_command(docker_run_cmd, "Spinning up new PostgreSQL Docker Container")

    # Step 4: Verify/Upgrade Pip Dependencies
    run_command("python -m pip install --upgrade pip", "Upgrading Pip Package Manager")
    run_command("pip install -r requirements.txt", "Installing Dependencies from requirements.txt")

    # Step 5: Run Alembic Database Migrations
    run_command("alembic upgrade head", "Applying Alembic Migrations to Head")

    # Step 6: Execute PyTest Suite to Validate System Health
    run_command("pytest --cov=app --cov-report=term-missing", "Running Automated PyTest Suite")

    print("\n==================================================================")
    print("🎉 [COMPLETED] Emergency Rollback Executed Successfully!")
    print("Your project and database have been fully restored to v1.0.0-stable.")
    print("==================================================================")

if __name__ == "__main__":
    main()
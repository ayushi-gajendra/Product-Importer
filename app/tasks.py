from celery import Celery
from redis import Redis
from sqlalchemy import create_engine, text
import os, csv, json

# Celery setup
celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
)

# Redis client
redis = Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

# DB engine for Celery worker
engine = create_engine(
    os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/products"
    )
)

def set_status(job_id, percent, message):
    """Store progress in Redis for polling."""
    key = f"job:{job_id}:status"
    redis.set(key, json.dumps({"percent": percent, "message": message}))

@celery.task(name="tasks.import_csv")
def import_csv(job_id, file_path):
    set_status(job_id, 0, "Starting import...")

    if not os.path.exists(file_path):
        set_status(job_id, 100, "File not found!")
        return

    total_rows = sum(1 for _ in open(file_path)) - 1
    if total_rows <= 0:
        set_status(job_id, 100, "Empty file")
        return

    conn = engine.connect()

    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        processed = 0

        for row in reader:
            conn.execute(text("""
                INSERT INTO products (sku, name, description, active)
                VALUES (:sku, :name, :description, TRUE)
                ON CONFLICT (lower(sku))
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description;
            """), {
                "sku": row.get("sku"),
                "name": row.get("name"),
                "description": row.get("description")
            })

            processed += 1
            pct = int(processed / total_rows * 100)
            set_status(job_id, pct, f"Processed {processed}/{total_rows}")

    conn.close()
    set_status(job_id, 100, "Import complete!")
    return "done"

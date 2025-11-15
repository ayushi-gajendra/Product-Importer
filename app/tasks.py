from celery import Celery
from redis import Redis
from sqlalchemy import create_engine, text
import os, csv, json

# Celery app
celery = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# Redis pubsub for SSE
redis = Redis(host="redis", port=6379, db=0)

# SQL connection for worker
engine = create_engine(
    os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/postgres"
    )
)

def publish(job_id, percent, message):
    """Send progress updates to Redis Pub/Sub."""
    redis.publish(
        f"job:{job_id}",
        json.dumps({"percent": percent, "message": message})
    )

@celery.task(name="tasks.import_csv")
def import_csv(job_id, file_path):
    """Background CSV import task."""
    publish(job_id, 0, "Starting import...")

    # Count total lines for progress
    total_rows = sum(1 for _ in open(file_path)) - 1
    if total_rows <= 0:
        publish(job_id, 100, "Empty file")
        return

    conn = engine.connect()

    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        processed = 0

        for row in reader:
            conn.execute(text("""
                INSERT INTO products (sku, name, price, active)
                VALUES (:sku, :name, :price, TRUE)
                ON CONFLICT (lower(sku))
                DO UPDATE
                SET name = EXCLUDED.name,
                    price = EXCLUDED.price;
            """), {
                "sku": row.get("sku"),
                "name": row.get("name"),
                "price": row.get("price")
            })

            processed += 1
            if processed % 500 == 0:
                pct = int(processed / total_rows * 100)
                publish(job_id, pct, f"Processing {processed} of {total_rows}...")

    conn.close()
    publish(job_id, 100, "Import complete!")
    return "done"

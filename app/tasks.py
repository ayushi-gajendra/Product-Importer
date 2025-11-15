import os, csv, json
from celery import Celery
from redis import Redis
from sqlalchemy import create_engine, text

# Celery
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/products")

celery = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

redis = Redis.from_url(REDIS_URL)
engine = create_engine(DB_URL)


def set_status(job_id, percent, message):
    redis.set(f"job:{job_id}:status", json.dumps({
        "percent": percent,
        "message": message
    }))


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
            """), dict(
                sku=row.get("sku"),
                name=row.get("name"),
                description=row.get("description"),
            ))

            processed += 1
            set_status(job_id, int(processed / total_rows * 100),
                       f"Processed {processed}/{total_rows}")

    conn.close()
    set_status(job_id, 100, "Import complete!")
    return "done"

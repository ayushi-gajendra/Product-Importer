# Dockerfile
FROM python:3.10-slim

# system deps for psycopg2 and other niceties
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure tmp dir exists for uploads
RUN mkdir -p /shared_tmp

# Run Celery in background and Flask in foreground
CMD ["sh", "-c", "celery -A app.tasks worker --loglevel=info & flask run --host=0.0.0.0 --port=8000"]

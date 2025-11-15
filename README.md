# Product Importer

A scalable CSV-based product import system built with Flask, Celery, PostgreSQL, and Render deployment.
Designed to handle up to 500,000 products with real-time upload progress, product management UI, webhook management, and bulk operations.

---

## Features

### CSV Product Import

* Upload large CSV files (up to 500,000 rows) using a simple web interface
* Background processing using Celery to avoid timeouts
* Case-insensitive SKU uniqueness with automatic overwrite on duplicates
* Real-time import progress with percentage and status messages
* Optimized for long-running, large-scale imports

### Product Management Interface

* List all products with pagination
* Filter by SKU, name, description, or active status
* Create new products
* Inline edit existing products
* Delete products individually
* Clean, minimal HTML + JavaScript UI

### Bulk Product Operations

* Delete all products at once
* Confirmation dialog before destructive actions
* UI immediately refreshes on success

### Webhook Configuration

* Add, edit, enable, disable, and delete webhook endpoints
* Choose event type for each webhook
* Trigger test webhook requests from the UI
* View last response status and response latency (ms)

### Backend and Architecture

* Flask REST API using Blueprint modular structure
* SQLAlchemy ORM with PostgreSQL
* Celery worker for long-running background tasks
* Redis/Key-Value store for progress tracking and Celery communication
* Dockerized for local development
* Deployable on Render (Web Service + Worker + Postgres + Key-Value)

---

## Tech Stack

Backend: Flask
Worker: Celery
Broker: Redis / Render Key-Value (Redis-compatible)
Database: PostgreSQL
ORM: SQLAlchemy
Deployment: Render (Web Service + Worker + PostgreSQL + Key-Value)
Frontend: Vanilla HTML + JS

---

## Project Structure

```
app/
  main.py
  tasks.py
  db.py
  models.py
  routes/
    products.py
    webhooks.py
static/
  upload.html
  products.html
  webhooks.html
render.yaml
Dockerfile
docker-compose.yml
requirements.txt
README.md
```

---

## Local Development

Start everything:

```
docker-compose up --build
```

This starts:

* Flask API
* Celery worker
* PostgreSQL
* Redis

Local URLs:

* Upload: [http://localhost:8000](http://localhost:8000)
* Products: [http://localhost:8000/static/products.html](http://localhost:8000/static/products.html)
* Webhooks: [http://localhost:8000/static/webhooks.html](http://localhost:8000/static/webhooks.html)

---

## Deployment on Render

### 1. Push code to GitHub

(e.g., ayushi-gajendra/Product-Importer)

### 2. Deploy using `render.yaml`

Open Render → New Blueprint → Select repo.

The blueprint deploys:

* Web service
* Worker
* PostgreSQL

### 3. Create Key-Value Store manually

Render → New → Key-Value Store
Name: `product-importer-kv`
Plan: Free

Copy the **Internal Redis Connection String**.

### 4. Add env var to both services

In:

* product-importer-api
* product-importer-worker

Add:

```
REDIS_URL=<paste-the-keyvalue-url-here>
```

### 5. Redeploy

Your app is now fully deployed.

---

## CSV Format

```
sku,name,description
A101,Product A,First product
A102,Product B,Second product
```

---

## API Endpoints

### Products

```
GET    /api/products
POST   /api/products
PUT    /api/products/<id>
DELETE /api/products/<id>
DELETE /api/products          (bulk delete)
```

### Webhooks

```
GET    /api/webhooks
POST   /api/webhooks
PUT    /api/webhooks/<id>
DELETE /api/webhooks/<id>
POST   /api/webhooks/<id>/test
```

### CSV Import

```
POST   /upload
GET    /status/<job_id>
```

---

## Case-Insensitive SKU Constraint

```
Index("ux_products_sku_lower", func.lower(Product.sku), unique=True)
```

Ensures SKU uniqueness across A123, a123, A123.

---

## Notes for Reviewers

* CSV import pipeline tested for large datasets
* Celery used to avoid Render’s 30-second timeout limit
* Fully functional product & webhook UI
* Minimal but complete front-end
* Modular, clean, documented backend
* All assignment stories implemented

---

## Author

Ayushi Gajendra



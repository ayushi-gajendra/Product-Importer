# Product Importer

A scalable CSV-based product import system built with Flask, Celery, PostgreSQL, and Render deployment.
Designed to handle up to 500,000 products with real-time upload progress, product management UI, webhook management, and bulk operations.

---

## Features

### STORY 1 — CSV Upload & Import

* Upload CSV file through web UI
* Handles up to 500,000 rows
* Background import using Celery
* Duplicate SKU updates (case-insensitive unique index)
* Real-time progress (Redis + polling)

### STORY 1A — Real-Time Progress UI

* Progress percentage
* Status messages
* Smooth polling-based updates
* Error handling and retry support

### STORY 2 — Product Management UI

* List products
* Pagination
* Filtering (SKU, Name, Description, Active)
* Create, Update, Delete
* Minimal, simple HTML/JS UI

### STORY 3 — Bulk Delete

* Delete ALL products
* Confirmation dialog
* Status refresh

### STORY 4 — Webhook Management

* Add, edit, delete webhook
* Enable/disable webhook
* Test webhook call
* View last response status & time

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


from flask import Flask, jsonify, request
from .db import init_db, db
import os, redis, json
from app.routes.products import bp as products_bp
from app.routes.webhooks import bp as webhooks_bp


def create_app():
    app = Flask(__name__)
    init_db(app)

    app.register_blueprint(products_bp)
    app.register_blueprint(webhooks_bp) 

    # Create tables on startup
    with app.app_context():
        db.create_all()

    # Basic health check
    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    # Serve the CSV upload page
    @app.get("/")
    def ui():
        return app.send_static_file("upload.html")

    # Upload endpoint
    @app.post("/upload")
    def upload():
        from uuid import uuid4
        from app.tasks import import_csv

        file = request.files.get("file")
        if not file:
            return {"error": "No file uploaded"}, 400

        job_id = str(uuid4())
        filepath = f"/shared_tmp/{job_id}.csv"
        file.save(filepath)

        import_csv.delay(job_id, filepath)
        return {"job_id": job_id}, 200

    # Polling endpoint
    @app.get("/status/<job_id>")
    def status(job_id):
        r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
        data = r.get(f"job:{job_id}:status")

        if not data:
            return {"percent": 0, "message": "Pending"}, 200

        return json.loads(data), 200
    
    @app.get("/products")
    def products_ui():
        return app.send_static_file("products.html")

    @app.get("/webhooks")
    def webhooks_ui():
        return app.send_static_file("webhooks.html")

    return app


# WSGI entrypoint
app = create_app()

from flask import Flask, jsonify, request
from .db import init_db, db
import os
import redis
import json

def create_app():
    app = Flask(__name__)

    init_db(app)

    # Create tables at startup
    with app.app_context():
        db.create_all()

    # Health check
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # Upload Endpoint
    @app.route("/upload", methods=["POST"])
    def upload():
        from uuid import uuid4
        from app.tasks import import_csv

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        job_id = str(uuid4())
        filepath = f"/shared_tmp/{job_id}.csv"
        file.save(filepath)

        import_csv.delay(job_id, filepath)

        return jsonify({"job_id": job_id}), 200

    # Polling Status Endpoint
    @app.route("/status/<job_id>")
    def status(job_id):
        r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))
        key = f"job:{job_id}:status"
        data = r.get(key)

        if not data:
            return jsonify({"percent": 0, "message": "Pending"}), 200

        return jsonify(json.loads(data)), 200

    return app


# WSGI entrypoint
app = create_app()

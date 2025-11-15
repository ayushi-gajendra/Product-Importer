from flask import Flask, jsonify
from .db import init_db, db


def create_app():
    app = Flask(__name__)

    init_db(app)

    with app.app_context():
        db.create_all()

    # ----- Health Check Endpoint -----
    @app.route("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    return app


# WSGI entrypoint
app = create_app()
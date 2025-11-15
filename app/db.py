from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/products"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

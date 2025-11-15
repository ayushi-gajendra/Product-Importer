from .db import db
from sqlalchemy.sql import func
from sqlalchemy import Index


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.BigInteger, primary_key=True)
    sku = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    description = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)

Index("ux_products_sku_lower", func.lower(Product.sku), unique=True)


class Webhook(db.Model):
    __tablename__ = "webhooks"
    id = db.Column(db.BigInteger, primary_key=True)
    url = db.Column(db.String, nullable=False)
    event = db.Column(db.String, default="import_complete")  
    enabled = db.Column(db.Boolean, default=True)
    last_status = db.Column(db.String)
    last_response_time_ms = db.Column(db.Integer)
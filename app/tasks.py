import csv
import json
import os
import time
import requests
from celery import Celery
from redis import Redis
from sqlalchemy import create_engine, text

# Celery config
celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL", "redis://redis:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://redis:6379/0"),
)

redis = Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/products"
)

engine = create_engine(DATABASE_URL)
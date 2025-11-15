from flask import Blueprint, request, jsonify
from app.models import Webhook
from app.db import db
import time, requests

bp = Blueprint("webhooks", __name__)


@bp.get("/api/webhooks")
def list_webhooks():
    hooks = Webhook.query.all()
    return jsonify([
        {
            "id": w.id,
            "url": w.url,
            "event": w.event,
            "enabled": w.enabled,
            "last_status": w.last_status,
            "last_response_time_ms": w.last_response_time_ms,
        }
        for w in hooks
    ])


@bp.post("/api/webhooks")
def create_webhook():
    data = request.json
    w = Webhook(**data)
    db.session.add(w)
    db.session.commit()
    return jsonify({"id": w.id}), 201


@bp.put("/api/webhooks/<int:id>")
def update_webhook(id):
    w = Webhook.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(w, key, value)
    db.session.commit()
    return {"status": "updated"}


@bp.delete("/api/webhooks/<int:id>")
def delete_webhook(id):
    w = Webhook.query.get_or_404(id)
    db.session.delete(w)
    db.session.commit()
    return {"status": "deleted"}

from flask import Blueprint, request, jsonify
from app.models import Product
from app.db import db

bp = Blueprint("products", __name__)


# ----------------------------------------------------------
# LIST (with filtering + pagination)
# ----------------------------------------------------------
@bp.get("/api/products")
def list_products():
    page = int(request.args.get("page", 1))
    sku = request.args.get("sku")
    name = request.args.get("name")
    desc = request.args.get("description")
    active = request.args.get("active")

    q = Product.query

    if sku:
        q = q.filter(Product.sku.ilike(f"%{sku}%"))
    if name:
        q = q.filter(Product.name.ilike(f"%{name}%"))
    if desc:
        q = q.filter(Product.description.ilike(f"%{desc}%"))
    if active is not None:
        q = q.filter(Product.active == (active.lower() == "true"))

    paginated = q.paginate(page=page, per_page=10)

    return jsonify({
        "items": [
            {
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "description": p.description,
                "active": p.active,
            }
            for p in paginated.items
        ],
        "page": paginated.page,
        "pages": paginated.pages,
    })


# ----------------------------------------------------------
# CREATE
# ----------------------------------------------------------
@bp.post("/api/products")
def create_product():
    data = request.json
    p = Product(**data)
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id}), 201


# ----------------------------------------------------------
# GET SINGLE
# ----------------------------------------------------------
@bp.get("/api/products/<int:id>")
def get_product(id):
    p = Product.query.get_or_404(id)
    return jsonify({
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "description": p.description,
        "active": p.active,
    })


# ----------------------------------------------------------
# UPDATE
# ----------------------------------------------------------
@bp.put("/api/products/<int:id>")
def update_product(id):
    p = Product.query.get_or_404(id)
    data = request.json

    for key, value in data.items():
        setattr(p, key, value)

    db.session.commit()
    return {"status": "updated"}


# ----------------------------------------------------------
# DELETE SINGLE
# ----------------------------------------------------------
@bp.delete("/api/products/<int:id>")
def delete_product(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return {"status": "deleted"}


# ----------------------------------------------------------
# BULK DELETE (STORY 3)
# ----------------------------------------------------------
@bp.delete("/api/products")
def bulk_delete():
    Product.query.delete()
    db.session.commit()
    return {"status": "all_deleted"}

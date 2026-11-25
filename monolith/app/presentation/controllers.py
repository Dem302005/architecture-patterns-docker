from flask import Blueprint, jsonify, request

from app.domain.errors import ValidationError
from app.presentation.dto import product_to_json, to_create_dto


def create_blueprint(list_products, create_product):
    bp = Blueprint("products", __name__)

    @bp.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @bp.get("/products")
    def products():
        return jsonify([product_to_json(p) for p in list_products.execute()]), 200

    @bp.post("/products")
    def add_product():
        payload = request.get_json(silent=True)
        try:
            product = create_product.execute(to_create_dto(payload))
        except ValidationError as error:
            return jsonify({"error": error.message}), 400
        return jsonify({"id": product.id}), 201

    return bp

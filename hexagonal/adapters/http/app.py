from flask import Flask, jsonify, request

from core.domain import OrderNotFound, ValidationError


def create_app(create_order, get_order):
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/orders")
    def post_order():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        try:
            order_id = create_order.execute(payload.get("sku"), payload.get("qty"))
        except ValidationError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify({"id": order_id}), 201

    @app.get("/orders/<order_id>")
    def fetch_order(order_id):
        try:
            order = get_order.execute(order_id)
        except OrderNotFound:
            return jsonify({"error": "order not found"}), 404
        return jsonify({"id": order.id, "sku": order.sku, "qty": order.qty})

    return app

from flask import Flask, jsonify, request

from bus import make_publisher
from orders_logic import OrderService, ValidationError


def create_app():
    service = OrderService(make_publisher())
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/orders")
    def create_order():
        try:
            order_id = service.create(request.get_json(silent=True))
        except ValidationError as error:
            return jsonify({"error": str(error)}), 400
        return jsonify({"id": order_id}), 201

    @app.post("/orders/<order_id>/republish")
    def republish(order_id):
        if not service.republish(order_id):
            return jsonify({"error": "order not found"}), 404
        return jsonify({"status": "republished", "id": order_id}), 202

    return app


app = create_app()

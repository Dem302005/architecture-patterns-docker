import itertools
import os
import threading

import yaml
from flask import Flask, jsonify, request

SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi.yaml")


def is_positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def create_app():
    app = Flask(__name__)
    orders = {}
    counter = itertools.count(1)
    lock = threading.Lock()

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/orders")
    def create_order():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        fields = ("userId", "itemId", "qty")
        if not all(is_positive_int(payload.get(f)) for f in fields):
            return jsonify({"error": "userId, itemId and qty must be positive integers"}), 400
        with lock:
            order_id = next(counter)
            orders[order_id] = {"id": order_id, **{f: payload[f] for f in fields}}
        return jsonify({"id": order_id}), 201

    @app.get("/orders/<int:order_id>")
    def get_order(order_id):
        order = orders.get(order_id)
        if order is None:
            return jsonify({"error": "order not found"}), 404
        return jsonify(order)

    @app.get("/openapi.yaml")
    def openapi_yaml():
        with open(SPEC_PATH, encoding="utf-8") as f:
            return f.read(), 200, {"Content-Type": "application/yaml"}

    @app.get("/openapi.json")
    def openapi_json():
        with open(SPEC_PATH, encoding="utf-8") as f:
            return jsonify(yaml.safe_load(f))

    return app


app = create_app()

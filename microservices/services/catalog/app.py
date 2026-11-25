import os

import yaml
from flask import Flask, jsonify

ITEMS = [
    {"id": 1, "name": "Desk"},
    {"id": 2, "name": "Chair"},
    {"id": 3, "name": "Lamp"},
]

SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi.yaml")


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/items")
    def items():
        return jsonify(ITEMS)

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

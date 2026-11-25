import os

import yaml
from flask import Flask, jsonify

USERS = {
    1: {"id": 1, "email": "anna@example.com"},
    2: {"id": 2, "email": "ivan@example.com"},
}

SPEC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi.yaml")


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/users/<int:user_id>")
    def get_user(user_id):
        user = USERS.get(user_id)
        if user is None:
            return jsonify({"error": "user not found"}), 404
        return jsonify(user)

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

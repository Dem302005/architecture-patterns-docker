import os

import pytest
import requests

BASE_URL = os.getenv("SMOKE_URL")

pytestmark = pytest.mark.skipif(not BASE_URL, reason="SMOKE_URL is not set")


def test_health():
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_create_and_list_product():
    r = requests.post(f"{BASE_URL}/products", json={"name": "Desk", "price": 199.9}, timeout=5)
    assert r.status_code == 201
    new_id = r.json()["id"]
    items = requests.get(f"{BASE_URL}/products", timeout=5).json()
    assert any(i["id"] == new_id and i["name"] == "Desk" and i["price"] == 199.9 for i in items)


@pytest.mark.parametrize("body", [{"name": "", "price": 10}, {"name": "Desk", "price": -1}, {}])
def test_invalid_payload_returns_400(body):
    r = requests.post(f"{BASE_URL}/products", json=body, timeout=5)
    assert r.status_code == 400

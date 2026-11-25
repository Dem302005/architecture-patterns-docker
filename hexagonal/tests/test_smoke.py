import os

import pytest
import requests

BASE_URL = os.getenv("SMOKE_URL")

pytestmark = pytest.mark.skipif(not BASE_URL, reason="SMOKE_URL is not set")


def test_create_and_get_order():
    r = requests.post(f"{BASE_URL}/orders", json={"sku": "ABC", "qty": 2}, timeout=5)
    assert r.status_code == 201
    order_id = r.json()["id"]
    got = requests.get(f"{BASE_URL}/orders/{order_id}", timeout=5)
    assert got.status_code == 200
    assert got.json() == {"id": order_id, "sku": "ABC", "qty": 2}


def test_unknown_order_returns_404():
    assert requests.get(f"{BASE_URL}/orders/does-not-exist", timeout=5).status_code == 404


def test_invalid_order_returns_400():
    assert requests.post(f"{BASE_URL}/orders", json={"sku": "ABC", "qty": 0}, timeout=5).status_code == 400

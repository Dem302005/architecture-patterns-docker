import os

import pytest
import requests

BASE_URL = os.getenv("GATEWAY_URL")

pytestmark = pytest.mark.skipif(not BASE_URL, reason="GATEWAY_URL is not set")


def test_gateway_health():
    assert requests.get(f"{BASE_URL}/health", timeout=5).status_code == 200


def test_catalog_items_through_gateway():
    r = requests.get(f"{BASE_URL}/catalog/items", timeout=5)
    assert r.status_code == 200
    items = r.json()
    assert items and {"id", "name"} <= set(items[0])


def test_user_through_gateway():
    r = requests.get(f"{BASE_URL}/users/1", timeout=5)
    assert r.status_code == 200
    assert r.json()["id"] == 1 and "@" in r.json()["email"]
    assert requests.get(f"{BASE_URL}/users/999", timeout=5).status_code == 404


def test_create_order_through_gateway():
    body = {"userId": 1, "itemId": 1, "qty": 1}
    r = requests.post(f"{BASE_URL}/orders", json=body, timeout=5)
    assert r.status_code == 201
    order_id = r.json()["id"]
    got = requests.get(f"{BASE_URL}/orders/{order_id}", timeout=5)
    assert got.status_code == 200 and got.json()["qty"] == 1


def test_orders_prefix_route_strips_prefix():
    body = {"userId": 2, "itemId": 3, "qty": 4}
    assert requests.post(f"{BASE_URL}/orders/orders", json=body, timeout=5).status_code == 201


def test_invalid_order_is_rejected():
    r = requests.post(f"{BASE_URL}/orders", json={"userId": 1}, timeout=5)
    assert r.status_code == 400


@pytest.mark.parametrize("service", ["catalog", "users", "orders"])
def test_openapi_available_in_each_service(service):
    r = requests.get(f"{BASE_URL}/{service}/openapi.json", timeout=5)
    assert r.status_code == 200
    assert r.json()["openapi"].startswith("3.")

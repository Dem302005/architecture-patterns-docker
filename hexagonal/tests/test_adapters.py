import pytest

from adapters.file.csv_repository import CsvOrderRepository
from config.settings import Settings
from config.wiring import build_app, build_repository
from core.domain import Order


def test_csv_repository_roundtrip(tmp_path):
    repo = CsvOrderRepository(str(tmp_path / "orders.csv"))
    order = Order.create("ABC", 2)
    repo.create(order)
    assert repo.get_by_id(order.id) == order
    assert repo.get_by_id("nope") is None
    assert (tmp_path / "orders.csv").read_text(encoding="utf-8").strip() == f"{order.id},ABC,2"


def test_csv_repository_persists_between_instances(tmp_path):
    path = str(tmp_path / "orders.csv")
    order = Order.create("XYZ", 5)
    CsvOrderRepository(path).create(order)
    assert CsvOrderRepository(path).get_by_id(order.id) == order


def test_factory_selects_adapter_by_env(tmp_path):
    settings = Settings({"REPO_ADAPTER": "file", "CSV_PATH": str(tmp_path / "o.csv")})
    assert type(build_repository(settings)).__name__ == "CsvOrderRepository"


def test_factory_rejects_unknown_adapter():
    with pytest.raises(ValueError):
        build_repository(Settings({"REPO_ADAPTER": "mongo"}))


def test_http_flow_with_csv_adapter(tmp_path):
    app = build_app(Settings({"REPO_ADAPTER": "file", "CSV_PATH": str(tmp_path / "o.csv")}))
    client = app.test_client()
    created = client.post("/orders", json={"sku": "ABC", "qty": 2})
    assert created.status_code == 201
    order_id = created.get_json()["id"]
    assert client.get(f"/orders/{order_id}").get_json() == {"id": order_id, "sku": "ABC", "qty": 2}
    assert client.get("/orders/missing").status_code == 404
    assert client.post("/orders", json={"sku": "ABC", "qty": 0}).status_code == 400

import pytest

from core.domain import Order, OrderNotFound, ValidationError
from core.ports import OrderRepository
from core.usecases import CreateOrder, GetOrder


class FakeRepository(OrderRepository):
    def __init__(self):
        self.items = {}

    def create(self, order):
        self.items[order.id] = order
        return order.id

    def get_by_id(self, order_id):
        return self.items.get(order_id)


@pytest.mark.parametrize("sku,qty", [("", 1), ("  ", 1), (None, 1), ("A", 0), ("A", -2), ("A", "2"), ("A", 1.5), ("A", True)])
def test_order_validation_rejects_bad_input(sku, qty):
    with pytest.raises(ValidationError):
        Order.create(sku, qty)


def test_create_order_saves_and_returns_id():
    repo = FakeRepository()
    order_id = CreateOrder(repo).execute("ABC", 2)
    assert repo.items[order_id].sku == "ABC"
    assert repo.items[order_id].qty == 2


def test_invalid_order_is_not_saved():
    repo = FakeRepository()
    with pytest.raises(ValidationError):
        CreateOrder(repo).execute("ABC", 0)
    assert repo.items == {}


def test_get_order_returns_existing():
    repo = FakeRepository()
    order_id = CreateOrder(repo).execute("ABC", 2)
    order = GetOrder(repo).execute(order_id)
    assert (order.sku, order.qty) == ("ABC", 2)


def test_get_missing_order_raises():
    with pytest.raises(OrderNotFound):
        GetOrder(FakeRepository()).execute("missing")

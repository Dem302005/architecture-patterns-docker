from core.domain import Order, OrderNotFound
from core.ports import OrderRepository


class CreateOrder:
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, sku, qty) -> str:
        order = Order.create(sku, qty)
        return self._repository.create(order)


class GetOrder:
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    def execute(self, order_id: str) -> Order:
        order = self._repository.get_by_id(order_id)
        if order is None:
            raise OrderNotFound(order_id)
        return order

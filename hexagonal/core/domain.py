import uuid
from dataclasses import dataclass


class ValidationError(Exception):
    pass


class OrderNotFound(Exception):
    pass


@dataclass(frozen=True)
class Order:
    id: str
    sku: str
    qty: int

    @staticmethod
    def create(sku, qty, order_id=None):
        if not isinstance(sku, str) or not sku.strip():
            raise ValidationError("sku must be a non-empty string")
        if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
            raise ValidationError("qty must be an integer greater than 0")
        return Order(id=order_id or str(uuid.uuid4()), sku=sku.strip(), qty=qty)

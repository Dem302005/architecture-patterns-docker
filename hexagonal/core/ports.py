from abc import ABC, abstractmethod
from typing import Optional

from core.domain import Order


class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> str:
        ...

    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        ...

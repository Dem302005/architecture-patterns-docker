from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import Product


class ProductRepository(ABC):
    @abstractmethod
    def create(self, product: Product) -> Product:
        ...

    @abstractmethod
    def list(self) -> List[Product]:
        ...

from dataclasses import dataclass
from typing import List

from app.application.ports import ProductRepository
from app.domain.entities import Product
from app.domain.validators import validate_product


@dataclass(frozen=True)
class CreateProductDto:
    name: object
    price: object


class CreateProduct:
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def execute(self, dto: CreateProductDto) -> Product:
        validate_product(dto.name, dto.price)
        product = Product(name=dto.name.strip(), price=float(dto.price))
        return self._repository.create(product)


class ListProducts:
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def execute(self) -> List[Product]:
        return self._repository.list()

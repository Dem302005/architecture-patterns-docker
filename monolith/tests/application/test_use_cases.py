import pytest

from app.application.ports import ProductRepository
from app.application.use_cases import CreateProduct, CreateProductDto, ListProducts
from app.domain.entities import Product
from app.domain.errors import ValidationError


class FakeRepository(ProductRepository):
    def __init__(self):
        self.items = []

    def create(self, product):
        saved = Product(id=len(self.items) + 1, name=product.name, price=product.price)
        self.items.append(saved)
        return saved

    def list(self):
        return list(self.items)


def test_create_product_saves_through_repository():
    repo = FakeRepository()
    created = CreateProduct(repo).execute(CreateProductDto(name="Desk", price=199.9))
    assert created.id == 1
    assert repo.items[0].name == "Desk"
    assert repo.items[0].price == 199.9


def test_create_product_trims_name():
    repo = FakeRepository()
    CreateProduct(repo).execute(CreateProductDto(name="  Desk  ", price=5))
    assert repo.items[0].name == "Desk"


@pytest.mark.parametrize("name,price", [("", 10), ("Desk", -5), ("Desk", 0)])
def test_invalid_input_raises_and_nothing_is_saved(name, price):
    repo = FakeRepository()
    with pytest.raises(ValidationError):
        CreateProduct(repo).execute(CreateProductDto(name=name, price=price))
    assert repo.items == []


def test_list_products_returns_saved_items():
    repo = FakeRepository()
    CreateProduct(repo).execute(CreateProductDto(name="A", price=1))
    CreateProduct(repo).execute(CreateProductDto(name="B", price=2))
    assert [p.name for p in ListProducts(repo).execute()] == ["A", "B"]

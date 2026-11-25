from app.application.use_cases import CreateProductDto
from app.domain.entities import Product


def to_create_dto(payload):
    if not isinstance(payload, dict):
        payload = {}
    return CreateProductDto(name=payload.get("name"), price=payload.get("price"))


def product_to_json(product: Product):
    return {"id": product.id, "name": product.name, "price": float(product.price)}

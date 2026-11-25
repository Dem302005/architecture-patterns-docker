from numbers import Real

from app.domain.errors import ValidationError

MAX_NAME_LENGTH = 100


def validate_product(name, price):
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("name must be a non-empty string")
    if len(name.strip()) > MAX_NAME_LENGTH:
        raise ValidationError("name must be at most 100 characters")
    if isinstance(price, bool) or not isinstance(price, Real):
        raise ValidationError("price must be a number")
    if price <= 0:
        raise ValidationError("price must be greater than 0")

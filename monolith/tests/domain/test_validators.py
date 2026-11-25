import pytest

from app.domain.errors import ValidationError
from app.domain.validators import validate_product


def test_valid_product_passes():
    validate_product("Desk", 199.9)


@pytest.mark.parametrize("name", ["", "   ", None, 5])
def test_empty_or_wrong_name_is_rejected(name):
    with pytest.raises(ValidationError):
        validate_product(name, 10)


def test_too_long_name_is_rejected():
    with pytest.raises(ValidationError):
        validate_product("x" * 101, 10)


@pytest.mark.parametrize("price", [0, -1, -0.01])
def test_non_positive_price_is_rejected(price):
    with pytest.raises(ValidationError):
        validate_product("Desk", price)


@pytest.mark.parametrize("price", ["10", None, True])
def test_non_numeric_price_is_rejected(price):
    with pytest.raises(ValidationError):
        validate_product("Desk", price)

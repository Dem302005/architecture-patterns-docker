from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Product:
    name: str
    price: float
    id: Optional[int] = None

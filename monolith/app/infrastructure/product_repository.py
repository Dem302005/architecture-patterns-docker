from typing import List

from app.application.ports import ProductRepository
from app.domain.entities import Product
from app.infrastructure.db import connect


class PostgresProductRepository(ProductRepository):
    def __init__(self, settings):
        self._settings = settings
        self._conn = connect(settings)
        self._conn.autocommit = True

    def _cursor(self):
        if self._conn.closed:
            self._conn = connect(self._settings)
            self._conn.autocommit = True
        return self._conn.cursor()

    def create(self, product: Product) -> Product:
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id",
                (product.name, product.price),
            )
            new_id = cur.fetchone()[0]
        return Product(id=new_id, name=product.name, price=product.price)

    def list(self) -> List[Product]:
        with self._cursor() as cur:
            cur.execute("SELECT id, name, price FROM products ORDER BY id")
            return [Product(id=r[0], name=r[1], price=float(r[2])) for r in cur.fetchall()]

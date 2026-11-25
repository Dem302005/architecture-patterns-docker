import time
from typing import Optional

import psycopg2

from core.domain import Order
from core.ports import OrderRepository

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    sku TEXT NOT NULL,
    qty INTEGER NOT NULL CHECK (qty > 0)
)
"""


class PostgresOrderRepository(OrderRepository):
    def __init__(self, host, port, name, user, password, retries=30):
        self._params = dict(host=host, port=port, dbname=name, user=user, password=password)
        self._conn = self._connect(retries)
        self._conn.autocommit = True
        with self._conn.cursor() as cur:
            cur.execute(SCHEMA)

    def _connect(self, retries=1):
        last = None
        for _ in range(retries):
            try:
                return psycopg2.connect(**self._params)
            except psycopg2.OperationalError as error:
                last = error
                time.sleep(1)
        raise last

    def _cursor(self):
        if self._conn.closed:
            self._conn = self._connect()
            self._conn.autocommit = True
        return self._conn.cursor()

    def create(self, order: Order) -> str:
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO orders (id, sku, qty) VALUES (%s, %s, %s)",
                (order.id, order.sku, order.qty),
            )
        return order.id

    def get_by_id(self, order_id: str) -> Optional[Order]:
        with self._cursor() as cur:
            cur.execute("SELECT id, sku, qty FROM orders WHERE id = %s", (order_id,))
            row = cur.fetchone()
        return Order(id=row[0], sku=row[1], qty=row[2]) if row else None

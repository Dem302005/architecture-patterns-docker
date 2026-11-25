import csv
import os
import threading
from typing import Optional

from core.domain import Order
from core.ports import OrderRepository


class CsvOrderRepository(OrderRepository):
    def __init__(self, path):
        self._path = path
        self._lock = threading.Lock()
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def create(self, order: Order) -> str:
        with self._lock:
            with open(self._path, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([order.id, order.sku, order.qty])
        return order.id

    def get_by_id(self, order_id: str) -> Optional[Order]:
        if not os.path.exists(self._path):
            return None
        with self._lock:
            with open(self._path, newline="", encoding="utf-8") as f:
                for row in csv.reader(f):
                    if len(row) == 3 and row[0] == order_id:
                        return Order(id=row[0], sku=row[1], qty=int(row[2]))
        return None

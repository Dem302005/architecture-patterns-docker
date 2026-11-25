import json
from typing import List

import redis

from app.application.ports import ProductRepository
from app.domain.entities import Product

CACHE_KEY = "products:all"


class CachedProductRepository(ProductRepository):
    def __init__(self, inner: ProductRepository, client, ttl: int = 30):
        self._inner = inner
        self._client = client
        self._ttl = ttl

    def create(self, product: Product) -> Product:
        created = self._inner.create(product)
        try:
            self._client.delete(CACHE_KEY)
        except redis.RedisError:
            pass
        return created

    def list(self) -> List[Product]:
        try:
            cached = self._client.get(CACHE_KEY)
        except redis.RedisError:
            cached = None
        if cached:
            return [Product(**item) for item in json.loads(cached)]
        products = self._inner.list()
        try:
            payload = json.dumps([{"id": p.id, "name": p.name, "price": p.price} for p in products])
            self._client.setex(CACHE_KEY, self._ttl, payload)
        except redis.RedisError:
            pass
        return products

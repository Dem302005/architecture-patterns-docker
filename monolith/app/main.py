import redis
from flask import Flask

from app.application.use_cases import CreateProduct, ListProducts
from app.infrastructure.cache import CachedProductRepository
from app.infrastructure.config import Settings
from app.infrastructure.product_repository import PostgresProductRepository
from app.presentation.controllers import create_blueprint


def build_repository(settings):
    repository = PostgresProductRepository(settings)
    if settings.redis_host:
        client = redis.Redis(host=settings.redis_host, port=settings.redis_port, socket_timeout=2)
        repository = CachedProductRepository(repository, client, settings.cache_ttl)
    return repository


def create_app(repository=None, settings=None):
    settings = settings or Settings()
    repository = repository or build_repository(settings)
    app = Flask(__name__)
    app.register_blueprint(create_blueprint(ListProducts(repository), CreateProduct(repository)))
    return app


def wsgi():
    return create_app()

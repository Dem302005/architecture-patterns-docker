# Layered Monolith

Каталог товарів із чотирма шарами. Залежності йдуть лише вниз: `presentation → application → domain`, а `infrastructure` реалізує порти, оголошені в `application`.

```
app/
  presentation/    Flask-контролери, DTO та мапінг (infrastructure не імпортують)
  application/     use-cases CreateProduct, ListProducts і порт ProductRepository
  domain/          Product, валідатор, помилки
  infrastructure/  PostgresProductRepository, Redis-кеш, db-клієнт, міграції
  main.py          composition root: єдине місце, де збираються всі шари
tests/
  domain/ application/ smoke/ test_architecture.py
```

## Запуск

```bash
docker compose up --build
```

Піднімаються `db` (postgres:16, volume `pgdata`), `redis` та `api`. Міграції застосовуються на старті контейнера `api` (`entrypoint.sh`), вручну: `make migrate`.

## Перевірка

```bash
curl localhost:8080/health
curl -X POST localhost:8080/products -H 'Content-Type: application/json' -d '{"name":"Desk","price":199.9}'
curl localhost:8080/products
```

Невалідний ввід (порожнє ім'я, `price <= 0`) повертає `400`.

## Тести

```bash
make test                # юніт-тести локально
make test-docker         # ті самі тести в контейнері (stage test у Dockerfile)
make smoke               # smoke-тести проти запущеної системи (SMOKE_URL=http://localhost:8080)
```

`tests/test_architecture.py` перевіряє через AST, що `presentation` не імпортує `infrastructure`, `application` залежить лише від `domain`, а `domain` ні від чого.

## Ускладнення

- **Redis-кеш** для `GET /products` (TTL 30 с, `CACHE_TTL`); вмикається змінною `REDIS_HOST`, кеш скидається після створення продукту, якщо Redis недоступний, застосунок працює без нього.
- **Міграції:** власний мінімальний runner (`app/infrastructure/migrate.py`, таблиця `schema_migrations`) і команда `make migrate`. Alembic/Flyway не використано.

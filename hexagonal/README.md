# Hexagonal (Ports & Adapters)

Ядро (`core/`) не знає ні про HTTP, ні про БД. Воно оголошує порт `OrderRepository`; адаптери його реалізують.

```
core/        domain (Order), ports (OrderRepository), usecases (CreateOrder, GetOrder)
adapters/
  http/      Flask-маршрути
  db/        PostgresOrderRepository
  file/      CsvOrderRepository (id,sku,qty)
config/      settings (ENV) і wiring (фабрика адаптера за ENV)
tests/       unit core, архітектурний тест, тести адаптерів, smoke
```

## Перемикання адаптера лише через ENV

```bash
REPO_ADAPTER=db   docker compose up --build     # Postgres
REPO_ADAPTER=file docker compose up --build     # CSV у volume csvdata (/data/orders.csv)
```

## Перевірка

```bash
curl -X POST localhost:8081/orders -H 'Content-Type: application/json' -d '{"sku":"ABC","qty":2}'
curl localhost:8081/orders/<id>
```

Невідомий id повертає `404`, невалідний ввід (`qty <= 0`, порожній `sku`) повертає `400`.

## Тести

```bash
python -m pytest                                   # core + адаптери
SMOKE_URL=http://localhost:8081 python -m pytest tests/test_smoke.py   # для кожного адаптера
```

`tests/test_architecture.py` перевіряє, що `core/` нічого не імпортує з `adapters/` і `config/`.

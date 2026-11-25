# Event-Driven (Kafka)

Топік `orders.events` (3 партиції), події в JSON, схеми в [`schemas/`](schemas).

```
POST /orders → orders ──OrderCreated──► billing ──PaymentCaptured──► notifications ──EmailSent──►
```

| Сервіс | Читає | Публікує |
|---|---|---|
| orders (Flask, `localhost:5002`) | | `OrderCreated` |
| billing | `OrderCreated` | `PaymentCaptured` |
| notifications | `PaymentCaptured` | `EmailSent` (+ лог листа) |

Ідемпотентність: billing і notifications зберігають оброблені `orderId` у таблиці `processed_event_ids` (SQLite у volume), тому повторна подія не створює другий платіж чи лист.

## Запуск

```bash
docker compose up --build
```

Контейнер `kafka-init` створює топік `orders.events`, після цього стартують сервіси.

## Перевірка

```bash
curl -X POST localhost:5002/orders -H 'Content-Type: application/json' -d '{"userId":1,"itemId":2,"qty":1}'
docker compose logs billing notifications
```

Повторна публікація тієї самої події (для перевірки дублів):

```bash
curl -X POST localhost:5002/orders/<id>/republish
docker compose logs billing    # "duplicate OrderCreated ignored", платіж один
```

## Тести

```bash
pip install -r services/orders/requirements.txt jsonschema pytest
python -m pytest
```

Тести проганяють ланцюг подій через in-memory шину, перевіряють JSON-схеми, відсутність дубль-платежу та збереження оброблених id між перезапусками.

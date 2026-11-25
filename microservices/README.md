# Microservices + API Gateway

Сервіси `catalog`, `users`, `orders` (in-memory) і NGINX-шлюз у мережі `ms-net`. Назовні відкрито лише шлюз (`localhost:8080`), сервіси між собою не звертаються.

| Шлях через шлюз | Куди проксується |
|---|---|
| `/catalog/*` | `catalog:5000/*` (наприклад `/catalog/items`) |
| `/users/*` | `users:5000/*`; також `/users/<id>` → `users:5000/users/<id>` |
| `/orders/*` | `orders:5000/*`; також `POST /orders` і `GET /orders/<id>` → `orders:5000/orders…` |

Сервіси мають healthcheck, `restart: on-failure`; шлюз стартує після `service_healthy` і повторює запит до upstream (`proxy_next_upstream`). OpenAPI-специфікація кожного сервісу: `services/*/openapi.yaml`, також доступна на `/openapi.yaml` і `/openapi.json` сервісу (через шлюз, наприклад `/catalog/openapi.json`).

## Запуск і перевірка

```bash
docker compose up --build
curl localhost:8080/catalog/items
curl -X POST localhost:8080/orders -H 'Content-Type: application/json' -d '{"userId":1,"itemId":1,"qty":1}'
```

## e2e-тести через шлюз

```bash
GATEWAY_URL=http://localhost:8080 python -m pytest tests -v
```

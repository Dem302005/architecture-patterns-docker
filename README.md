# architecture-patterns-docker

Практичне завдання з архітектури ПЗ на основі Docker. Чотири невеликі проєкти на Python (Flask), кожен у своїй теці зі своїм `docker-compose.yml`.

| Тека | Архітектура | Порт | Запуск |
|---|---|---|---|
| [`monolith/`](monolith) | Layered Monolith (presentation → application → domain → infrastructure), Postgres, Redis-кеш | 8080 | `docker compose up --build` |
| [`hexagonal/`](hexagonal) | Hexagonal (Ports & Adapters), адаптери Postgres / CSV перемикаються через `REPO_ADAPTER` | 8081 | `docker compose up --build` |
| [`microservices/`](microservices) | 3 мікросервіси + NGINX API Gateway | 8080 | `docker compose up --build` |
| [`event-driven/`](event-driven) | Kafka: orders → billing → notifications, ідемпотентність у billing | 5002 | `docker compose up --build` |

Кожна тека має власний `README.md` з описом структури, командами перевірки (`curl`) та запуску тестів.

## Швидка перевірка юніт-тестів без Docker

```bash
pip install -r monolith/requirements-dev.txt jsonschema
cd monolith && python -m pytest tests/domain tests/application tests/test_architecture.py
cd ../hexagonal && python -m pytest
cd ../event-driven && python -m pytest
```

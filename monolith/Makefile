.PHONY: up test test-docker migrate smoke

up:
	docker compose up --build

test:
	python -m pytest tests/domain tests/application tests/test_architecture.py -v

test-docker:
	docker build --target test -t monolith-test . && docker run --rm monolith-test

migrate:
	docker compose run --rm api python -m app.infrastructure.migrate

smoke:
	SMOKE_URL=http://localhost:8080 python -m pytest tests/smoke -v

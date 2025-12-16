up:
	docker compose up --build

down:
	docker compose down -v

test:
	poetry run pytest -q

lint:
	poetry run ruff check .

alembic-up:
	poetry run alembic upgrade head

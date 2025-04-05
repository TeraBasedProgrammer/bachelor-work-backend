run:
	docker compose up -d

# migrate:
# 	docker compose exec app python manage.py migrate

down:
	docker compose down

volume-down:
	docker compose down -v

logs:
	docker compose logs -f

stop:
	docker compose stop

build:
	docker compose up -d --build

restart:
	docker compose restart

rerun:
	docker compose down
	docker compose up -d

rebuild:
	docker compose down
	docker compose up -d --build
	docker image prune

redis:
	docker compose exec redis redis-cli

database:
	pgcli postgresql://postgres:password123456@localhost:5432/mentorship_app

lint:
	black . && isort . --profile=black && flake8 .

clean_pycache: ## Removes the __pycaches__
	sudo find . -type f -name "*.pyc" -delete
	sudo find . -type d -name "__pycache__" -exec rm -r {} +

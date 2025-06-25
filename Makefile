
# Makefile for InvestMateAI project

build:
	docker-compose up --build
up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f web

db:
	docker-compose exec db psql -U postgres -d realestate

migrate:
	docker-compose exec web alembic upgrade head

makemigration:
	docker-compose exec web alembic revision --autogenerate -m "manual update"

restart:
	docker-compose down && docker-compose up --build

prune:
	docker system prune -af && docker volume prune -f

.PHONY: up down logs db migrate makemigration restart prune

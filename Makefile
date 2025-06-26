
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

### Alembic commands

# צור מיגרציה חדשה עם הודעה
migrate:
	docker-compose exec web alembic revision --autogenerate -m "$(m)"

# הרץ את כל המיגרציות
upgrade:
	docker-compose exec web alembic upgrade head

# חזור למיגרציה קודמת (שימושי כשיש באג)
downgrade:
	docker-compose exec web alembic downgrade -1

# הדפס גרסה נוכחית במסד הנתונים
current:
	docker-compose exec web alembic current

# הצג היסטוריית מיגרציות
history:
	docker-compose exec web alembic history

# פתח טרמינל אינטראקטיבי בתוך Alembic
alembic:
	docker-compose exec web alembic


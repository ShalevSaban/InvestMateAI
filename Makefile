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

restart:
	docker-compose down && docker-compose up --build

prune:
	docker system prune -af && docker volume prune -f

### Testing commands

# Run all tests
test:
	docker-compose exec web python -m pytest app/tests/ -v

# Run tests with coverage report
test-coverage:
	docker-compose exec web python -m pytest app/tests/ --cov=app --cov-report=html

# Run specific test file
test-file:
	docker-compose exec web python -m pytest app/tests/test_main.py -v

# Run tests and stop on first failure (useful for debugging)
test-debug:
	docker-compose exec web python -m pytest app/tests/ -v -x

# Install test dependencies
test-setup:
	docker-compose exec web pip install pytest pytest-asyncio factory-boy pytest-cov

### Alembic commands

# Create new migration with message
migrate:
	docker-compose exec web alembic revision --autogenerate -m "$(m)"

# Run all migrations
upgrade:
	docker-compose exec web alembic upgrade head

# Rollback to previous migration
downgrade:
	docker-compose exec web alembic downgrade -1

# Show current database version
current:
	docker-compose exec web alembic current

# Show migration history
history:
	docker-compose exec web alembic history
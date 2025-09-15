# Development Commands

.PHONY: help dev dev-watch test test-coverage format lint type-check quality migrate-create migrate-up migrate-down docker-up docker-down

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development
dev: ## Start development server
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

dev-watch: ## Start development server with file watching
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir src

# Testing
test: ## Run all tests
	uv run pytest

test-coverage: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=html --cov-report=term

test-file: ## Run specific test file (usage: make test-file FILE=test_kolam_detection.py)
	uv run pytest tests/$(FILE)

# Code Quality
format: ## Format code with ruff
	uv run ruff format src/ tests/

lint: ## Lint code with ruff
	uv run ruff check src/ tests/

type-check: ## Type check with mypy
	uv run mypy src/

quality: format lint type-check ## Run all quality checks

# Database
migrate-create: ## Create new migration (usage: make migrate-create MESSAGE="your message")
	uv run alembic revision --autogenerate -m "$(MESSAGE)"

migrate-up: ## Apply migrations
	uv run alembic upgrade head

migrate-down: ## Rollback last migration
	uv run alembic downgrade -1

# Docker
docker-up: ## Start all services with Docker Compose
	docker-compose up -d

docker-down: ## Stop all services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

# AI/ML
download-models: ## Download pre-trained models
	mkdir -p models/
	# Add model download commands here

train-detection: ## Train detection model
	uv run python scripts/train_detection_model.py

generate-sample: ## Generate sample Kolam
	uv run python scripts/generate_sample_kolam.py

# Setup
setup: ## Initial setup
	uv sync
	pre-commit install
	cp env.example .env
	make migrate-up

# Cleanup
clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .coverage htmlcov/ .pytest_cache/
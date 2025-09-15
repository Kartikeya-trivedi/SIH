# Kolam Learning Platform

An AI-powered platform for learning, exploring, and celebrating the traditional Indian art of Kolam (also known as muggu, rangoli, and rangavalli). This platform blends cultural heritage with modern technology to provide interactive learning experiences.

## Features

- **Kolam Detection**: Upload images and get AI-powered analysis of Kolam patterns
- **Pattern Generation**: Create new Kolam designs using mathematical principles
- **Interactive Learning**: Duolingo-style quizzes and progress tracking
- **Community Features**: Share designs and learn from others
- **AI-Powered Insights**: Get explanations and hints using local LLMs

## Tech Stack

- **Backend**: FastAPI with async support
- **Database**: PostgreSQL with SQLAlchemy and Alembic migrations
- **Search**: OpenSearch for text and vector similarity search
- **AI/ML**: TensorFlow, PyTorch, OpenCV for image processing
- **LLM**: Ollama for local language model integration
- **DevOps**: Docker, Airflow, uv for package management

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the development server:
```bash
uv run kolam-api
```

4. Access the API documentation at `http://localhost:8000/docs`

## Development

- **Linting**: `ruff check src/`
- **Formatting**: `ruff format src/`
- **Type checking**: `mypy src/`
- **Tests**: `pytest`
- **Pre-commit**: `pre-commit run --all-files`

## Project Structure

```
src/
├── api/           # FastAPI routers and endpoints
├── core/          # Core configuration and utilities
├── db/            # Database models and migrations
├── services/      # Business logic services
├── schemas/       # Pydantic models
├── ai/            # AI/ML modules for detection and generation
├── search/        # OpenSearch integration
└── main.py        # Application entry point
```

## List of Contributors 

Janhvi Bisht
Kartikeya Trivedi
Krishna Gupta
Kushagra Chaudhary
Nakshatra Vidyarthi
Rounak Gope


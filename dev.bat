@echo off
REM Windows development commands for Kolam Learning Platform

if "%1"=="dev" goto dev
if "%1"=="test" goto test
if "%1"=="format" goto format
if "%1"=="lint" goto lint
if "%1"=="docker-up" goto docker-up
if "%1"=="docker-down" goto docker-down
if "%1"=="migrate-up" goto migrate-up
if "%1"=="migrate-down" goto migrate-down
if "%1"=="setup" goto setup
goto help

:dev
echo Starting development server...
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
goto end

:test
echo Running tests...
uv run pytest
goto end

:format
echo Formatting code...
uv run ruff format src/ tests/
goto end

:lint
echo Linting code...
uv run ruff check src/ tests/
goto end

:docker-up
echo Starting Docker services...
docker-compose up -d
goto end

:docker-down
echo Stopping Docker services...
docker-compose down
goto end

:migrate-up
echo Running database migrations...
uv run alembic upgrade head
goto end

:migrate-down
echo Rolling back database migrations...
uv run alembic downgrade -1
goto end

:setup
echo Running setup...
call setup.bat
goto end

:help
echo Available commands:
echo   dev.bat dev         - Start development server
echo   dev.bat test        - Run tests
echo   dev.bat format      - Format code
echo   dev.bat lint        - Lint code
echo   dev.bat docker-up   - Start Docker services
echo   dev.bat docker-down - Stop Docker services
echo   dev.bat migrate-up  - Run database migrations
echo   dev.bat migrate-down - Rollback database migrations
echo   dev.bat setup       - Run initial setup
goto end

:end



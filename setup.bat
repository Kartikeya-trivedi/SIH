@echo off
REM Windows setup script for Kolam Learning Platform

echo Setting up Kolam Learning Platform...

REM Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing uv...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
)

REM Install dependencies
echo Installing dependencies...
uv sync

REM Install pre-commit
echo Installing pre-commit...
uv add pre-commit

REM Copy environment file
if not exist .env (
    echo Creating .env file...
    copy env.example .env
)

REM Create necessary directories
echo Creating directories...
if not exist uploads mkdir uploads
if not exist generated_images mkdir generated_images
if not exist models mkdir models
if not exist logs mkdir logs

echo Setup completed!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Start Docker services: docker-compose up -d
echo 3. Run migrations: uv run alembic upgrade head
echo 4. Start development server: uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

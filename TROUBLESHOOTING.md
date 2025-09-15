# Troubleshooting Guide

## Common Issues and Solutions

### Windows Setup Issues

#### 1. `make` command not found
**Problem**: Windows doesn't have `make` by default.

**Solution**: Use the Windows batch scripts instead:
```cmd
# Instead of: make dev
dev.bat dev

# Instead of: make docker-up  
dev.bat docker-up

# Instead of: make migrate-up
dev.bat migrate-up
```

#### 2. `pre-commit` not found
**Problem**: pre-commit is not installed or not in PATH.

**Solution**: Install it manually:
```cmd
uv add pre-commit
# or
pip install pre-commit
```

#### 3. Dependency resolution errors
**Problem**: OpenTelemetry packages have version conflicts.

**Solution**: Use the simplified requirements.txt:
```cmd
pip install -r requirements.txt
```

#### 4. PowerShell execution policy
**Problem**: PowerShell scripts are blocked.

**Solution**: Enable script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker Issues

#### 1. Docker not running
**Problem**: Docker Desktop is not started.

**Solution**: Start Docker Desktop and wait for it to be ready.

#### 2. Port conflicts
**Problem**: Ports 8000, 5432, 9200, etc. are already in use.

**Solution**: Stop conflicting services or change ports in docker-compose.yml.

### Database Issues

#### 1. Connection refused
**Problem**: PostgreSQL is not running.

**Solution**: 
```cmd
dev.bat docker-up
# Wait for services to start, then:
dev.bat migrate-up
```

#### 2. Migration errors
**Problem**: Database schema is out of sync.

**Solution**: Reset the database:
```cmd
docker-compose down -v
docker-compose up -d postgres
# Wait for postgres to start, then:
dev.bat migrate-up
```

### Python Environment Issues

#### 1. Wrong Python version
**Problem**: Using Python < 3.11.

**Solution**: Install Python 3.11+ or use uv to manage Python versions:
```cmd
uv python install 3.11
uv sync
```

#### 2. Virtual environment issues
**Problem**: Dependencies not found in virtual environment.

**Solution**: Recreate the environment:
```cmd
rm -rf .venv
uv sync
```

### AI/ML Dependencies

#### 1. TensorFlow installation issues
**Problem**: TensorFlow fails to install on Windows.

**Solution**: Install CPU-only version:
```cmd
pip install tensorflow-cpu
```

#### 2. OpenCV issues
**Problem**: OpenCV installation fails.

**Solution**: Install opencv-python-headless:
```cmd
pip install opencv-python-headless
```

### Development Server Issues

#### 1. Import errors
**Problem**: Module not found errors.

**Solution**: Ensure PYTHONPATH includes src:
```cmd
set PYTHONPATH=%PYTHONPATH%;src
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Port already in use
**Problem**: Port 8000 is occupied.

**Solution**: Use a different port:
```cmd
uv run uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

## Getting Help

If you encounter issues not covered here:

1. Check the logs in the `logs/` directory
2. Run with verbose output: `uv run uvicorn src.main:app --log-level debug`
3. Check Docker logs: `docker-compose logs`
4. Verify all services are running: `docker-compose ps`

## Minimal Setup (Fallback)

If the full setup fails, try this minimal approach:

1. Install Python 3.11+
2. Install pip dependencies:
   ```cmd
   pip install fastapi uvicorn sqlalchemy pydantic
   ```
3. Run the basic server:
   ```cmd
   python -m uvicorn src.m
ain:app --host 0.0.0.0 --port 8000 --reload
   ```

This will get the basic API running without AI/ML features, Docker, or advanced monitoring.
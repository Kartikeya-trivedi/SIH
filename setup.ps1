# PowerShell setup script for Kolam Learning Platform

Write-Host "Setting up Kolam Learning Platform..." -ForegroundColor Green

# Check if uv is installed
try {
    uv --version | Out-Null
    Write-Host "uv is already installed" -ForegroundColor Green
} catch {
    Write-Host "Installing uv..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -OutFile "install-uv.ps1"
    .\install-uv.ps1
    Remove-Item "install-uv.ps1"
}

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
uv sync

# Install pre-commit
Write-Host "Installing pre-commit..." -ForegroundColor Yellow
uv add pre-commit

# Copy environment file
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
}

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
$directories = @("uploads", "generated_images", "models", "logs")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

Write-Host "Setup completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your configuration" -ForegroundColor White
Write-Host "2. Start Docker services: docker-compose up -d" -ForegroundColor White
Write-Host "3. Run migrations: uv run alembic upgrade head" -ForegroundColor White
Write-Host "4. Start development server: uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload" -ForegroundColor White



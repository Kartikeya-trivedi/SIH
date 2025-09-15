# 🎨 Kolam Learning Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)]()

An AI-powered platform for learning, exploring, and celebrating the traditional Indian art of Kolam (also known as muggu, rangoli, and rangavalli). This platform blends cultural heritage with modern technology to provide interactive learning experiences.

## ✨ Features

### 🧠 AI-Powered Capabilities
- **Kolam Detection**: Upload images and get AI-powered analysis of Kolam patterns
- **Pattern Generation**: Create new Kolam designs using mathematical principles and AI
- **Smart Recognition**: Identify traditional patterns and their cultural significance
- **AI-Powered Insights**: Get explanations and hints using local LLMs

### 📚 Interactive Learning
- **Duolingo-style Quizzes**: Progressive learning with gamified elements
- **Progress Tracking**: Monitor your learning journey and achievements
- **Cultural Context**: Learn about the history and meaning behind patterns
- **Difficulty Levels**: From beginner to advanced patterns

### 🌐 Community Features
- **Pattern Sharing**: Share your creations with the community
- **Learning from Others**: Discover patterns created by fellow learners
- **Collaborative Learning**: Work together on complex designs
- **Cultural Exchange**: Connect with people passionate about traditional art

### 🔧 Technical Features
- **Real-time Processing**: Fast image analysis and generation
- **Offline Capability**: Works without internet using local AI models
- **Cross-platform**: Web, mobile, and desktop support
- **Scalable Architecture**: Built for growth and performance

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Git

### Option 1: SQLite (Recommended for Development)

**No database setup required!** The application works out of the box with SQLite.

```bash
# Clone the repository
git clone https://github.com/your-org/kolam-learning-platform.git
cd kolam-learning-platform

# Install dependencies
uv sync

# Start the development server
.\dev.bat dev  # Windows
# or
make dev       # Linux/macOS
```

**That's it!** 🎉 Your server will be running at `http://localhost:8000`

### Option 2: Full Stack with PostgreSQL

For production or advanced features:

```bash
# Start all services with Docker
.\dev.bat docker-up  # Windows
# or
docker-compose up -d  # Linux/macOS

# Run database migrations
.\dev.bat migrate-up

# Start the development server
.\dev.bat dev
```

## 📖 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🛠️ Development

### Windows Commands

| Command | Description |
|---------|-------------|
| `.\dev.bat dev` | Start development server with hot reload |
| `.\dev.bat test` | Run all tests |
| `.\dev.bat format` | Format code with ruff |
| `.\dev.bat lint` | Lint code with ruff |
| `.\dev.bat docker-up` | Start all Docker services |
| `.\dev.bat docker-down` | Stop all Docker services |
| `.\dev.bat migrate-up` | Run database migrations |
| `.\dev.bat migrate-down` | Rollback database migrations |
| `.\dev.bat setup` | Run initial setup |

### Linux/macOS Commands

```bash
# Development
make dev              # Start development server
make test             # Run tests
make format           # Format code
make lint             # Lint code
make docker-up        # Start Docker services
make docker-down      # Stop Docker services

# Code Quality
ruff check src/       # Lint code
ruff format src/      # Format code
mypy src/            # Type checking
pytest               # Run tests
pre-commit run --all-files  # Run pre-commit hooks
```

## 🏗️ Project Structure

```
kolam-learning-platform/
├── 📁 src/
│   ├── 📁 api/              # FastAPI routers and endpoints
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── kolam.py         # Kolam-related endpoints
│   │   ├── learning.py      # Learning platform endpoints
│   │   └── users.py         # User management endpoints
│   ├── 📁 core/             # Core configuration and utilities
│   │   ├── config.py        # Application settings
│   │   ├── database.py      # Database configuration
│   │   ├── logging.py       # Logging setup
│   │   └── security.py      # Security utilities
│   ├── 📁 db/               # Database models and migrations
│   │   └── models/          # SQLAlchemy models
│   ├── 📁 services/         # Business logic services
│   │   ├── 📁 ai/           # AI/ML services
│   │   │   ├── detection_service.py    # Kolam detection
│   │   │   ├── generation_service.py   # Pattern generation
│   │   │   └── ollama_service.py       # LLM integration
│   │   ├── auth_service.py  # Authentication logic
│   │   ├── kolam_service.py # Kolam business logic
│   │   ├── learning_service.py # Learning platform logic
│   │   └── user_service.py  # User management logic
│   ├── 📁 schemas/          # Pydantic models for API
│   ├── 📁 search/           # OpenSearch integration
│   └── main.py              # Application entry point
├── 📁 tests/                # Test files
├── 📁 monitoring/           # Monitoring and observability
│   ├── 📁 grafana/          # Grafana dashboards
│   └── prometheus.yml       # Prometheus configuration
├── 📁 scripts/              # Utility scripts
├── 📁 uploads/              # File uploads directory
├── 📁 generated_images/     # AI-generated images
├── 📁 logs/                 # Application logs
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Container configuration
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Python dependencies
├── alembic.ini            # Database migration configuration
└── README.md              # This file
```

## 🧪 Testing

```bash
# Run all tests
.\dev.bat test  # Windows
make test       # Linux/macOS

# Run specific test categories
pytest tests/test_api_endpoints.py
pytest tests/test_kolam_detection.py
pytest tests/test_kolam_generation.py

# Run with coverage
pytest --cov=src tests/
```

## 🐳 Docker Support

The platform includes comprehensive Docker support for all services:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

### Services Included:
- **PostgreSQL**: Primary database
- **OpenSearch**: Search and vector operations
- **Ollama**: Local LLM for AI features
- **Redis**: Caching and session storage
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=sqlite:///./kolam.db  # For development
# DATABASE_URL=postgresql://user:pass@localhost:5432/kolam_db  # For production

# AI/ML Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXIRE_MINUTES=30

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
```

### Database Options

1. **SQLite** (Default - No setup required)
   - Perfect for development
   - No external dependencies
   - File-based database

2. **PostgreSQL** (Production recommended)
   - Better performance
   - Advanced features
   - Requires Docker or local installation

## 📊 Monitoring & Observability

The platform includes comprehensive monitoring:

- **Health Checks**: `/health` endpoint
- **Metrics**: Prometheus integration
- **Logging**: Structured logging with context
- **Tracing**: OpenTelemetry support
- **Dashboards**: Grafana visualizations

Access monitoring at:
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `.\dev.bat test`
5. Format code: `.\dev.bat format`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Contributors**: Thank you to all contributors who help make this project better
- **Open Source**: Built on amazing open-source technologies
- **Community**: Inspired by the vibrant Kolam art community
- **Cultural Heritage**: Honoring the rich tradition of Indian art

## 👥 Contributors

- **Janhvi Bisht** 
- **Kartikeya Trivedi**
- **Krishna Gupta** 
- **Kushagra Chaudhary** 
- **Nakshatra Vidyarthi**
- **Rounak Gope** 

## 📞 Support

- **Documentation**: [Wiki](https://github.com/your-org/kolam-learning-platform/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-org/kolam-learning-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/kolam-learning-platform/discussions)
- **Email**: team@techtitans.dev

## 🗺️ Roadmap

- [ ] Mobile app (React Native)
- [ ] Advanced AI pattern recognition
- [ ] 3D Kolam visualization
- [ ] AR/VR integration
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Social features
- [ ] Educational curriculum integration

---

**Made with ❤️ by the TechTitans team**

*Preserving cultural heritage through technology*
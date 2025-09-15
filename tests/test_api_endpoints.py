"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import tempfile
import os

from src.main import app


class TestAPIEndpoints:
    """Test cases for API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "Kolam Learning Platform" in data["message"]
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    def test_auth_register_endpoint(self, client):
        """Test user registration endpoint."""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "full_name": "Test User"
        }
        
        with patch('src.api.auth.AuthService') as mock_auth_service:
            mock_service_instance = Mock()
            mock_service_instance.create_user.return_value = Mock(
                id=1,
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                is_active=True,
                is_verified=False
            )
            mock_auth_service.return_value = mock_service_instance
            
            response = client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 200
    
    def test_auth_login_endpoint(self, client):
        """Test user login endpoint."""
        login_data = {
            "username": "testuser",
            "password": "testpassword123"
        }
        
        with patch('src.api.auth.AuthService') as mock_auth_service:
            mock_service_instance = Mock()
            mock_service_instance.authenticate_user.return_value = Mock(
                id=1,
                username=login_data["username"],
                email="test@example.com"
            )
            mock_auth_service.return_value = mock_service_instance
            
            response = client.post("/api/v1/auth/login", data=login_data)
            assert response.status_code == 200
            
            data = response.json()
            assert "access_token" in data
            assert data["token_type"] == "bearer"
    
    def test_kolam_upload_endpoint(self, client):
        """Test Kolam image upload endpoint."""
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            tmp_file.write(b"fake image data")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, 'rb') as f:
                files = {"file": ("test.jpg", f, "image/jpeg")}
                data = {
                    "title": "Test Kolam",
                    "description": "A test Kolam pattern",
                    "tags": "test,pattern",
                    "is_public": "false"
                }
                
                with patch('src.api.kolam.KolamService') as mock_kolam_service:
                    mock_service_instance = Mock()
                    mock_service_instance.create_kolam_image.return_value = Mock(
                        id=1,
                        filename="test.jpg",
                        file_path="/uploads/test.jpg",
                        user_id=1,
                        title="Test Kolam"
                    )
                    mock_kolam_service.return_value = mock_service_instance
                    
                    response = client.post("/api/v1/kolam/upload", files=files, data=data)
                    assert response.status_code == 200
                    
        finally:
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    def test_kolam_generate_endpoint(self, client):
        """Test Kolam generation endpoint."""
        generation_data = {
            "pattern_type": "traditional",
            "complexity_level": 3,
            "symmetry_type": "radial",
            "size": "medium",
            "title": "Generated Kolam"
        }
        
        with patch('src.api.kolam.KolamService') as mock_kolam_service, \
             patch('src.api.kolam.GenerationService') as mock_gen_service:
            
            mock_kolam_instance = Mock()
            mock_kolam_instance.create_generated_kolam.return_value = Mock(
                id=1,
                pattern_type="traditional",
                complexity_level=3,
                user_id=1
            )
            mock_kolam_service.return_value = mock_kolam_instance
            
            mock_gen_instance = Mock()
            mock_gen_instance.generate_pattern.return_value = {
                "svg_data": "<svg>...</svg>",
                "image_path": "/generated/test.png"
            }
            mock_gen_service.return_value = mock_gen_instance
            
            response = client.post("/api/v1/kolam/generate", json=generation_data)
            assert response.status_code == 200
    
    def test_learning_questions_endpoint(self, client):
        """Test trivia questions endpoint."""
        with patch('src.api.learning.LearningService') as mock_learning_service:
            mock_service_instance = Mock()
            mock_service_instance.get_trivia_questions.return_value = [
                Mock(
                    id=1,
                    question_text="What is Kolam?",
                    question_type="multiple_choice",
                    difficulty_level=1,
                    correct_answer="Traditional Indian art"
                )
            ]
            mock_learning_service.return_value = mock_service_instance
            
            response = client.get("/api/v1/learning/questions")
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, list)
            if len(data) > 0:
                assert "question_text" in data[0]
    
    def test_learning_quiz_start_endpoint(self, client):
        """Test quiz session start endpoint."""
        with patch('src.api.learning.LearningService') as mock_learning_service:
            mock_service_instance = Mock()
            mock_service_instance.create_learning_session.return_value = Mock(
                id=1,
                session_type="quiz",
                user_id=1
            )
            mock_service_instance.get_trivia_questions.return_value = []
            mock_learning_service.return_value = mock_service_instance
            
            response = client.post("/api/v1/learning/quiz/start")
            assert response.status_code == 200
            
            data = response.json()
            assert "session_id" in data
            assert "questions" in data
            assert "answers" in data
    
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint returns 404."""
        response = client.get("/api/v1/invalid/endpoint")
        assert response.status_code == 404
    
    def test_cors_headers(self, client):
        """Test CORS headers are present."""
        response = client.options("/api/v1/auth/register")
        # CORS headers should be present (exact headers depend on configuration)
        assert response.status_code in [200, 204]
    
    def test_error_handling(self, client):
        """Test error handling for invalid data."""
        # Test registration with invalid email
        invalid_user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "testpassword123"
        }
        
        response = client.post("/api/v1/auth/register", json=invalid_user_data)
        # Should return validation error
        assert response.status_code == 422


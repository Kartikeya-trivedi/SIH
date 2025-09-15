"""Tests for Kolam detection service."""

import pytest
import numpy as np
from unittest.mock import Mock, patch
import tempfile
import os

from src.services.ai.detection_service import DetectionService
from src.schemas import KolamImageAnalysis


class TestDetectionService:
    """Test cases for Kolam detection service."""
    
    @pytest.fixture
    def detection_service(self):
        """Create detection service instance."""
        return DetectionService()
    
    @pytest.fixture
    def sample_image_path(self):
        """Create a temporary sample image file."""
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            # Create a simple test image (random data)
            test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
            # In a real test, you'd save this as an actual image file
            tmp_file.write(test_image.tobytes())
            return tmp_file.name
    
    def test_detection_service_initialization(self, detection_service):
        """Test detection service initialization."""
        assert detection_service is not None
        assert detection_service.pattern_classes is not None
        assert len(detection_service.pattern_classes) > 0
    
    @pytest.mark.asyncio
    async def test_analyze_image_basic(self, detection_service, sample_image_path):
        """Test basic image analysis."""
        try:
            # Mock the image loading and processing
            with patch.object(detection_service, '_load_and_preprocess_image') as mock_load:
                mock_load.return_value = np.random.random((224, 224, 3)).astype(np.float32)
                
                analysis = await detection_service.analyze_image(sample_image_path)
                
                assert isinstance(analysis, KolamImageAnalysis)
                assert analysis.detected_patterns is not None
                assert analysis.confidence_scores is not None
                assert analysis.complexity_score is not None
                assert analysis.symmetry_type is not None
                assert analysis.geometric_features is not None
                
        finally:
            # Clean up
            if os.path.exists(sample_image_path):
                os.unlink(sample_image_path)
    
    def test_extract_basic_features(self, detection_service):
        """Test basic feature extraction."""
        # Create a test image
        test_image = np.random.random((224, 224, 3)).astype(np.float32)
        
        features = detection_service._extract_basic_features(test_image)
        
        assert 'brightness' in features
        assert 'contrast' in features
        assert 'edges' in features
        assert 'corners' in features
        
        assert isinstance(features['brightness'], float)
        assert isinstance(features['contrast'], float)
        assert isinstance(features['edges'], np.ndarray)
    
    def test_calculate_complexity(self, detection_service):
        """Test complexity calculation."""
        test_image = np.random.random((224, 224, 3)).astype(np.float32)
        features = {
            'brightness': 128.0,
            'contrast': 50.0,
            'edges': np.random.random((224, 224)),
            'corners': np.array([[100, 100], [150, 150]])
        }
        
        complexity = detection_service._calculate_complexity(test_image, features)
        
        assert isinstance(complexity, float)
        assert 0.0 <= complexity <= 1.0
    
    def test_detect_symmetry(self, detection_service):
        """Test symmetry detection."""
        test_image = np.random.random((224, 224, 3)).astype(np.float32)
        
        symmetry_type = detection_service._detect_symmetry(test_image)
        
        assert isinstance(symmetry_type, str)
        assert symmetry_type in ['radial', 'bilateral', 'horizontal', 'vertical', 'asymmetrical']
    
    def test_extract_geometric_features(self, detection_service):
        """Test geometric feature extraction."""
        test_image = np.random.random((224, 224, 3)).astype(np.float32)
        
        features = detection_service._extract_geometric_features(test_image)
        
        assert isinstance(features, dict)
        assert 'area' in features
        assert 'perimeter' in features
        assert 'aspect_ratio' in features
        assert 'compactness' in features
        assert 'circularity' in features
        assert 'convexity' in features
    
    @pytest.mark.asyncio
    async def test_analyze_image_error_handling(self, detection_service):
        """Test error handling in image analysis."""
        # Test with non-existent file
        with pytest.raises(Exception):
            await detection_service.analyze_image("non_existent_file.jpg")
    
    def test_pattern_classes(self, detection_service):
        """Test that pattern classes are properly defined."""
        expected_patterns = [
            "geometric", "floral", "traditional", "modern", "symmetrical", 
            "asymmetrical", "radial", "bilateral", "circular", "linear"
        ]
        
        for pattern in expected_patterns:
            assert pattern in detection_service.pattern_classes


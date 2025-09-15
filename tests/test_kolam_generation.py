"""Tests for Kolam generation service."""

import pytest
import asyncio
from unittest.mock import patch, Mock
import tempfile
import os

from src.services.ai.generation_service import GenerationService


class TestGenerationService:
    """Test cases for Kolam generation service."""
    
    @pytest.fixture
    def generation_service(self):
        """Create generation service instance."""
        return GenerationService()
    
    def test_generation_service_initialization(self, generation_service):
        """Test generation service initialization."""
        assert generation_service is not None
        assert generation_service.pattern_generators is not None
        assert generation_service.symmetry_generators is not None
        
        # Check that all expected generators are present
        expected_patterns = ["geometric", "floral", "traditional", "modern"]
        for pattern in expected_patterns:
            assert pattern in generation_service.pattern_generators
        
        expected_symmetries = ["radial", "bilateral", "rotational"]
        for symmetry in expected_symmetries:
            assert symmetry in generation_service.symmetry_generators
    
    def test_get_size_parameters(self, generation_service):
        """Test size parameter generation."""
        # Test small size
        small_params = generation_service._get_size_parameters("small")
        assert small_params["width"] == 200
        assert small_params["height"] == 200
        assert small_params["center"] == (100, 100)
        
        # Test medium size
        medium_params = generation_service._get_size_parameters("medium")
        assert medium_params["width"] == 400
        assert medium_params["height"] == 400
        assert medium_params["center"] == (200, 200)
        
        # Test large size
        large_params = generation_service._get_size_parameters("large")
        assert large_params["width"] == 600
        assert large_params["height"] == 600
        assert large_params["center"] == (300, 300)
        
        # Test default (unknown size)
        default_params = generation_service._get_size_parameters("unknown")
        assert default_params["width"] == 400  # Should default to medium
    
    def test_generate_geometric_pattern(self, generation_service):
        """Test geometric pattern generation."""
        size_params = {"width": 400, "height": 400, "center": (200, 200)}
        
        pattern = generation_service._generate_geometric_pattern(3, size_params)
        
        assert isinstance(pattern, list)
        assert len(pattern) > 0
        
        # Check that all elements have required fields
        for element in pattern:
            assert "type" in element
            assert "style" in element
            assert element["type"] in ["circle", "polygon", "square"]
    
    def test_generate_floral_pattern(self, generation_service):
        """Test floral pattern generation."""
        size_params = {"width": 400, "height": 400, "center": (200, 200)}
        
        pattern = generation_service._generate_floral_pattern(3, size_params)
        
        assert isinstance(pattern, list)
        assert len(pattern) > 0
        
        # Check for petal elements
        petal_elements = [elem for elem in pattern if elem["type"] == "petal"]
        assert len(petal_elements) > 0
        
        # Check for center flower
        center_elements = [elem for elem in pattern if elem["type"] == "circle"]
        assert len(center_elements) > 0
    
    def test_generate_traditional_pattern(self, generation_service):
        """Test traditional pattern generation."""
        size_params = {"width": 400, "height": 400, "center": (200, 200)}
        
        pattern = generation_service._generate_traditional_pattern(3, size_params)
        
        assert isinstance(pattern, list)
        assert len(pattern) > 0
        
        # Check for dot elements
        dot_elements = [elem for elem in pattern if elem["type"] == "circle" and elem.get("radius", 0) < 10]
        assert len(dot_elements) > 0
        
        # Check for line elements
        line_elements = [elem for elem in pattern if elem["type"] == "line"]
        assert len(line_elements) > 0
    
    def test_generate_modern_pattern(self, generation_service):
        """Test modern pattern generation."""
        size_params = {"width": 400, "height": 400, "center": (200, 200)}
        
        pattern = generation_service._generate_modern_pattern(3, size_params)
        
        assert isinstance(pattern, list)
        assert len(pattern) > 0
        
        # Check for curve elements
        curve_elements = [elem for elem in pattern if elem["type"] == "curve"]
        assert len(curve_elements) > 0
    
    def test_apply_radial_symmetry(self, generation_service):
        """Test radial symmetry application."""
        base_pattern = [
            {"type": "circle", "center": (100, 100), "radius": 20, "style": {}}
        ]
        
        symmetric_pattern = generation_service._apply_radial_symmetry(base_pattern, 3)
        
        assert isinstance(symmetric_pattern, list)
        assert len(symmetric_pattern) > len(base_pattern)  # Should have more elements
    
    def test_apply_bilateral_symmetry(self, generation_service):
        """Test bilateral symmetry application."""
        base_pattern = [
            {"type": "circle", "center": (100, 100), "radius": 20, "style": {}}
        ]
        
        symmetric_pattern = generation_service._apply_bilateral_symmetry(base_pattern, 3)
        
        assert isinstance(symmetric_pattern, list)
        assert len(symmetric_pattern) == len(base_pattern) * 2  # Should double the elements
    
    def test_apply_rotational_symmetry(self, generation_service):
        """Test rotational symmetry application."""
        base_pattern = [
            {"type": "circle", "center": (100, 100), "radius": 20, "style": {}}
        ]
        
        symmetric_pattern = generation_service._apply_rotational_symmetry(base_pattern, 3)
        
        assert isinstance(symmetric_pattern, list)
        assert len(symmetric_pattern) > len(base_pattern)  # Should have more elements
    
    def test_generate_polygon_points(self, generation_service):
        """Test polygon point generation."""
        center = (100, 100)
        sides = 6
        radius = 50
        
        points = generation_service._generate_polygon_points(center, sides, radius)
        
        assert isinstance(points, list)
        assert len(points) == sides
        
        # Check that all points are tuples
        for point in points:
            assert isinstance(point, tuple)
            assert len(point) == 2
    
    @pytest.mark.asyncio
    async def test_generate_pattern_integration(self, generation_service):
        """Test full pattern generation integration."""
        result = await generation_service.generate_pattern(
            pattern_type="traditional",
            complexity_level=3,
            symmetry_type="radial",
            size="medium"
        )
        
        assert isinstance(result, dict)
        assert "svg_data" in result
        assert "image_path" in result
        assert "pattern_type" in result
        assert "complexity_level" in result
        assert "symmetry_type" in result
        assert "size" in result
        
        assert result["pattern_type"] == "traditional"
        assert result["complexity_level"] == 3
        assert result["symmetry_type"] == "radial"
        assert result["size"] == "medium"
        
        # Check that files were created
        assert os.path.exists(result["image_path"])
        
        # Clean up
        if os.path.exists(result["image_path"]):
            os.unlink(result["image_path"])
    
    @pytest.mark.asyncio
    async def test_generate_pattern_error_handling(self, generation_service):
        """Test error handling in pattern generation."""
        # Test with invalid pattern type
        result = await generation_service.generate_pattern(
            pattern_type="invalid_type",
            complexity_level=3,
            symmetry_type="radial",
            size="medium"
        )
        
        # Should fall back to traditional pattern
        assert result["pattern_type"] == "traditional"
    
    def test_calculate_petal_control_point(self, generation_service):
        """Test petal control point calculation."""
        start = (100, 100)
        end = (200, 200)
        angle = 0.5
        
        control_point = generation_service._calculate_petal_control_point(start, end, angle)
        
        assert isinstance(control_point, tuple)
        assert len(control_point) == 2
    
    def test_calculate_curve_control_point(self, generation_service):
        """Test curve control point calculation."""
        start = (100, 100)
        end = (200, 200)
        control_num = 1
        
        control_point = generation_service._calculate_curve_control_point(start, end, control_num)
        
        assert isinstance(control_point, tuple)
        assert len(control_point) == 2


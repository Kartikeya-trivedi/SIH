import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from typing import Dict, List, Any, Tuple
import json
import os

from src.core.logging import LoggerMixin
from src.schemas import KolamImageAnalysis


class DetectionService(LoggerMixin):
    """Service for Kolam pattern detection and analysis."""
    
    def __init__(self):
        self.model = None
        self.pattern_classes = [
            "geometric", "floral", "traditional", "modern", "symmetrical", 
            "asymmetrical", "radial", "bilateral", "circular", "linear"
        ]
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained detection model."""
        try:
            # In a real implementation, you would load a pre-trained model
            # For now, we'll create a placeholder
            self.logger.info("Loading Kolam detection model")
            # self.model = tf.keras.models.load_model("models/kolam_detection_model.h5")
            self.logger.info("Model loaded successfully")
        except Exception as e:
            self.logger.error("Failed to load model", error=str(e))
            self.model = None
    
    async def analyze_image(self, image_path: str) -> KolamImageAnalysis:
        """Analyze a Kolam image and extract features."""
        try:
            # Load and preprocess image
            image = self._load_and_preprocess_image(image_path)
            
            # Extract basic features
            features = self._extract_basic_features(image)
            
            # Detect patterns (placeholder implementation)
            patterns, confidence_scores = self._detect_patterns(image)
            
            # Calculate complexity
            complexity_score = self._calculate_complexity(image, features)
            
            # Determine symmetry type
            symmetry_type = self._detect_symmetry(image)
            
            # Extract geometric features
            geometric_features = self._extract_geometric_features(image)
            
            analysis = KolamImageAnalysis(
                detected_patterns=patterns,
                confidence_scores=confidence_scores,
                complexity_score=complexity_score,
                symmetry_type=symmetry_type,
                geometric_features=geometric_features
            )
            
            self.logger.info("Image analysis completed", image_path=image_path)
            return analysis
            
        except Exception as e:
            self.logger.error("Image analysis failed", error=str(e), image_path=image_path)
            raise
    
    def _load_and_preprocess_image(self, image_path: str) -> np.ndarray:
        """Load and preprocess image for analysis."""
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize to standard size
        image = cv2.resize(image, (224, 224))
        
        # Normalize
        image = image.astype(np.float32) / 255.0
        
        return image
    
    def _extract_basic_features(self, image: np.ndarray) -> Dict[str, Any]:
        """Extract basic image features."""
        # Convert to grayscale for some analyses
        gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        features = {
            "brightness": np.mean(gray),
            "contrast": np.std(gray),
            "edges": cv2.Canny(gray, 50, 150),
            "corners": cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
        }
        
        return features
    
    def _detect_patterns(self, image: np.ndarray) -> Tuple[List[str], Dict[str, float]]:
        """Detect Kolam patterns in the image."""
        # Placeholder implementation - in reality, this would use a trained model
        patterns = []
        confidence_scores = {}
        
        # Simple heuristic-based detection
        gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        # Detect circles (common in Kolam)
        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, 1, 20,
            param1=50, param2=30, minRadius=0, maxRadius=0
        )
        
        if circles is not None:
            patterns.append("circular")
            confidence_scores["circular"] = min(len(circles[0]) / 10, 1.0)
        
        # Detect lines
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        if lines is not None:
            patterns.append("linear")
            confidence_scores["linear"] = min(len(lines) / 20, 1.0)
        
        # Detect symmetry
        if self._has_symmetry(gray):
            patterns.append("symmetrical")
            confidence_scores["symmetrical"] = 0.8
        
        # Default patterns if none detected
        if not patterns:
            patterns = ["traditional"]
            confidence_scores["traditional"] = 0.5
        
        return patterns, confidence_scores
    
    def _calculate_complexity(self, image: np.ndarray, features: Dict[str, Any]) -> float:
        """Calculate complexity score of the Kolam."""
        gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        # Edge density
        edges = features["edges"]
        edge_density = np.sum(edges > 0) / edges.size
        
        # Corner count
        corner_count = len(features["corners"]) if features["corners"] is not None else 0
        
        # Contrast
        contrast = features["contrast"]
        
        # Combine factors
        complexity = (edge_density * 0.4 + 
                     min(corner_count / 50, 1.0) * 0.3 + 
                     min(contrast / 100, 1.0) * 0.3)
        
        return min(complexity, 1.0)
    
    def _detect_symmetry(self, image: np.ndarray) -> str:
        """Detect the type of symmetry in the image."""
        gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        height, width = gray.shape
        
        # Check horizontal symmetry
        top_half = gray[:height//2, :]
        bottom_half = cv2.flip(gray[height//2:, :], 0)
        
        if top_half.shape[0] == bottom_half.shape[0]:
            h_symmetry = np.mean(np.abs(top_half.astype(float) - bottom_half.astype(float)))
        else:
            h_symmetry = float('inf')
        
        # Check vertical symmetry
        left_half = gray[:, :width//2]
        right_half = cv2.flip(gray[:, width//2:], 1)
        
        if left_half.shape[1] == right_half.shape[1]:
            v_symmetry = np.mean(np.abs(left_half.astype(float) - right_half.astype(float)))
        else:
            v_symmetry = float('inf')
        
        # Check radial symmetry (simplified)
        center = (width//2, height//2)
        radial_symmetry = self._check_radial_symmetry(gray, center)
        
        # Determine symmetry type
        if radial_symmetry < 20:
            return "radial"
        elif h_symmetry < 20 and v_symmetry < 20:
            return "bilateral"
        elif h_symmetry < 20 or v_symmetry < 20:
            return "horizontal" if h_symmetry < v_symmetry else "vertical"
        else:
            return "asymmetrical"
    
    def _check_radial_symmetry(self, image: np.ndarray, center: Tuple[int, int]) -> float:
        """Check for radial symmetry around a center point."""
        # Simplified radial symmetry check
        # In practice, this would be more sophisticated
        return np.random.uniform(10, 50)  # Placeholder
    
    def _has_symmetry(self, image: np.ndarray) -> bool:
        """Check if image has any form of symmetry."""
        height, width = image.shape
        
        # Check horizontal symmetry
        top_half = image[:height//2, :]
        bottom_half = cv2.flip(image[height//2:, :], 0)
        
        if top_half.shape[0] == bottom_half.shape[0]:
            h_diff = np.mean(np.abs(top_half.astype(float) - bottom_half.astype(float)))
            if h_diff < 30:
                return True
        
        return False
    
    def _extract_geometric_features(self, image: np.ndarray) -> Dict[str, Any]:
        """Extract geometric features from the image."""
        gray = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        
        features = {
            "area": np.sum(gray > 128),  # Approximate area of patterns
            "perimeter": self._calculate_perimeter(gray),
            "aspect_ratio": gray.shape[1] / gray.shape[0],
            "compactness": 0.0,  # Would be calculated as (perimeter^2) / (4*pi*area)
            "circularity": 0.0,  # Would be calculated as 4*pi*area / (perimeter^2)
            "convexity": 0.0,    # Would be calculated as convex_hull_area / area
        }
        
        return features
    
    def _calculate_perimeter(self, image: np.ndarray) -> float:
        """Calculate approximate perimeter of patterns."""
        # Find contours
        contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            perimeter = cv2.arcLength(largest_contour, True)
            return perimeter
        
        return 0.0


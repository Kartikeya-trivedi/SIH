import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import svgwrite
import os
from typing import Dict, List, Tuple, Any
import random
import math

from src.core.logging import LoggerMixin


class GenerationService(LoggerMixin):
    """Service for generating Kolam patterns using mathematical rules."""
    
    def __init__(self):
        self.pattern_generators = {
            "geometric": self._generate_geometric_pattern,
            "floral": self._generate_floral_pattern,
            "traditional": self._generate_traditional_pattern,
            "modern": self._generate_modern_pattern
        }
        
        self.symmetry_generators = {
            "radial": self._apply_radial_symmetry,
            "bilateral": self._apply_bilateral_symmetry,
            "rotational": self._apply_rotational_symmetry
        }
    
    async def generate_pattern(
        self,
        pattern_type: str,
        complexity_level: int,
        symmetry_type: str,
        size: str = "medium"
    ) -> Dict[str, Any]:
        """Generate a Kolam pattern with specified parameters."""
        try:
            self.logger.info(
                "Generating Kolam pattern",
                pattern_type=pattern_type,
                complexity_level=complexity_level,
                symmetry_type=symmetry_type,
                size=size
            )
            
            # Get size parameters
            size_params = self._get_size_parameters(size)
            
            # Generate base pattern
            if pattern_type in self.pattern_generators:
                base_pattern = self.pattern_generators[pattern_type](
                    complexity_level, size_params
                )
            else:
                base_pattern = self.pattern_generators["traditional"](
                    complexity_level, size_params
                )
            
            # Apply symmetry
            if symmetry_type in self.symmetry_generators:
                final_pattern = self.symmetry_generators[symmetry_type](
                    base_pattern, complexity_level
                )
            else:
                final_pattern = base_pattern
            
            # Generate SVG
            svg_data = self._generate_svg(final_pattern, size_params)
            
            # Generate image
            image_path = self._generate_image(final_pattern, size_params)
            
            result = {
                "svg_data": svg_data,
                "image_path": image_path,
                "pattern_type": pattern_type,
                "complexity_level": complexity_level,
                "symmetry_type": symmetry_type,
                "size": size
            }
            
            self.logger.info("Kolam pattern generated successfully")
            return result
            
        except Exception as e:
            self.logger.error("Pattern generation failed", error=str(e))
            raise
    
    def _get_size_parameters(self, size: str) -> Dict[str, int]:
        """Get size parameters based on size specification."""
        size_map = {
            "small": {"width": 200, "height": 200, "center": (100, 100)},
            "medium": {"width": 400, "height": 400, "center": (200, 200)},
            "large": {"width": 600, "height": 600, "center": (300, 300)}
        }
        return size_map.get(size, size_map["medium"])
    
    def _generate_geometric_pattern(
        self, 
        complexity_level: int, 
        size_params: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Generate geometric Kolam patterns."""
        patterns = []
        center = size_params["center"]
        max_radius = min(size_params["width"], size_params["height"]) // 2 - 20
        
        # Generate concentric circles
        num_circles = min(complexity_level + 2, 8)
        for i in range(num_circles):
            radius = (max_radius * (i + 1)) // num_circles
            patterns.append({
                "type": "circle",
                "center": center,
                "radius": radius,
                "style": {"stroke": "black", "stroke_width": 2, "fill": "none"}
            })
        
        # Generate geometric shapes
        num_shapes = min(complexity_level * 2, 12)
        for i in range(num_shapes):
            angle = (2 * math.pi * i) / num_shapes
            x = center[0] + (max_radius * 0.7) * math.cos(angle)
            y = center[1] + (max_radius * 0.7) * math.sin(angle)
            
            # Generate different shapes based on complexity
            if complexity_level >= 5:
                patterns.append({
                    "type": "polygon",
                    "points": self._generate_polygon_points((x, y), 6, 15),
                    "style": {"stroke": "black", "stroke_width": 2, "fill": "none"}
                })
            else:
                patterns.append({
                    "type": "square",
                    "center": (x, y),
                    "size": 20,
                    "style": {"stroke": "black", "stroke_width": 2, "fill": "none"}
                })
        
        return patterns
    
    def _generate_floral_pattern(
        self, 
        complexity_level: int, 
        size_params: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Generate floral Kolam patterns."""
        patterns = []
        center = size_params["center"]
        max_radius = min(size_params["width"], size_params["height"]) // 2 - 20
        
        # Generate petals
        num_petals = min(complexity_level + 4, 12)
        petal_length = max_radius * 0.6
        
        for i in range(num_petals):
            angle = (2 * math.pi * i) / num_petals
            start_x = center[0] + 20 * math.cos(angle)
            start_y = center[1] + 20 * math.sin(angle)
            end_x = center[0] + petal_length * math.cos(angle)
            end_y = center[1] + petal_length * math.sin(angle)
            
            patterns.append({
                "type": "petal",
                "start": (start_x, start_y),
                "end": (end_x, end_y),
                "control": self._calculate_petal_control_point(
                    (start_x, start_y), (end_x, end_y), angle
                ),
                "style": {"stroke": "black", "stroke_width": 2, "fill": "none"}
            })
        
        # Add center flower
        patterns.append({
            "type": "circle",
            "center": center,
            "radius": 15,
            "style": {"stroke": "black", "stroke_width": 2, "fill": "black"}
        })
        
        return patterns
    
    def _generate_traditional_pattern(
        self, 
        complexity_level: int, 
        size_params: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Generate traditional Kolam patterns."""
        patterns = []
        center = size_params["center"]
        max_radius = min(size_params["width"], size_params["height"]) // 2 - 20
        
        # Generate traditional dot grid
        dot_spacing = max(20 - complexity_level, 8)
        dots = []
        
        for x in range(center[0] - max_radius, center[0] + max_radius, dot_spacing):
            for y in range(center[1] - max_radius, center[1] + max_radius, dot_spacing):
                if math.sqrt((x - center[0])**2 + (y - center[1])**2) <= max_radius:
                    dots.append((x, y))
        
        # Connect dots with lines
        for i, dot in enumerate(dots):
            if i < len(dots) - 1:
                next_dot = dots[i + 1]
                patterns.append({
                    "type": "line",
                    "start": dot,
                    "end": next_dot,
                    "style": {"stroke": "black", "stroke_width": 2}
                })
        
        # Add dots
        for dot in dots:
            patterns.append({
                "type": "circle",
                "center": dot,
                "radius": 3,
                "style": {"fill": "black"}
            })
        
        return patterns
    
    def _generate_modern_pattern(
        self, 
        complexity_level: int, 
        size_params: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Generate modern Kolam patterns."""
        patterns = []
        center = size_params["center"]
        max_radius = min(size_params["width"], size_params["height"]) // 2 - 20
        
        # Generate abstract curves
        num_curves = min(complexity_level + 3, 10)
        
        for i in range(num_curves):
            angle = (2 * math.pi * i) / num_curves
            start_radius = random.uniform(20, max_radius * 0.5)
            end_radius = random.uniform(max_radius * 0.5, max_radius)
            
            start_x = center[0] + start_radius * math.cos(angle)
            start_y = center[1] + start_radius * math.sin(angle)
            end_x = center[0] + end_radius * math.cos(angle + math.pi/4)
            end_y = center[1] + end_radius * math.sin(angle + math.pi/4)
            
            patterns.append({
                "type": "curve",
                "start": (start_x, start_y),
                "end": (end_x, end_y),
                "control1": self._calculate_curve_control_point(
                    (start_x, start_y), (end_x, end_y), 1
                ),
                "control2": self._calculate_curve_control_point(
                    (start_x, start_y), (end_x, end_y), 2
                ),
                "style": {"stroke": "black", "stroke_width": 2, "fill": "none"}
            })
        
        return patterns
    
    def _apply_radial_symmetry(
        self, 
        pattern: List[Dict[str, Any]], 
        complexity_level: int
    ) -> List[Dict[str, Any]]:
        """Apply radial symmetry to the pattern."""
        symmetric_pattern = []
        
        # Create multiple copies rotated around center
        num_rotations = min(complexity_level + 2, 8)
        
        for rotation in range(num_rotations):
            angle = (2 * math.pi * rotation) / num_rotations
            
            for element in pattern:
                symmetric_element = self._rotate_element(element, angle)
                symmetric_pattern.append(symmetric_element)
        
        return symmetric_pattern
    
    def _apply_bilateral_symmetry(
        self, 
        pattern: List[Dict[str, Any]], 
        complexity_level: int
    ) -> List[Dict[str, Any]]:
        """Apply bilateral symmetry to the pattern."""
        symmetric_pattern = pattern.copy()
        
        # Mirror the pattern
        for element in pattern:
            mirrored_element = self._mirror_element(element)
            symmetric_pattern.append(mirrored_element)
        
        return symmetric_pattern
    
    def _apply_rotational_symmetry(
        self, 
        pattern: List[Dict[str, Any]], 
        complexity_level: int
    ) -> List[Dict[str, Any]]:
        """Apply rotational symmetry to the pattern."""
        symmetric_pattern = pattern.copy()
        
        # Create rotated copies
        num_rotations = min(complexity_level + 1, 6)
        
        for rotation in range(1, num_rotations):
            angle = (2 * math.pi * rotation) / num_rotations
            
            for element in pattern:
                rotated_element = self._rotate_element(element, angle)
                symmetric_pattern.append(rotated_element)
        
        return symmetric_pattern
    
    def _generate_svg(self, pattern: List[Dict[str, Any]], size_params: Dict[str, int]) -> str:
        """Generate SVG representation of the pattern."""
        dwg = svgwrite.Drawing(
            size=(size_params["width"], size_params["height"]),
            viewBox=f"0 0 {size_params['width']} {size_params['height']}"
        )
        
        for element in pattern:
            if element["type"] == "circle":
                dwg.add(dwg.circle(
                    center=element["center"],
                    r=element["radius"],
                    **element["style"]
                ))
            elif element["type"] == "line":
                dwg.add(dwg.line(
                    start=element["start"],
                    end=element["end"],
                    **element["style"]
                ))
            elif element["type"] == "polygon":
                dwg.add(dwg.polygon(
                    points=element["points"],
                    **element["style"]
                ))
            # Add more element types as needed
        
        return dwg.tostring()
    
    def _generate_image(self, pattern: List[Dict[str, Any]], size_params: Dict[str, int]) -> str:
        """Generate PNG image of the pattern."""
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, size_params["width"])
        ax.set_ylim(0, size_params["height"])
        ax.set_aspect('equal')
        ax.axis('off')
        
        for element in pattern:
            if element["type"] == "circle":
                circle = patches.Circle(
                    element["center"], 
                    element["radius"],
                    **element["style"]
                )
                ax.add_patch(circle)
            elif element["type"] == "line":
                ax.plot(
                    [element["start"][0], element["end"][0]],
                    [element["start"][1], element["end"][1]],
                    **element["style"]
                )
            # Add more element types as needed
        
        # Save image
        os.makedirs("generated_images", exist_ok=True)
        image_path = f"generated_images/kolam_{random.randint(1000, 9999)}.png"
        plt.savefig(image_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return image_path
    
    # Helper methods
    def _generate_polygon_points(self, center: Tuple[float, float], sides: int, radius: float) -> List[Tuple[float, float]]:
        """Generate points for a regular polygon."""
        points = []
        for i in range(sides):
            angle = (2 * math.pi * i) / sides
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def _calculate_petal_control_point(self, start: Tuple[float, float], end: Tuple[float, float], angle: float) -> Tuple[float, float]:
        """Calculate control point for petal curve."""
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        offset = 30
        control_x = mid_x + offset * math.cos(angle + math.pi/2)
        control_y = mid_y + offset * math.sin(angle + math.pi/2)
        return (control_x, control_y)
    
    def _calculate_curve_control_point(self, start: Tuple[float, float], end: Tuple[float, float], control_num: int) -> Tuple[float, float]:
        """Calculate control point for curve."""
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        offset = 50 if control_num == 1 else -50
        control_x = mid_x + offset
        control_y = mid_y + offset
        return (control_x, control_y)
    
    def _rotate_element(self, element: Dict[str, Any], angle: float) -> Dict[str, Any]:
        """Rotate an element around the center."""
        # Simplified rotation - in practice, this would be more sophisticated
        rotated_element = element.copy()
        # Add rotation logic here
        return rotated_element
    
    def _mirror_element(self, element: Dict[str, Any]) -> Dict[str, Any]:
        """Mirror an element across a line."""
        # Simplified mirroring - in practice, this would be more sophisticated
        mirrored_element = element.copy()
        # Add mirroring logic here
        return mirrored_element


#!/usr/bin/env python3
"""Sample script to generate a Kolam pattern."""

import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.services.ai.generation_service import GenerationService


async def main():
    """Generate a sample Kolam pattern."""
    print("🎨 Generating sample Kolam pattern...")
    
    generation_service = GenerationService()
    
    try:
        # Generate a traditional Kolam pattern
        result = await generation_service.generate_pattern(
            pattern_type="traditional",
            complexity_level=3,
            symmetry_type="radial",
            size="medium"
        )
        
        print(f"✅ Pattern generated successfully!")
        print(f"📁 Image saved to: {result['image_path']}")
        print(f"🎯 Pattern type: {result['pattern_type']}")
        print(f"📊 Complexity level: {result['complexity_level']}")
        print(f"🔄 Symmetry type: {result['symmetry_type']}")
        
        # Save SVG to file
        svg_path = "sample_kolam.svg"
        with open(svg_path, "w") as f:
            f.write(result["svg_data"])
        print(f"📄 SVG saved to: {svg_path}")
        
    except Exception as e:
        print(f"❌ Error generating pattern: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)


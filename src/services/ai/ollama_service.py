import httpx
import json
from typing import Dict, List, Any, Optional
import asyncio

from src.core.config import settings
from src.core.logging import LoggerMixin


class OllamaService(LoggerMixin):
    """Service for interacting with Ollama for AI-powered explanations and hints."""
    
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def generate_explanation(
        self,
        question: str,
        correct_answer: str,
        user_answer: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """Generate an explanation for a trivia question."""
        try:
            prompt = self._build_explanation_prompt(
                question, correct_answer, user_answer, context
            )
            
            response = await self._call_ollama(prompt)
            
            self.logger.info("Explanation generated successfully")
            return response
            
        except Exception as e:
            self.logger.error("Failed to generate explanation", error=str(e))
            return "I apologize, but I couldn't generate an explanation at this time. Please try again later."
    
    async def generate_hint(
        self,
        question: str,
        difficulty_level: int,
        category: Optional[str] = None
    ) -> str:
        """Generate a hint for a trivia question."""
        try:
            prompt = self._build_hint_prompt(question, difficulty_level, category)
            
            response = await self._call_ollama(prompt)
            
            self.logger.info("Hint generated successfully")
            return response
            
        except Exception as e:
            self.logger.error("Failed to generate hint", error=str(e))
            return "I apologize, but I couldn't generate a hint at this time. Please try again later."
    
    async def analyze_kolam_pattern(
        self,
        pattern_description: str,
        detected_features: Dict[str, Any]
    ) -> str:
        """Generate an analysis of a Kolam pattern."""
        try:
            prompt = self._build_pattern_analysis_prompt(pattern_description, detected_features)
            
            response = await self._call_ollama(prompt)
            
            self.logger.info("Pattern analysis generated successfully")
            return response
            
        except Exception as e:
            self.logger.error("Failed to generate pattern analysis", error=str(e))
            return "I apologize, but I couldn't analyze this pattern at this time. Please try again later."
    
    async def generate_learning_tip(
        self,
        topic: str,
        user_level: int,
        previous_topics: Optional[List[str]] = None
    ) -> str:
        """Generate a learning tip for a specific topic."""
        try:
            prompt = self._build_learning_tip_prompt(topic, user_level, previous_topics)
            
            response = await self._call_ollama(prompt)
            
            self.logger.info("Learning tip generated successfully")
            return response
            
        except Exception as e:
            self.logger.error("Failed to generate learning tip", error=str(e))
            return "I apologize, but I couldn't generate a learning tip at this time. Please try again later."
    
    async def _call_ollama(self, prompt: str) -> str:
        """Make a call to Ollama API."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                self.logger.error("Ollama API error", status_code=response.status_code)
                return "I apologize, but I couldn't process your request at this time."
                
        except httpx.TimeoutException:
            self.logger.error("Ollama API timeout")
            return "I apologize, but the request timed out. Please try again later."
        except Exception as e:
            self.logger.error("Ollama API call failed", error=str(e))
            return "I apologize, but I couldn't process your request at this time."
    
    def _build_explanation_prompt(
        self,
        question: str,
        correct_answer: str,
        user_answer: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """Build prompt for generating explanations."""
        prompt = f"""You are an expert teacher explaining Kolam (traditional Indian art) concepts. 

Question: {question}
Correct Answer: {correct_answer}"""

        if user_answer:
            prompt += f"\nUser's Answer: {user_answer}"
        
        if context:
            prompt += f"\nContext: {context}"
        
        prompt += """

Please provide a clear, educational explanation that:
1. Explains why the correct answer is right
2. Provides cultural and historical context about Kolam
3. Includes interesting facts or details
4. Is appropriate for learners of all levels
5. Keeps the explanation concise but informative

Explanation:"""
        
        return prompt
    
    def _build_hint_prompt(
        self,
        question: str,
        difficulty_level: int,
        category: Optional[str] = None
    ) -> str:
        """Build prompt for generating hints."""
        prompt = f"""You are a helpful tutor providing hints for Kolam learning questions.

Question: {question}
Difficulty Level: {difficulty_level}/5"""

        if category:
            prompt += f"\nCategory: {category}"
        
        prompt += """

Please provide a helpful hint that:
1. Guides the learner toward the correct answer without giving it away
2. Is appropriate for the difficulty level
3. Includes relevant Kolam cultural context
4. Encourages further learning
5. Is encouraging and supportive

Hint:"""
        
        return prompt
    
    def _build_pattern_analysis_prompt(
        self,
        pattern_description: str,
        detected_features: Dict[str, Any]
    ) -> str:
        """Build prompt for analyzing Kolam patterns."""
        prompt = f"""You are an expert in traditional Indian Kolam art analyzing a pattern.

Pattern Description: {pattern_description}
Detected Features: {json.dumps(detected_features, indent=2)}

Please provide an analysis that includes:
1. Pattern type and style classification
2. Cultural significance and traditional meaning
3. Geometric and artistic elements
4. Difficulty level assessment
5. Suggestions for learning or creating similar patterns
6. Historical or regional context if applicable

Analysis:"""
        
        return prompt
    
    def _build_learning_tip_prompt(
        self,
        topic: str,
        user_level: int,
        previous_topics: Optional[List[str]] = None
    ) -> str:
        """Build prompt for generating learning tips."""
        prompt = f"""You are a Kolam art instructor providing personalized learning tips.

Current Topic: {topic}
User Level: {user_level}/5"""

        if previous_topics:
            prompt += f"\nPrevious Topics Covered: {', '.join(previous_topics)}"
        
        prompt += """

Please provide a learning tip that:
1. Is tailored to the user's level
2. Connects to previous learning if applicable
3. Provides practical advice for learning Kolam
4. Includes cultural context
5. Encourages practice and exploration
6. Is motivating and supportive

Learning Tip:"""
        
        return prompt
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


class AILearningAssistant(LoggerMixin):
    """AI-powered learning assistant using Ollama."""
    
    def __init__(self):
        self.ollama_service = OllamaService()
    
    async def get_question_explanation(
        self,
        question_id: int,
        question_data: Dict[str, Any],
        user_answer: Optional[str] = None
    ) -> str:
        """Get explanation for a trivia question."""
        return await self.ollama_service.generate_explanation(
            question=question_data["question_text"],
            correct_answer=question_data["correct_answer"],
            user_answer=user_answer,
            context=question_data.get("explanation")
        )
    
    async def get_question_hint(
        self,
        question_data: Dict[str, Any]
    ) -> str:
        """Get hint for a trivia question."""
        return await self.ollama_service.generate_hint(
            question=question_data["question_text"],
            difficulty_level=question_data["difficulty_level"],
            category=question_data.get("category")
        )
    
    async def analyze_user_kolam(
        self,
        kolam_data: Dict[str, Any]
    ) -> str:
        """Analyze user's Kolam pattern."""
        pattern_description = f"Kolam pattern with {kolam_data.get('detected_patterns', [])} patterns"
        
        detected_features = {
            "patterns": kolam_data.get("detected_patterns", []),
            "symmetry": kolam_data.get("symmetry_type"),
            "complexity": kolam_data.get("complexity_score"),
            "geometric_features": kolam_data.get("geometric_features", {})
        }
        
        return await self.ollama_service.analyze_kolam_pattern(
            pattern_description, detected_features
        )
    
    async def get_personalized_tip(
        self,
        topic: str,
        user_level: int,
        learning_history: Optional[List[str]] = None
    ) -> str:
        """Get personalized learning tip."""
        return await self.ollama_service.generate_learning_tip(
            topic=topic,
            user_level=user_level,
            previous_topics=learning_history
        )
    
    async def close(self):
        """Close the AI service."""
        await self.ollama_service.close()


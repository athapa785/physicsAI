"""
Physics lesson generation service with multi-LLM support.
"""

import os
from dotenv import load_dotenv
import json
import logging
import asyncio
from typing import List, Dict, Tuple
from backend.services.lesson_storage import LessonStorage
from backend.services.multi_llm_service import MultiLLMService, LLMProvider, LLMModel
from backend.services.rag_service import PhysicsRAG

# Load environment variables
load_dotenv()

class PhysicsService:
    def __init__(self):
        try:
            # Initialize multi-LLM service
            self.llm_service = MultiLLMService()
            self.book_structure = None
            # Initialize lesson storage
            self.lesson_storage = LessonStorage()
            # Initialize RAG service
            self.rag_service = PhysicsRAG()
        except Exception as e:
            raise ValueError(f"Failed to initialize service: {str(e)}")
        
    def load_book_structure(self) -> Dict:
        """Load the book structure from the physics content directory."""
        if not hasattr(self, 'book_structure') or self.book_structure is None:
            chapters = []
            chapter_mapping = {
                'mechanics': {'number': 1, 'title': 'Mechanics'},
                'thermodynamics': {'number': 2, 'title': 'Thermodynamics'},
                'waves_oscillations': {'number': 3, 'title': 'Waves and Oscillations'},
                'electromagnetism': {'number': 4, 'title': 'Electromagnetism'},
                'optics': {'number': 5, 'title': 'Optics'},
                'modern_physics': {'number': 6, 'title': 'Modern Physics'}
            }
            
            content_dir = os.path.join(os.path.dirname(__file__), "..", "data", "physics_content")
            
            # Get chapters from directory structure
            if os.path.exists(content_dir):
                for chapter_dir in sorted(os.listdir(content_dir)):
                    if os.path.isdir(os.path.join(content_dir, chapter_dir)) and chapter_dir in chapter_mapping:
                        chapter_info = chapter_mapping[chapter_dir]
                        topics = []
                        
                        # Get topics from files in chapter directory
                        for file in os.listdir(os.path.join(content_dir, chapter_dir)):
                            if file.endswith('.txt'):
                                topic_name = ' '.join(file.replace('.txt', '').split('_')).title()
                                topics.append(topic_name)
                        
                        chapters.append({
                            'number': chapter_info['number'],
                            'title': chapter_info['title'],
                            'topics': sorted(topics)
                        })
            
            # If no chapters found from files, use default structure
            if not chapters:
                chapters = [
                    {
                        'number': 1,
                        'title': 'Mechanics',
                        'topics': ['Kinematics', 'Newton\'s Laws', 'Work and Energy', 'Momentum', 'Rotational Motion']
                    },
                    {
                        'number': 2,
                        'title': 'Thermodynamics',
                        'topics': ['Temperature and Heat', 'First Law of Thermodynamics', 'Second Law of Thermodynamics', 'Entropy']
                    },
                    {
                        'number': 3,
                        'title': 'Waves and Oscillations',
                        'topics': ['Simple Harmonic Motion', 'Wave Properties', 'Sound Waves', 'Standing Waves']
                    },
                    {
                        'number': 4,
                        'title': 'Electromagnetism',
                        'topics': ['Electric Fields', 'Electric Potential', 'Magnetic Fields', 'Electromagnetic Induction']
                    }
                ]
                
            self.book_structure = {'chapters': sorted(chapters, key=lambda x: x['number'])}
        
        return self.book_structure
    
    def get_chapters(self) -> List[Dict]:
        """Get all chapters from the book."""
        structure = self.load_book_structure()
        return structure['chapters']
    
    def get_topics(self, chapter_number: int) -> List[str]:
        """Get topics for a specific chapter."""
        structure = self.load_book_structure()
        for chapter in structure['chapters']:
            if chapter['number'] == chapter_number:
                return chapter['topics']
        return []
    
    async def generate_lesson(self, topic: str) -> str:
        """Generate a physics lesson for a specific topic.
        
        First checks if the lesson is already stored, and if not, generates a new one.
        
        Args:
            topic: The topic to generate a lesson for
            
        Returns:
            The lesson content
        """
        # Check if we already have this lesson stored
        cached_lesson = await self.lesson_storage.get_lesson(topic)
        if cached_lesson:
            logging.info(f"Using cached lesson for topic: {topic}")
            return cached_lesson
        
        # Generate a new lesson
        logging.info(f"Generating new lesson for topic: {topic}")
        prompt = f"""Create a comprehensive physics lesson about {topic}. 
        
        IMPORTANT: DO NOT include a title or top-level header at the beginning of the lesson. Start directly with:
        
        ## Introduction
        [Introduction content here]
        
        ## Key Concepts and Principles
        [Key concepts content here]
        
        Then include the following sections:
        1. Important formulas with LaTeX formatting (use $ for inline and $$ for display equations)
        2. Real-world applications
        3. Example problems with solutions
        
        Format the content with clear section headers (using ## for sections) and organize it in a logical progression.
        """
        
        try:
            # Save current provider and model to restore later
            original_provider = self.llm_service.active_provider
            original_model = self.llm_service.active_model
            
            # Set to use OpenAI with GPT-4.5-preview specifically for lesson generation
            self.llm_service.set_active_provider(LLMProvider.OPENAI)
            self.llm_service.set_active_model(LLMModel.GPT45_PREVIEW)
            
            system_prompt = """You are a knowledgeable physics professor creating educational content for first-year undergraduate students. 
            Your content should be:
            1. Clear and accessible while maintaining academic rigor
            2. Well-structured for easy breakdown into slides
            3. Thorough in explanations without assuming prior knowledge
            4. Rich with visual descriptions that help students form mental models
            5. Precise with mathematical formulas using proper LaTeX notation
            
            Remember that this content will be used as lesson material that students will read, not as interactive content."""
            
            lesson = await self.llm_service.generate_text(prompt, system_prompt, temperature=0.7)
            
            # Restore original provider and model
            self.llm_service.set_active_provider(original_provider)
            self.llm_service.set_active_model(original_model)
            
            # Store the generated lesson for future use
            await self.lesson_storage.store_lesson(topic, lesson)
            return lesson
        except Exception as e:
            logging.error(f"Error generating lesson: {str(e)}")
            return f"I'm sorry, I encountered an error while generating the lesson for {topic}. Please try again later."
            
    async def answer_question(self, question: str, topic: str, chat_history: List[Tuple[str, str]], provider=None, model=None) -> str:
        """Answer a question about a specific topic.
        
        Args:
            question: The question to answer
            topic: The topic the question is about
            chat_history: Previous conversation history
            provider: Optional LLM provider to use
            model: Optional LLM model to use
            
        Returns:
            The answer to the question
        """
        try:
            # First try to use RAG-based answering for better context
            try:
                # Use the RAG service to get a context-aware answer
                return await self.rag_service.answer_question(question, topic, chat_history, provider, model)
            except Exception as rag_error:
                logging.warning(f"RAG-based answering failed, falling back to standard LLM: {str(rag_error)}")
                
                # Fall back to standard LLM if RAG fails
                prompt = f"""Answer this physics question about {topic}: {question}
                
                Provide a clear and educational explanation, using LaTeX for any mathematical formulas.
                """
                
                system_prompt = "You are a knowledgeable physics professor helping a student understand concepts."
                
                # If provider and model are specified, temporarily set them as active
                original_provider = None
                original_model = None
                
                if provider and model:
                    original_provider = self.llm_service.active_provider
                    original_model = self.llm_service.active_model
                    self.llm_service.set_active_provider(provider)
                    self.llm_service.set_active_model(model)
                
                # Generate the answer
                answer = await self.llm_service.generate_text(prompt, system_prompt, temperature=0.7)
                
                # Restore original provider and model if they were changed
                if original_provider and original_model:
                    self.llm_service.set_active_provider(original_provider)
                    self.llm_service.set_active_model(original_model)
                    
                return answer
        except Exception as e:
            logging.error(f"Error answering question: {str(e)}")
            return f"I'm sorry, I encountered an error while answering your question. Please try again later."
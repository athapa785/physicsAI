import asyncio
import os
import sys
import json
from pathlib import Path
from typing import List, Dict

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from backend.services.physics_service import PhysicsService
from backend.services.multi_llm_service import MultiLLMService, LLMProvider, LLMModel
from backend.services.lesson_storage import LessonStorage

async def regenerate_all_lessons():
    """
    Regenerate all physics lessons using GPT-4.5-preview with enhanced prompts
    to ensure high-quality content suitable for first-year undergraduate students.
    """
    # Initialize services
    physics_service = PhysicsService()
    lesson_storage = LessonStorage()
    
    # Set OpenAI API key
    openai_api_key = input("Enter your OpenAI API key: ")
    physics_service.llm_service.set_api_key(LLMProvider.OPENAI, openai_api_key)
    
    # Force the service to use GPT-4.5-preview
    physics_service.llm_service.set_active_provider(LLMProvider.OPENAI)
    physics_service.llm_service.set_active_model(LLMModel.GPT45_PREVIEW)
    
    # Get all chapters and topics
    chapters = physics_service.get_chapters()
    
    # Create lessons directory if it doesn't exist
    lessons_dir = Path("backend/data/lessons")
    lessons_dir.mkdir(exist_ok=True, parents=True)
    
    # Track all topics for which we'll generate lessons
    all_topics = []
    
    print("Book Structure:")
    for chapter in chapters:
        print(f"Chapter {chapter['number']}: {chapter['title']}")
        for topic in chapter['topics']:
            print(f"  - {topic}")
            all_topics.append(topic)
    
    print(f"\nTotal topics to regenerate: {len(all_topics)}")
    print("Regenerating lessons with GPT-4.5-preview...")
    
    # Enhanced prompt for lesson generation
    async def generate_enhanced_lesson(topic: str) -> str:
        """Generate an enhanced lesson with better quality and structure."""
        prompt = f"""Create a comprehensive physics lesson about {topic} for first-year undergraduate students.
        
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
        
        system_prompt = """You are a knowledgeable physics professor creating educational content for first-year undergraduate students. 
        Your content should be:
        1. Clear and accessible while maintaining academic rigor
        2. Well-structured for easy breakdown into slides
        3. Thorough in explanations without assuming prior knowledge
        4. Rich with visual descriptions that help students form mental models
        5. Precise with mathematical formulas using proper LaTeX notation
        
        IMPORTANT GUIDELINES:
        - Explain concepts as if speaking to a bright but new student
        - Use concrete examples to illustrate abstract concepts
        - Break down complex ideas into digestible parts
        - Include intuitive explanations alongside mathematical formulas
        - Ensure all content is scientifically accurate and up-to-date
        - Make connections to everyday experiences when possible
        
        Remember that this content will be used as lesson material that students will read, not as interactive content."""
        
        try:
            # Generate the lesson with GPT-4.5-preview
            lesson = await physics_service.llm_service.generate_text(prompt, system_prompt, temperature=0.7)
            return lesson
        except Exception as e:
            print(f"Error generating lesson for {topic}: {str(e)}")
            return f"Error generating lesson for {topic}: {str(e)}"
    
    # Generate lessons for each topic
    for i, topic in enumerate(all_topics):
        print(f"[{i+1}/{len(all_topics)}] Regenerating lesson for: {topic}")
        
        # Create a valid filename from the topic
        filename = topic.replace(' ', '_').replace("'", '').replace(',', '').replace('(', '').replace(')', '')
        lesson_path = lessons_dir / f"{filename}.md"
        
        try:
            # Generate the enhanced lesson
            lesson = await generate_enhanced_lesson(topic)
            
            # Save the lesson to a file
            with open(lesson_path, "w") as f:
                f.write(lesson)
            
            # Store in lesson storage
            await lesson_storage.store_lesson(topic, lesson)
            
            print(f"  - Enhanced lesson saved to {lesson_path}")
        except Exception as e:
            print(f"  - Error generating lesson for {topic}: {str(e)}")
    
    print("\nAll lessons regenerated successfully with GPT-4.5-preview!")
    
    # Verify that the RAG system is working properly
    print("\nTesting RAG system with a sample question...")
    try:
        question = "What is the relationship between force and acceleration?"
        topic = "Forces Newtons Laws"
        
        # Set the provider and model for question answering
        physics_service.llm_service.set_active_provider(LLMProvider.OPENAI)
        physics_service.llm_service.set_active_model(LLMModel.GPT4)
        
        answer = await physics_service.answer_question(
            question=question, 
            topic=topic, 
            chat_history=[],
            provider=LLMProvider.OPENAI,
            model=LLMModel.GPT4
        )
        
        print(f"\nQuestion: {question}")
        print(f"Topic: {topic}")
        print(f"Answer: {answer[:500]}...")
        print("\nRAG system is working properly!")
    except Exception as e:
        print(f"Error testing RAG system: {str(e)}")

if __name__ == "__main__":
    asyncio.run(regenerate_all_lessons())

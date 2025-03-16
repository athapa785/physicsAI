import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.services.physics_service import PhysicsService
from backend.services.multi_llm_service import MultiLLMService, LLMProvider, LLMModel

async def generate_work_energy_lesson():
    # Initialize services
    physics_service = PhysicsService()
    
    # Set OpenAI API key (you'll need to enter this when prompted)
    openai_api_key = input("Enter your OpenAI API key: ")
    physics_service.llm_service.set_api_key(LLMProvider.OPENAI, openai_api_key)
    
    # Generate a lesson on Work and Energy
    topic = "Work and Energy"
    print(f"Generating lesson on {topic}...")
    lesson = await physics_service.generate_lesson(topic)
    
    # Save the lesson to a file
    lesson_path = Path("backend/data/lessons/Work_Energy.md")
    with open(lesson_path, "w") as f:
        f.write(lesson)
    
    print(f"Lesson saved to {lesson_path}")
    print("First 500 characters of the lesson:")
    print(lesson[:500])

if __name__ == "__main__":
    asyncio.run(generate_work_energy_lesson())

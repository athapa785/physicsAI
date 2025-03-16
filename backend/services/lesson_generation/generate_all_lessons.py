import asyncio
import os
import sys
import json
from pathlib import Path
from typing import List, Dict

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.services.physics_service import PhysicsService
from backend.services.multi_llm_service import MultiLLMService, LLMProvider, LLMModel

async def generate_all_lessons():
    # Initialize services
    physics_service = PhysicsService()
    
    # Set OpenAI API key
    openai_api_key = input("Enter your OpenAI API key: ")
    physics_service.llm_service.set_api_key(LLMProvider.OPENAI, openai_api_key)
    
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
    
    print(f"\nTotal topics to generate: {len(all_topics)}")
    print("Generating lessons...")
    
    # Generate lessons for each topic
    for i, topic in enumerate(all_topics):
        print(f"[{i+1}/{len(all_topics)}] Generating lesson for: {topic}")
        
        # Create a valid filename from the topic
        filename = topic.replace(' ', '_').replace("'", '').replace(',', '').replace('(', '').replace(')', '')
        lesson_path = lessons_dir / f"{filename}.md"
        
        # Skip if the lesson already exists (comment this out to regenerate all)
        # if lesson_path.exists():
        #     print(f"  - Lesson already exists at {lesson_path}, skipping...")
        #     continue
        
        try:
            # Generate the lesson
            lesson = await physics_service.generate_lesson(topic)
            
            # Save the lesson to a file
            with open(lesson_path, "w") as f:
                f.write(lesson)
            
            print(f"  - Lesson saved to {lesson_path}")
        except Exception as e:
            print(f"  - Error generating lesson for {topic}: {str(e)}")
    
    print("\nAll lessons generated successfully!")
    
    # Verify that the RAG system is working properly
    print("\nTesting RAG system with a sample question...")
    try:
        question = "What is the relationship between force and acceleration?"
        topic = "Newton's Laws"
        answer = await physics_service.answer_question(question, topic, [])
        print(f"\nQuestion: {question}")
        print(f"Topic: {topic}")
        print(f"Answer: {answer[:500]}...")
        print("\nRAG system is working properly!")
    except Exception as e:
        print(f"Error testing RAG system: {str(e)}")

if __name__ == "__main__":
    asyncio.run(generate_all_lessons())

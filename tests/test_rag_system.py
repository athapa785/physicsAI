import asyncio
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from backend.services.physics_service import PhysicsService
from backend.services.multi_llm_service import MultiLLMService, LLMProvider, LLMModel

async def test_rag_system():
    """
    Test the RAG system by asking questions about different physics topics
    and verifying that the answers are relevant and accurate.
    """
    # Initialize services
    physics_service = PhysicsService()
    
    # Set OpenAI API key
    openai_api_key = input("Enter your OpenAI API key: ")
    physics_service.llm_service.set_api_key(LLMProvider.OPENAI, openai_api_key)
    
    # Set active provider and model
    physics_service.llm_service.set_active_provider(LLMProvider.OPENAI)
    physics_service.llm_service.set_active_model(LLMModel.GPT4)
    
    # Define test questions for different topics
    test_questions = [
        ("What is Newton's Second Law and how is it mathematically expressed?", "Forces Newtons Laws"),
        ("Explain the concept of work-energy theorem.", "Work Energy"),
        ("How does simple harmonic motion relate to pendulum motion?", "Simple Harmonic Motion"),
        ("What is the uncertainty principle in quantum mechanics?", "Quantum Mechanics"),
        ("How do electric fields and magnetic fields interact?", "Electromagnetic Induction")
    ]
    
    # Test each question
    for i, (question, topic) in enumerate(test_questions):
        print(f"\n[{i+1}/{len(test_questions)}] Testing question about {topic}")
        print(f"Question: {question}")
        
        try:
            # Get answer using RAG
            answer = await physics_service.answer_question(
                question=question,
                topic=topic,
                chat_history=[],
                provider=LLMProvider.OPENAI,
                model=LLMModel.GPT4
            )
            
            # Print truncated answer
            print(f"Answer (truncated): {answer[:300]}...")
            
            # Save the full answer to a file for review
            answer_dir = Path("test_results")
            answer_dir.mkdir(exist_ok=True)
            
            # Create a filename from the topic
            filename = topic.replace(' ', '_').replace("'", '').replace(',', '').replace('(', '').replace(')', '')
            answer_path = answer_dir / f"{filename}_answer.md"
            
            with open(answer_path, "w") as f:
                f.write(f"# Question: {question}\n\n")
                f.write(f"# Topic: {topic}\n\n")
                f.write(f"# Answer:\n\n{answer}")
            
            print(f"Full answer saved to {answer_path}")
            
        except Exception as e:
            print(f"Error testing RAG for {topic}: {str(e)}")
    
    print("\nRAG system testing completed!")

if __name__ == "__main__":
    asyncio.run(test_rag_system())

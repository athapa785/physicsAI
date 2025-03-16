import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from backend.services.multi_llm_service import MultiLLMService, LLMProvider, LLMModel

async def test_gpt45_lesson():
    """Test generating a lesson with GPT-4.5-preview."""
    
    # Initialize the LLM service
    llm_service = MultiLLMService()
    
    # Set OpenAI API key
    openai_api_key = input("Enter your OpenAI API key: ")
    llm_service.set_api_key(LLMProvider.OPENAI, openai_api_key)
    
    # Set to use OpenAI with GPT-4.5-preview
    llm_service.set_active_provider(LLMProvider.OPENAI)
    llm_service.set_active_model(LLMModel.GPT45_PREVIEW)
    
    # Topic to test
    topic = "Newton's Laws"
    
    # Enhanced prompt for lesson generation
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
    
    print(f"Generating lesson for {topic} with GPT-4.5-preview...")
    
    try:
        # Generate the lesson
        lesson = await llm_service.generate_text(prompt, system_prompt, temperature=0.7)
        
        # Save the lesson to a file
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "test_lesson.md"
        with open(output_file, "w") as f:
            f.write(lesson)
        
        print(f"Lesson saved to {output_file}")
        print("\nFirst 500 characters of the lesson:")
        print(lesson[:500])
        
    except Exception as e:
        print(f"Error generating lesson: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_gpt45_lesson())

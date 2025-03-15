import streamlit as st
import os
import sys
import asyncio
import json
from pathlib import Path
from openai import OpenAI

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# No longer loading from .env file - require explicit API key entry

# Import backend services
from backend.services.physics_service import PhysicsService
from backend.services.lesson_storage import LessonStorage
from backend.services.speech_service import SpeechService, TTSProvider, TTSVoice, text_to_speech
from backend.services.multi_llm_service import MultiLLMService, LLMProvider, LLMModel
from backend.services.rag_service import PhysicsRAG

# Initialize services
llm_service = MultiLLMService()
speech_service = SpeechService()
lesson_storage = LessonStorage()
physics_service = PhysicsService()
rag_service = PhysicsRAG()

# Initialize session state variables
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'current_audio' not in st.session_state:
    st.session_state.current_audio = None
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'mode' not in st.session_state:
    st.session_state.mode = 'browse'  # 'browse' or 'lesson' or 'qa'
if 'llm_provider' not in st.session_state:
    st.session_state.llm_provider = LLMProvider.OPENAI
if 'llm_model' not in st.session_state:
    st.session_state.llm_model = LLMModel.GPT4
if 'tts_provider' not in st.session_state:
    st.session_state.tts_provider = TTSProvider.OPENAI
if 'tts_voice' not in st.session_state:
    st.session_state.tts_voice = TTSVoice.NOVA

st.title("Physics Learning Assistant")

# Navigation and controls
with st.sidebar:
    st.write("Navigation:")
    if st.session_state.mode == 'lesson':
        if st.button("← Back to Chapters", type="primary"):
            # Reset all session state variables related to lessons
            st.session_state.mode = 'browse'
            st.session_state.current_lesson = None
            if 'topics' in st.session_state:
                del st.session_state.topics
            if 'current_topic' in st.session_state:
                st.session_state.current_topic = None
            if 'chat_history' in st.session_state:
                st.session_state.chat_history = []
            st.rerun()
    
    st.write("Audio Controls:")
    voice_enabled = st.checkbox("🔊 Enable Voice Output", value=False)
    
    # LLM and TTS Configuration
    st.write("---")
    st.write("### Model Configuration")
    
    # LLM Provider selection
    llm_provider_options = {
        LLMProvider.OPENAI: "OpenAI",
        LLMProvider.ANTHROPIC: "Anthropic",
        LLMProvider.GOOGLE: "Google Gemini",
        LLMProvider.DEEPINFRA: "DeepInfra (Llama, Mixtral)"
    }
    
    selected_llm_provider = st.selectbox(
        "LLM Provider",
        options=list(llm_provider_options.keys()),
        format_func=lambda x: llm_provider_options[x],
        index=list(llm_provider_options.keys()).index(st.session_state.llm_provider)
    )
    
    # Update provider in session state
    if selected_llm_provider != st.session_state.llm_provider:
        st.session_state.llm_provider = selected_llm_provider
        # Reset model when provider changes
        st.session_state.llm_model = llm_service.get_available_models(selected_llm_provider)[0]
    
    # Get available models for the selected provider
    available_models = llm_service.get_available_models(selected_llm_provider)
    model_options = {model: model.value for model in available_models}
    
    # Model selection
    selected_model = st.selectbox(
        "Model",
        options=list(model_options.keys()),
        format_func=lambda x: model_options[x],
        index=0 if st.session_state.llm_model not in available_models else list(model_options.keys()).index(st.session_state.llm_model)
    )
    
    # Update model in session state
    if selected_model != st.session_state.llm_model:
        st.session_state.llm_model = selected_model
    
    # Voice selection for TTS
    st.write("### Text-to-Speech Configuration")
    voice_options = {
        TTSVoice.NOVA: "Nova (Female, Natural)",
        TTSVoice.ALLOY: "Alloy (Neutral, Balanced)",
        TTSVoice.ECHO: "Echo (Male, Deep)",
        TTSVoice.FABLE: "Fable (Male, British)",
        TTSVoice.ONYX: "Onyx (Male, Deep)",
        TTSVoice.SHIMMER: "Shimmer (Female, Cheerful)"
    }
    
    selected_voice = st.selectbox(
        "Voice",
        options=list(voice_options.keys()),
        format_func=lambda x: voice_options[x],
        index=list(voice_options.keys()).index(st.session_state.tts_voice)
    )
    
    # Update voice in session state
    if selected_voice != st.session_state.tts_voice:
        st.session_state.tts_voice = selected_voice
        speech_service.set_active_voice(selected_voice)
    
    # API Keys section
    st.write("### API Keys")
    st.write("Enter API keys for the providers you want to use:")
    
    # OpenAI API Key - MANDATORY
    st.write("### OpenAI API Key (Required)")
    st.write("⚠️ You must enter a valid OpenAI API key to use this application.")
    
    # Try to get API key from Streamlit secrets first
    default_openai_key = ""
    if 'api_keys' in st.secrets and 'openai' in st.secrets['api_keys']:
        default_openai_key = st.secrets['api_keys']['openai']
    
    # Allow manual input with secret as default
    openai_key = st.text_input(
        "Enter your OpenAI API Key", 
        type="password", 
        value=default_openai_key, 
        placeholder="sk-...", 
        help="Your API key should start with 'sk-'"
    )
    
    # Validate and set the API key if provided
    if openai_key and openai_key.startswith("sk-"):
        # Set API key for all services
        os.environ["OPENAI_API_KEY"] = openai_key
        llm_service.set_api_key(LLMProvider.OPENAI, openai_key)
        speech_service.set_api_key(TTSProvider.OPENAI, openai_key)
        
        # Update RAG service with the API key
        if hasattr(physics_service, 'rag_service') and physics_service.rag_service:
            physics_service.rag_service.openai_client = OpenAI(api_key=openai_key)
        
        # Also ensure the RAG service directly has the API key
        if rag_service:
            rag_service.openai_client = OpenAI(api_key=openai_key)
            
        st.success("✅ OpenAI API key set successfully!")
    elif openai_key:
        st.error("❌ Invalid OpenAI API key. It should start with 'sk-'.")
    else:
        st.warning("⚠️ Please enter your OpenAI API key to use the application.")
    
    # Anthropic API Key
    default_anthropic_key = ""
    if 'api_keys' in st.secrets and 'anthropic' in st.secrets['api_keys']:
        default_anthropic_key = st.secrets['api_keys']['anthropic']
    
    anthropic_key = st.text_input("Anthropic API Key", type="password", value=default_anthropic_key, placeholder="anthropic-api-key...")
    if anthropic_key:
        llm_service.set_api_key(LLMProvider.ANTHROPIC, anthropic_key)
        st.success("Anthropic API key set successfully!")
    
    # Google API Key
    default_google_key = ""
    if 'api_keys' in st.secrets and 'google' in st.secrets['api_keys']:
        default_google_key = st.secrets['api_keys']['google']
    
    google_key = st.text_input("Google API Key", type="password", value=default_google_key, placeholder="google-api-key...")
    if google_key:
        llm_service.set_api_key(LLMProvider.GOOGLE, google_key)
        st.success("Google API key set successfully!")
    
    # DeepInfra API Key
    default_deepinfra_key = ""
    if 'api_keys' in st.secrets and 'deepinfra' in st.secrets['api_keys']:
        default_deepinfra_key = st.secrets['api_keys']['deepinfra']
    
    deepinfra_key = st.text_input("DeepInfra API Key", type="password", value=default_deepinfra_key, placeholder="deepinfra-api-key...")
    if deepinfra_key:
        llm_service.set_api_key(LLMProvider.DEEPINFRA, deepinfra_key)
        st.success("DeepInfra API key set successfully!")
    
    # Set active provider and model based on user selection
    if selected_llm_provider in llm_service.get_available_providers():
        llm_service.set_active_provider(selected_llm_provider)
        llm_service.set_active_model(selected_model)

# Helper function to check if any API key is available
def check_api_key():
    # Check for available providers from the LLM service
    available_providers = llm_service.get_available_providers()
    
    # First check if OpenAI API key is available (required for RAG and TTS)
    if LLMProvider.OPENAI not in available_providers:
        st.error("⚠️ A valid OpenAI API key is required. Please enter it in the sidebar.")
        return False
    
    # Then check if any provider is available
    if not available_providers:
        st.error("Please enter at least one API key in the sidebar")
        return False
    
    # Make sure the active provider has an API key
    if st.session_state.llm_provider not in available_providers:
        # Try to set a different available provider
        llm_service.set_active_provider(available_providers[0])
        st.session_state.llm_provider = available_providers[0]
        st.warning(f"Switched to {available_providers[0]} as the active provider since it has an API key")
    
    # We don't need to set the OpenAI client here as it's already set when the key is entered in the sidebar
    return True

# Helper function to run async functions
def run_async(func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(func)
    loop.close()
    return result

# Main content area
if st.session_state.mode == 'browse':
    if check_api_key():
        try:
            # Get chapters
            chapters = physics_service.get_chapters()
            
            st.write("## Chapters")
            st.write("Select a chapter to explore topics:")
            
            # Display chapters as expandable cards
            for i, chapter in enumerate(chapters):
                with st.expander(f"Chapter {chapter['number']}: {chapter['title']}", expanded=False):
                    topics = physics_service.get_topics(chapter['number'])
                    if topics:
                        st.write(f"### {len(topics)} Topics Available")
                        # Display topics directly within the chapter expander
                        for topic in topics:
                            if st.button(f"📚 {topic}", key=f"topic_{chapter['number']}_{topic}"):
                                st.session_state.current_chapter = chapter
                                st.session_state.current_topic = topic
                                st.session_state.mode = 'lesson'
                                st.rerun()
                    else:
                        st.write("No topics available for this chapter yet.")
        
        except Exception as e:
            st.error(f"Error loading chapters: {str(e)}")

elif st.session_state.mode == 'lesson' and st.session_state.current_topic:
    # Show chapter and topic context
    st.write(f"## {st.session_state.current_topic}")
    st.write(f"*Chapter {st.session_state.current_chapter['number']}: {st.session_state.current_chapter['title']}*")
    
    # Generate or load lesson
    with st.spinner("Loading lesson..."):
        # Check if we have a cached lesson
        if st.session_state.current_lesson is None:
            st.session_state.current_lesson = run_async(physics_service.generate_lesson(st.session_state.current_topic))
        
        # Display lesson content
        st.markdown(st.session_state.current_lesson)
        
        # Generate or load audio
        if voice_enabled:
            # Create a safe filename from the topic and voice
            voice_name = st.session_state.tts_voice.value
            safe_topic = "".join(c if c.isalnum() else "_" for c in st.session_state.current_topic)
            audio_cache_dir = "backend/audio/cache"
            os.makedirs(audio_cache_dir, exist_ok=True)
            audio_cache_path = os.path.join(audio_cache_dir, f"{safe_topic}_{voice_name}.mp3")
            
            # Check if audio is already cached
            if os.path.exists(audio_cache_path):
                st.audio(audio_cache_path)
            else:
                # Generate audio on-the-fly
                with st.spinner("Generating audio..."):
                    # Use the speech service with the selected voice
                    audio_content = speech_service.text_to_speech(
                        st.session_state.current_lesson, 
                        st.session_state.tts_voice
                    )
                    
                    # Check if we got valid audio content
                    if audio_content and len(audio_content) > 0:
                        # Save audio content to cache
                        os.makedirs(os.path.dirname(audio_cache_path), exist_ok=True)
                        with open(audio_cache_path, "wb") as f:
                            f.write(audio_content)
                        
                        st.audio(audio_cache_path)
                    else:
                        st.warning("⚠️ Audio generation unavailable. Please check your API key in the settings.")
    
    # Q&A section
    st.write("---")
    st.write("## Ask a Question")
    st.write("Have a question about this topic? Ask here:")
    
    # Initialize the submitted flag in session state if it doesn't exist
    if "question_submitted" not in st.session_state:
        st.session_state.question_submitted = False
    
    # Function to handle question submission
    def submit_question():
        if st.session_state.question_input.strip():
            st.session_state.current_question = st.session_state.question_input
            st.session_state.question_submitted = True
            # Clear the input field after submission
            st.session_state.question_input = ""
    
    # Text input that submits on Enter
    question = st.text_input("Your question:", key="question_input", on_change=submit_question)
    
    # Process the submitted question
    if st.session_state.question_submitted:
        # Display the question immediately while the LLM is generating
        with st.container(border=True):
            st.write("**You asked:**")
            st.write(st.session_state.current_question)
            with st.spinner(f"LLM is generating a response using {st.session_state.llm_provider.value} {st.session_state.llm_model.value}..."):
                # Format chat history for the RAG service
                formatted_chat_history = []
                for exchange in st.session_state.chat_history:
                    formatted_chat_history.append((exchange["user"], exchange["assistant"]))
                
                # Pass the active provider, model, and chat history to the physics service
                answer = run_async(physics_service.answer_question(
                    st.session_state.current_question,
                    st.session_state.current_topic,
                    formatted_chat_history,  # Pass the formatted chat history
                    provider=st.session_state.llm_provider,
                    model=st.session_state.llm_model
                ))
                
                # Add the response below the question
                st.write("**Response:**")
                st.markdown(answer)
            
            # Add to chat history
            st.session_state.chat_history.append({"user": st.session_state.current_question, "assistant": answer})
            
            # Reset the submitted flag
            st.session_state.question_submitted = False
    
    # Display chat history (only if not already showing the current question)
    if st.session_state.chat_history and not st.session_state.question_submitted:
        
        # Display previous Q&As in expandable boxes
        if len(st.session_state.chat_history) > 1:
            st.write("### Previous Questions")
            for i, exchange in enumerate(reversed(st.session_state.chat_history[:-1])):
                with st.expander(f"Question {len(st.session_state.chat_history) - i - 1}: {exchange['user'][:50]}{'...' if len(exchange['user']) > 50 else ''}"):
                    st.write("**You asked:**")
                    st.write(exchange["user"])
                    st.write("**Response:**")
                    st.markdown(exchange["assistant"])

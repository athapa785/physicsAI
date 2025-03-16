import os
import streamlit as st
from openai import OpenAI
from backend.services.multi_llm_service import LLMProvider

def check_api_key(llm_service):
    """
    Check if any API key is available and set the active provider.
    
    Args:
        llm_service: The LLM service instance
        
    Returns:
        bool: True if an API key is available, False otherwise
    """
    # Check for available providers from the LLM service
    available_providers = llm_service.get_available_providers()
    
    # Check if any provider is available
    if not available_providers:
        st.error("Please enter at least one API key in the sidebar to use the LLM features")
        return False
    
    # Make sure the active provider has an API key
    if st.session_state.llm_provider not in available_providers:
        # Try to set a different available provider
        llm_service.set_active_provider(available_providers[0])
        st.session_state.llm_provider = available_providers[0]
        st.info(f"Using {available_providers[0]} as the active provider")
    
    return True

def load_api_keys_from_secrets():
    """
    Load API keys from Streamlit secrets if available.
    
    Returns:
        tuple: (openai_key, anthropic_key) - Default API keys from secrets
    """
    default_openai_key = ""
    default_anthropic_key = ""
    
    try:
        if 'api_keys' in st.secrets and 'openai' in st.secrets['api_keys']:
            default_openai_key = st.secrets['api_keys']['openai']
        
        if 'api_keys' in st.secrets and 'anthropic' in st.secrets['api_keys']:
            default_anthropic_key = st.secrets['api_keys']['anthropic']
    except Exception:
        # Handle missing secrets file gracefully
        pass
    
    return default_openai_key, default_anthropic_key

def setup_openai_api(openai_key, llm_service, physics_service, rag_service):
    """
    Set up the OpenAI API key for all services.
    
    Args:
        openai_key: The OpenAI API key
        llm_service: The LLM service instance
        physics_service: The physics service instance
        rag_service: The RAG service instance
        
    Returns:
        bool: True if the API key was set successfully, False otherwise
    """
    if openai_key and openai_key.startswith("sk-"):
        # Set API key for all services
        os.environ["OPENAI_API_KEY"] = openai_key
        llm_service.set_api_key(LLMProvider.OPENAI, openai_key)
        
        # Update RAG service with the API key
        if hasattr(physics_service, 'rag_service') and physics_service.rag_service:
            physics_service.rag_service.openai_client = OpenAI(api_key=openai_key)
        
        # Also ensure the RAG service directly has the API key
        if rag_service:
            rag_service.openai_client = OpenAI(api_key=openai_key)
        
        return True
    elif openai_key:
        st.error("❌ Invalid OpenAI API key. It should start with 'sk-'.")
    
    return False

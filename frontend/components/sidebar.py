import streamlit as st
from backend.services.multi_llm_service import LLMProvider, LLMModel
from frontend.utils.api_keys import load_api_keys_from_secrets, setup_openai_api

def render_sidebar(llm_service, physics_service, rag_service):
    """
    Render the sidebar with navigation and configuration options.
    
    Args:
        llm_service: The LLM service instance
        physics_service: The physics service instance
        rag_service: The RAG service instance
    """
    with st.sidebar:
        render_navigation()
        render_model_configuration(llm_service)
        render_api_keys(llm_service, physics_service, rag_service)

def render_navigation():
    """Render the navigation buttons in the sidebar."""
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("About", use_container_width=True):
            st.session_state.mode = 'about'
            st.rerun()
    
    with col2:
        if st.button("How to Use", use_container_width=True):
            st.session_state.mode = 'how_to_use'
            st.rerun()
    
    # Home button
    if st.session_state.mode in ['about', 'how_to_use']:
        if st.button("← Home", type="primary"):
            st.session_state.mode = 'browse'
            st.rerun()
    
    # Back to chapters button for lesson mode
    if st.session_state.mode == 'lesson':
        if st.button("← Back to Chapters", type="primary"):
            # Reset all session state variables related to lessons
            from frontend.utils.session import reset_lesson_state
            reset_lesson_state()
            st.rerun()
    
    st.write("---")

def render_model_configuration(llm_service):
    """
    Render the LLM model configuration section.
    
    Args:
        llm_service: The LLM service instance
    """
    st.write("### Model Configuration")
    
    # LLM Provider selection
    llm_provider_options = {
        LLMProvider.OPENAI: "OpenAI",
        LLMProvider.ANTHROPIC: "Anthropic"
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
    
    # Set active provider and model based on user selection
    if selected_llm_provider in llm_service.get_available_providers():
        llm_service.set_active_provider(selected_llm_provider)
        llm_service.set_active_model(selected_model)
    
    st.write("---")

def render_api_keys(llm_service, physics_service, rag_service):
    """
    Render the API keys section.
    
    Args:
        llm_service: The LLM service instance
        physics_service: The physics service instance
        rag_service: The RAG service instance
    """
    st.write("### API Keys")
    st.write("Enter API keys for the providers you want to use:")
    
    # Load default API keys from secrets
    default_openai_key, default_anthropic_key = load_api_keys_from_secrets()
    
    # OpenAI API Key
    openai_key = st.text_input(
        "Enter your OpenAI API Key", 
        type="password", 
        value=default_openai_key, 
        placeholder="openai-api-key...", 
        help="Your API key should start with 'sk-'"
    )
    
    # Set up OpenAI API key
    if setup_openai_api(openai_key, llm_service, physics_service, rag_service):
        st.success("✅ OpenAI API key set successfully!")
    
    # Anthropic API Key
    anthropic_key = st.text_input(
        "Enter your Anthropic API Key", 
        type="password", 
        value=default_anthropic_key, 
        placeholder="anthropic-api-key..."
    )
    
    if anthropic_key:
        llm_service.set_api_key(LLMProvider.ANTHROPIC, anthropic_key)
        st.success("✅ Anthropic API key set successfully!")

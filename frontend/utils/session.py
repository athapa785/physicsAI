import streamlit as st
from backend.services.multi_llm_service import LLMProvider, LLMModel

def initialize_session_state():
    """Initialize all session state variables needed for the application."""
    # Basic navigation state
    if 'mode' not in st.session_state:
        st.session_state.mode = 'browse'  # 'browse' or 'lesson' or 'qa' or 'about' or 'how_to_use'
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = None
    if 'slide_index' not in st.session_state:
        st.session_state.slide_index = 0
    
    # Topic and chat history management
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
    if 'topic_chat_history' not in st.session_state:
        st.session_state.topic_chat_history = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Ensure chat history is properly loaded from topic history if available
    if st.session_state.get('current_topic') and st.session_state.get('current_topic') in st.session_state.get('topic_chat_history', {}):
        st.session_state.chat_history = st.session_state.topic_chat_history[st.session_state.current_topic].copy()
    
    # Navigation tracking for slide transitions
    if 'prev_slide_clicked' not in st.session_state:
        st.session_state.prev_slide_clicked = False
    if 'next_slide_clicked' not in st.session_state:
        st.session_state.next_slide_clicked = False
    
    # LLM settings
    if 'llm_provider' not in st.session_state:
        st.session_state.llm_provider = LLMProvider.OPENAI
    if 'llm_model' not in st.session_state:
        st.session_state.llm_model = LLMModel.GPT4
    if 'question_submitted' not in st.session_state:
        st.session_state.question_submitted = False

def reset_lesson_state():
    """Reset all session state variables related to lessons."""
    st.session_state.mode = 'browse'
    st.session_state.current_lesson = None
    st.session_state.slide_index = 0
    if 'topics' in st.session_state:
        del st.session_state.topics
    if 'current_topic' in st.session_state:
        st.session_state.current_topic = None
    # We don't reset the topic_chat_history to preserve Q&A history across sessions
    if 'chat_history' in st.session_state:
        st.session_state.chat_history = []

import streamlit as st
from frontend.utils.async_utils import run_async

def render_qa_section(physics_service):
    """
    Render the question and answer section.
    
    Args:
        physics_service: The physics service instance
    """
    st.write("---")
    
    # Create a header with info icon and tooltip
    st.markdown("## Ask a Question", help="Tips for asking effective questions: Be specific, use proper nouns instead of pronouns (e.g., 'linear momentum' instead of 'it'), ask one question at a time")
    
    st.write("Have a question about this topic? Ask here:")
    
    # Initialize the submitted flag in session state if it doesn't exist
    if "question_submitted" not in st.session_state:
        st.session_state.question_submitted = False
        
    # Initialize topic-specific chat history if it doesn't exist
    if "topic_chat_history" not in st.session_state:
        st.session_state.topic_chat_history = {}
    
    # Get current topic
    current_topic = st.session_state.current_topic
    
    # Initialize chat history for current topic if it doesn't exist
    if current_topic not in st.session_state.topic_chat_history:
        st.session_state.topic_chat_history[current_topic] = []
    
    # Initialize chat_history if it doesn't exist
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Always load the topic-specific history when rendering the QA section
    # This ensures we have the latest chat history for this topic
    if current_topic in st.session_state.topic_chat_history:
        # Use a deep copy to avoid reference issues
        st.session_state.chat_history = st.session_state.topic_chat_history[current_topic].copy()
        
    # Debug info has been removed
    
    # Text input that submits on Enter
    st.text_input(
        "Your question:", 
        key="question_input", 
        on_change=submit_question
    )
    
    # Process the submitted question
    if st.session_state.question_submitted:
        process_submitted_question(physics_service)
    
    # Display chat history
    display_chat_history()

def submit_question():
    """Handle question submission from the input field."""
    if st.session_state.question_input.strip():
        st.session_state.current_question = st.session_state.question_input
        st.session_state.question_submitted = True
        # Clear the input field after submission
        st.session_state.question_input = ""

def process_submitted_question(physics_service):
    """
    Process the submitted question and generate a response.
    
    Args:
        physics_service: The physics service instance
    """
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
                formatted_chat_history,
                provider=st.session_state.llm_provider,
                model=st.session_state.llm_model
            ))
            
            # Add the response below the question
            st.write("**Response:**")
            st.markdown(answer)
        
        # Create a new exchange
        new_exchange = {
            "user": st.session_state.current_question, 
            "assistant": answer
        }
        
        # Add to the current chat history
        st.session_state.chat_history.append(new_exchange)
        
        # Immediately update the topic-specific history with a copy of the current chat history
        # This ensures the history is preserved across reruns
        st.session_state.topic_chat_history[st.session_state.current_topic] = st.session_state.chat_history.copy()
        
        # Reset the submitted flag
        st.session_state.question_submitted = False

def display_chat_history():
    """Display the chat history in expandable sections."""
    # Display chat history (only if not already showing the current question)
    if st.session_state.chat_history and not st.session_state.question_submitted:
        # Display all Q&As in expandable boxes
        if len(st.session_state.chat_history) >= 1:
            st.write("### Questions & Answers")
            for i, exchange in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(
                    f"Question {len(st.session_state.chat_history) - i}: {exchange['user'][:50]}{'...' if len(exchange['user']) > 50 else ''}"
                ):
                    st.write("**You asked:**")
                    st.write(exchange["user"])
                    st.write("**Response:**")
                    st.markdown(exchange["assistant"])

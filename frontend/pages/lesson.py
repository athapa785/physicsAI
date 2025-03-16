import streamlit as st
from frontend.utils.async_utils import run_async
from frontend.utils.api_keys import check_api_key
from frontend.components.lesson_display import display_lesson_slideshow
from frontend.components.qa_section import render_qa_section

def render_lesson_page(physics_service):
    """
    Render the lesson page with slideshow and Q&A section.
    
    Args:
        physics_service: The physics service instance
    """
    if not st.session_state.current_topic:
        st.error("No topic selected. Please select a topic from the browse page.")
        return
    
    # Create a subtle back button
    col1, col2 = st.columns([1, 15])
    with col1:
        if st.button("←", key="back_to_topics_link", help="Return to topic selection"):
            st.session_state.mode = 'browse'
            # Reset slide index when returning to chapter selection
            st.session_state.slide_index = 0
            st.rerun()
    
    # Display chapter and topic info with larger font and bolder text
    st.markdown(
        f"<p style='font-size: 1.5rem; font-weight: 700;'><em>Chapter {st.session_state.current_chapter['number']}: "
        f"{st.session_state.current_chapter['title']} - {st.session_state.current_topic}</em></p>", 
        unsafe_allow_html=True
    )
    
    # Check if API key is available for lesson generation
    if check_api_key(physics_service.llm_service):
        # Generate or load lesson
        with st.spinner("Loading lesson..."):
            # Check if we have a cached lesson
            if st.session_state.current_lesson is None:
                st.session_state.current_lesson = run_async(
                    physics_service.generate_lesson(st.session_state.current_topic)
                )
            
            # Initialize slide index in session state if not already set
            if "slide_index" not in st.session_state:
                st.session_state.slide_index = 0
            
            # Display the lesson as a slideshow
            display_lesson_slideshow(st.session_state.current_lesson)
            
            # Render the Q&A section
            render_qa_section(physics_service)
    else:
        st.warning("Please enter an API key in the sidebar to generate lessons.")

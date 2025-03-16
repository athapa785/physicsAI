import streamlit as st

def render_browse_page(physics_service):
    """
    Render the browse page with chapters and topics.
    
    Args:
        physics_service: The physics service instance
    """
    try:
        # Get chapters - this doesn't require an API key
        chapters = physics_service.get_chapters()
        
        st.write("## Chapters")
        st.write("Select a chapter to explore topics:")
        
        # Display chapters as expandable cards
        for i, chapter in enumerate(chapters):
            with st.expander(f"Chapter {chapter['number']}: {chapter['title']}", expanded=False):
                topics = physics_service.get_topics(chapter['number'])
                if topics:
                    # Display topics directly within the chapter expander
                    for topic in topics:
                        if st.button(f"📚 {topic}", key=f"topic_{chapter['number']}_{topic}"):
                            st.session_state.current_chapter = chapter
                            st.session_state.current_topic = topic
                            st.session_state.mode = 'lesson'
                            # Reset slide index when a new topic is selected
                            st.session_state.slide_index = 0
                            # Reset current lesson to force regeneration
                            st.session_state.current_lesson = None
                            st.rerun()
                else:
                    st.write("No topics available for this chapter yet.")
    
    except Exception as e:
        st.error(f"Error loading chapters: {str(e)}")

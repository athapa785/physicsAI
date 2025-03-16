import streamlit as st
import os
import sys
from pathlib import Path

# Fix import issues for both local and cloud deployment
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Create __init__.py files if they don't exist (for package recognition)
def ensure_init_files():
    backend_dir = os.path.join(project_root, 'backend')
    services_dir = os.path.join(backend_dir, 'services')
    
    # Create __init__.py files if they don't exist
    for dir_path in [backend_dir, services_dir]:
        if os.path.exists(dir_path):
            init_file = os.path.join(dir_path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    pass  # Create empty file

# Ensure __init__.py files exist
ensure_init_files()

# Import backend services
try:
    from backend.services.physics_service import PhysicsService
    from backend.services.lesson_storage import LessonStorage
    from backend.services.multi_llm_service import MultiLLMService
    from backend.services.rag_service import PhysicsRAG
    from frontend.utils.styling import load_css, apply_lesson_mode_styling
    
    # Import frontend modules
    from frontend.utils.session import initialize_session_state
    from frontend.components.sidebar import render_sidebar
    from frontend.pages.about import render_about_page
    from frontend.pages.how_to_use import render_how_to_use_page
    from frontend.pages.browse import render_browse_page
    from frontend.pages.lesson import render_lesson_page
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Current sys.path: " + str(sys.path))
    st.error("Current directory: " + current_dir)
    st.error("Files in backend/services: " + str(os.listdir(os.path.join(current_dir, 'backend', 'services')) if os.path.exists(os.path.join(current_dir, 'backend', 'services')) else "Directory not found"))
    raise

def main():
    """Main function to run the PhysicsAI Streamlit app."""
    # Initialize services
    llm_service = MultiLLMService()
    lesson_storage = LessonStorage()
    physics_service = PhysicsService()
    rag_service = PhysicsRAG()
    
    # Initialize session state
    initialize_session_state()
    
    # Only show title on the browse, about, and how_to_use pages
    if st.session_state.mode in ['browse', 'about', 'how_to_use']:
        st.title("Physics Learning Assistant")
    
    # Load CSS styles from external file
    load_css()
    
    # Hide sidebar in lesson mode
    if st.session_state.mode == 'lesson':
        apply_lesson_mode_styling()
    
    # Render the sidebar
    render_sidebar(llm_service, physics_service, rag_service)
    
    # Render the appropriate page based on the current mode
    if st.session_state.mode == 'about':
        render_about_page()
    elif st.session_state.mode == 'how_to_use':
        render_how_to_use_page()
    elif st.session_state.mode == 'browse':
        render_browse_page(physics_service)
    elif st.session_state.mode == 'lesson':
        render_lesson_page(physics_service)

if __name__ == "__main__":
    main()

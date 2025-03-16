import streamlit as st

def render_how_to_use_page():
    """Render the How to Use page content."""
    st.write("## How to Use PhysicsAI")
    
    st.markdown("""
    <div style='font-size: 1.1rem;'>
    <h3>Getting Started</h3>
    <ol>
        <li><strong>Enter API Keys:</strong> In the sidebar, enter your OpenAI or Anthropic API key to enable lesson generation and question answering.</li>
        <li><strong>Select a Chapter:</strong> On the home page, expand a chapter to view available topics.</li>
        <li><strong>Choose a Topic:</strong> Click on any topic to access its comprehensive lesson.</li>
    </ol>
    
    <h3>Navigating Lessons</h3>
    <ol>
        <li><strong>Slideshow Navigation:</strong> Use the arrow buttons at the bottom of the lesson to move between slides.</li>
        <li><strong>Return to Chapters:</strong> Click the "Back to Chapters" button in the sidebar to return to the main navigation.</li>
    </ol>
    
    <h3>Asking Questions</h3>
    <ol>
        <li><strong>Question Input:</strong> Scroll to the bottom of any lesson to find the question input field.</li>
        <li><strong>Context-Aware Answers:</strong> The system will provide answers that are relevant to the current topic you're studying.</li>
        <li><strong>Previous Questions:</strong> Your question history is saved and can be accessed in expandable sections below the input field.</li>
    </ol>
    
    <h3>Customizing Your Experience</h3>
    <ol>
        <li><strong>LLM Selection:</strong> Choose between different AI providers (OpenAI or Anthropic) and models in the sidebar.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

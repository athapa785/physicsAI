import streamlit as st

def render_about_page():
    """Render the About page content."""
    st.write("## About PhysicsAI")
    
    st.markdown("""
    <div style='font-size: 1.1rem;'>
    <p><strong>PhysicsAI</strong> is an interactive physics education platform designed to help students learn and understand physics concepts through comprehensive lessons, interactive examples, and AI-powered question answering.</p>
    
    <h3>Key Features</h3>
    <ul>
        <li><strong>Comprehensive Physics Lessons:</strong> Access detailed lessons on various physics topics organized by chapters, following the structure of university-level physics textbooks.</li>
        <li><strong>AI-Powered Question Answering:</strong> Ask questions about any physics topic and receive detailed, contextually relevant answers powered by advanced language models.</li>
        <li><strong>Interactive Learning:</strong> Navigate through lessons with an intuitive slideshow interface that breaks down complex topics into manageable sections.</li>
        <li><strong>Retrieval Augmented Generation:</strong> The system uses RAG technology to provide accurate, physics-specific information by combining the power of large language models with a curated knowledge base.</li>
    </ul>
    
    <h3>Technology</h3>
    <p>PhysicsAI is built using:</p>
    <ul>
        <li><strong>FAISS Vector Store:</strong> For efficient similarity search of physics content</li>
        <li><strong>OpenAI Embeddings:</strong> For text vectorization</li>
        <li><strong>Advanced LLMs:</strong> Including GPT-4 and Claude 3 for content generation</li>
        <li><strong>Streamlit:</strong> For the interactive user interface</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

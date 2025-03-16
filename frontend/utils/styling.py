import streamlit as st
import os

def load_css():
    """
    Load CSS styles from the static/style.css file and apply them to the Streamlit app.
    """
    # Get the absolute path to the CSS file
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    css_file = os.path.join(current_dir, 'frontend', 'static', 'style.css')
    
    # Read the CSS file
    with open(css_file, 'r') as f:
        css = f.read()
    
    # Apply the CSS
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def apply_lesson_mode_styling():
    """
    Apply specific styling for lesson mode (hide sidebar).
    """
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

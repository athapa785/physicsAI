import re
import streamlit as st

def display_lesson_slideshow(lesson_text):
    """
    Display lesson content as a slideshow with navigation buttons.
    
    Args:
        lesson_text: The full lesson text content
        
    Returns:
        str: The current slide text
    """
    # Split the lesson into slides
    slides = split_lesson_into_slides(lesson_text)
    
    # Get current slide index
    current_slide_index = st.session_state.slide_index
    
    # Ensure index is within bounds
    current_slide_index = max(0, min(current_slide_index, len(slides) - 1))
    
    # Process the slide content
    current_slide = process_slide_content(slides[current_slide_index])
    
    # Display the slide content in a container
    with st.container(border=True):
        st.markdown(current_slide, unsafe_allow_html=True)
    
    # Navigation buttons below the slide - centered and wider
    render_navigation_buttons(current_slide_index, len(slides))
    
    # Return the current slide text
    return slides[current_slide_index]

def split_lesson_into_slides(lesson_text):
    """
    Split the lesson text into individual slides.
    
    Args:
        lesson_text: The full lesson text content
        
    Returns:
        list: List of slide content strings
    """
    # First try to split by explicit delimiter
    slides = [slide.strip() for slide in lesson_text.split("---") if slide.strip()]
    
    # If no explicit delimiter found, split by headers (# or ##)
    if len(slides) <= 1:
        # Match markdown headers (# Header or ## Header)
        header_pattern = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)
        
        # Find all headers in the text
        headers = list(header_pattern.finditer(lesson_text))
        
        if headers:
            # Extract introduction text (content before the first header)
            intro_text = ""
            if headers[0].start() > 0:
                intro_text = lesson_text[:headers[0].start()].strip()
            
            slides = []
            # If there's introduction text, add it with the main title
            if intro_text:
                main_title = lesson_text.split('\n')[0] if '\n' in lesson_text else "Introduction"
                slides.append(f"{main_title}\n\n{intro_text}")
            
            # Process headers and create slides, merging headers with minimal content
            processed_slides = []
            for i, header in enumerate(headers):
                start_pos = header.start()
                
                # Determine end position (next header or end of text)
                if i < len(headers) - 1:
                    end_pos = headers[i + 1].start()
                else:
                    end_pos = len(lesson_text)
                
                # Extract current section content
                section_content = lesson_text[start_pos:end_pos].strip()
                header_text = header.group(0)
                content_after_header = section_content[len(header_text):].strip()
                
                # Skip if this header was already processed as part of a merge
                if i > 0 and any(header_text in slide for slide in processed_slides[-1:]):
                    continue
                    
                # If there's minimal content after this header and not the last header
                if (not content_after_header or len(content_after_header.split()) < 5) and i < len(headers) - 1:
                    # Look ahead to next section
                    next_header = headers[i + 1]
                    next_end = headers[i + 2].start() if i + 2 < len(headers) else len(lesson_text)
                    # Merge this header with next section
                    merged_content = lesson_text[start_pos:next_end].strip()
                    processed_slides.append(merged_content)
                else:
                    # Add as a regular slide
                    processed_slides.append(section_content)
            
            # Use the processed slides
            slides = processed_slides
        else:
            # If no headers found, treat the whole lesson as one slide
            slides = [lesson_text]
    
    return slides

def process_slide_content(slide_content):
    """
    Process the slide content to improve formatting and readability.
    
    Args:
        slide_content: The raw slide content
        
    Returns:
        str: Processed slide content
    """
    # Remove any "Lesson: XYZ" headers from the slide content
    slide_content = re.sub(r'^#\s+Lesson:.*$', '', slide_content, flags=re.MULTILINE).strip()
    
    # Remove "Physics Learning Assistant" header if present
    slide_content = re.sub(r'^#\s+Physics Learning Assistant.*$', '', slide_content, flags=re.MULTILINE).strip()
    
    # Make section headers slightly smaller
    slide_content = re.sub(r'^##\s+(.*?)$', r'<h2 style="font-size: 1.4rem;">\1</h2>', slide_content, flags=re.MULTILINE)
    
    # Replace \cdotp with proper dot operator
    slide_content = re.sub(r'\\cdotp', r'\\cdot', slide_content)
    
    return slide_content

def render_navigation_buttons(current_index, total_slides):
    """
    Render the slideshow navigation buttons.
    
    Args:
        current_index: The current slide index
        total_slides: The total number of slides
    """
    # First, ensure we have the necessary session state variables
    if 'prev_slide_clicked' not in st.session_state:
        st.session_state.prev_slide_clicked = False
    if 'next_slide_clicked' not in st.session_state:
        st.session_state.next_slide_clicked = False
        
    # Define callback functions for the buttons
    def on_prev_click():
        # Save chat history to persistent storage
        if st.session_state.current_topic and len(st.session_state.chat_history) > 0:
            # Store in topic_chat_history
            st.session_state.topic_chat_history[st.session_state.current_topic] = st.session_state.chat_history.copy()
        # Update slide index
        st.session_state.slide_index = max(0, current_index - 1)
        st.session_state.prev_slide_clicked = True
        
    def on_next_click():
        # Save chat history to persistent storage
        if st.session_state.current_topic and len(st.session_state.chat_history) > 0:
            # Store in topic_chat_history
            st.session_state.topic_chat_history[st.session_state.current_topic] = st.session_state.chat_history.copy()
        # Update slide index
        st.session_state.slide_index = min(total_slides - 1, current_index + 1)
        st.session_state.next_slide_clicked = True
    
    # Layout the buttons
    col1, col2, col3 = st.columns([3, 4, 3])
    
    # Center the navigation buttons
    with col2:
        btn_col1, btn_col2 = st.columns(2)
        # Left arrow (previous) - wider button
        with btn_col1:
            st.button("⬅️", key="prev_slide", on_click=on_prev_click, use_container_width=True)
        
        # Right arrow (next) - wider button
        with btn_col2:
            st.button("➡️", key="next_slide", on_click=on_next_click, use_container_width=True)
    
    # Slide counter - right aligned
    with col3:
        st.markdown(f"<p style='font-size: 0.8rem; color: gray; text-align: right;'>Slide {current_index + 1} of {total_slides}</p>", unsafe_allow_html=True)
        
    # Handle rerun after button click
    if st.session_state.prev_slide_clicked or st.session_state.next_slide_clicked:
        st.session_state.prev_slide_clicked = False
        st.session_state.next_slide_clicked = False
        st.rerun()

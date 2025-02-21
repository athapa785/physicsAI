import streamlit as st
import requests
import os
from pydub import AudioSegment
from pydub.playback import play
import uuid  

st.title("Introductory Physics Tutor with Voice Toggle")

# Initialize session state
if "response_history" not in st.session_state:
    st.session_state.response_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # Generate a new session ID
if "submit_triggered" not in st.session_state:
    st.session_state.submit_triggered = False
if "captured_input" not in st.session_state:
    st.session_state.captured_input = ""

# Button to start a new session
if st.button("Start New Session"):
    st.session_state.response_history = []
    st.session_state.session_id = str(uuid.uuid4())  # Generate a fresh session ID
    st.success("New session started. Memory has been cleared.")

# Voice output toggle
voice_enabled = st.checkbox("Enable Voice Output", value=False)

# Define a callback function for Enter key submission
def submit_on_enter():
    # Capture input before clearing for processing
    st.session_state.captured_input = st.session_state.input_field
    st.session_state.submit_triggered = True
    st.session_state.input_field = ""  # Clear the input field

# User Input Section with Enter-to-Submit and session state binding
user_input = st.text_input(
    "Ask a physics question:",
    key="input_field",
    value=st.session_state.get("input_field", ""),
    on_change=submit_on_enter
)

# Automatically handle submission when Enter is pressed
if st.session_state.submit_triggered or st.button("Submit"):
    if st.session_state.captured_input:
        response = requests.post("http://127.0.0.1:8000/query/", json={
            "input_text": st.session_state.captured_input,
            "voice_enabled": voice_enabled,
            "session_id": st.session_state.session_id  # Pass session ID
        })
        if response.status_code == 200:
            try:
                data = response.json()
                result = data.get("response", "No response from the tutor.")
                audio_file_path = data.get("audio_file")

                # Store the question and response in session state
                st.session_state.response_history.insert(0, (st.session_state.captured_input, result))

                # Display the latest response
                st.write("**Your Question:**")
                st.info(st.session_state.captured_input)
                st.write("**Tutor's Response:**")
                st.markdown(result, unsafe_allow_html=True)

                # Reset submission trigger after processing
                st.session_state.submit_triggered = False

                # Play audio if enabled
                if voice_enabled and audio_file_path:
                    audio = AudioSegment.from_file(audio_file_path)
                    play(audio)
            except requests.exceptions.JSONDecodeError:
                st.error("Failed to parse JSON from backend.")
        else:
            st.error(f"Backend error: {response.status_code}")

# Display older responses tucked away in an expandable section
if len(st.session_state.response_history) > 1:
    with st.expander("Previous Responses"):
        for i, (question, response) in enumerate(st.session_state.response_history[1:], start=1):
            st.markdown(f"**Question {len(st.session_state.response_history[1:])-i+1}:** {question}")
            st.markdown(f"**Response:** {response}")

# Speech Input Section
if st.button("Speak Your Question"):
    response = requests.get("http://127.0.0.1:8000/speech_input/")
    if response.status_code == 200:
        data = response.json()
        recognized_text = data.get("recognized_text", "Speech not recognized.")
        result = data.get("response", "No response from the tutor.")
        audio_file_path = data.get("audio_file")

        # Store the new response in session state
        st.session_state.response_history.insert(0, (recognized_text, result))

        st.write("Tutor Response:")
        st.success(result)

        # Play the audio response
        if voice_enabled and audio_file_path:
            audio = AudioSegment.from_file(audio_file_path)
            play(audio)
    else:
        st.error(f"Backend error: {response.status_code}")
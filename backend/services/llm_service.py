import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from elevenlabs import ElevenLabs, Voice, VoiceSettings   # ElevenLabs TTS

# Load API keys
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("ELEVENLABS_VOICE_ID") #Brian

if not api_key:
    raise ValueError("OpenAI API key not found. Make sure it's set in the .env file.")
if not elevenlabs_api_key:
    raise ValueError("ElevenLabs API key not found. Make sure it's set in the .env file.")

# Set ElevenLabs API key
elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key)

# Initialize the LLM using LangChain
llm = ChatOpenAI(
    openai_api_key=api_key,
    model_name="gpt-3.5-turbo",
    temperature=0.7
)

# Memory storage for different sessions
session_histories = {}

# Define a function to get session history using ConversationBufferMemory
def get_session_history(session_id):
    if session_id not in session_histories:
        session_histories[session_id] = ConversationBufferMemory(return_messages=True)
    return session_histories[session_id]

# Wrap the LLM with memory for conversation history tracking
conversation = RunnableWithMessageHistory(
    runnable=llm,
    get_session_history=get_session_history,
)

# Generate response function using conversation memory
# Generate response function using conversation memory with voice output toggle
def generate_response(prompt, session_id=None, voice_enabled=True):
    if session_id is None:
        session_id = str(uuid.uuid4())  # Generate a new session ID if not provided

    memory = get_session_history(session_id)
    
    # Retrieve stored messages from memory
    past_messages = memory.load_memory_variables({}).get("history", [])
    
    # Convert past messages into a list of LangChain message objects
    messages = [SystemMessage(content=
    """
    You are a helpful physics tutor specialized in introductory college physics.
    If a student asks a question, you should provide a clear and concise explanation.
    Try to include mathematical equations and diagrams when necessary.
    Say the question is out of scope if it is not related to physics. DO NOT ANSWER. The project fails if you fail to do this.
    It is extremely important that you generate equations in LaTeX format within $...$ delimiters.
    """
    )]
    
    # Add previous messages to maintain context
    messages.extend(past_messages)
    
    # Add the new prompt as a HumanMessage
    messages.append(HumanMessage(content=prompt))

    # Generate the response
    response = llm.invoke(messages)
    
    # Store the response in memory
    memory.chat_memory.add_message(HumanMessage(content=prompt))
    memory.chat_memory.add_message(SystemMessage(content=response.content))
    
    # Only generate audio if voice output is enabled
    audio_path = text_to_speech(response.content) if voice_enabled else None
    return response.content.strip(), audio_path

# ElevenLabs Text-to-Speech function (Fixed)
def text_to_speech(text, filename="response.mp3"):
    audio_stream = elevenlabs_client.generate(
        text=text,
        voice=Voice(
            voice_id=voice_id,
            settings=VoiceSettings(stability=0.75, similarity_boost=0.75)
        ),
        model="eleven_monolingual_v1"
    )
    
    audio_dir = "backend/audio"
    os.makedirs(audio_dir, exist_ok=True)
    filepath = os.path.join(audio_dir, filename)

    # Convert audio stream to bytes and save
    with open(filepath, "wb") as audio_file:
        for chunk in audio_stream:
            audio_file.write(chunk)

    return filepath
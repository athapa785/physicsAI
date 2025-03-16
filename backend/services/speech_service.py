import os
import enum
import speech_recognition as sr
from pathlib import Path
import tempfile
from openai import OpenAI

# Enums for TTS providers and voices
class TTSProvider(enum.Enum):
    OPENAI = "openai"
    ELEVENLABS = "elevenlabs"
    SYSTEM = "system"

class TTSVoice(enum.Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"

class SpeechService:
    def __init__(self):
        self.openai_client = None
        self.cache_dir = Path("backend/audio/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def initialize_openai(self, api_key):
        """Initialize OpenAI client with API key"""
        self.openai_client = OpenAI(api_key=api_key)
        return self.openai_client is not None
    
    def text_to_speech(self, text, output_file, voice=TTSVoice.NOVA.value, provider=TTSProvider.OPENAI.value):
        """Convert text to speech using the specified provider"""
        if provider == TTSProvider.OPENAI.value:
            return self._openai_tts(text, output_file, voice)
        else:
            # Fallback to system TTS if provider not supported
            return self._system_tts(text, output_file)
    
    def _openai_tts(self, text, output_file, voice):
        """Use OpenAI's TTS API"""
        if not self.openai_client:
            return False
        
        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            # Save to file
            response.stream_to_file(output_file)
            return True
        except Exception as e:
            print(f"Error in OpenAI TTS: {e}")
            return False
    
    def _system_tts(self, text, output_file):
        """Fallback to system TTS"""
        try:
            # This is a placeholder - would need platform-specific implementation
            print("System TTS not implemented, would convert:", text)
            return False
        except Exception as e:
            print(f"Error in system TTS: {e}")
            return False
    
    def cache_audio(self, text, filename, voice=TTSVoice.NOVA.value):
        """Cache audio for a specific text"""
        cache_path = self.cache_dir / f"{filename}_{voice}.mp3"
        if not cache_path.exists():
            return self.text_to_speech(text, str(cache_path), voice)
        return True
    
    def get_cached_path(self, filename, voice=TTSVoice.NOVA.value):
        """Get path to cached audio file"""
        cache_path = self.cache_dir / f"{filename}_{voice}.mp3"
        if cache_path.exists():
            return str(cache_path)
        return None
        
    def generate_speech(self, text, voice=TTSVoice.NOVA.value):
        """Generate speech from text and return the path to the audio file"""
        # Create a unique filename based on the text content (first 20 chars)
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:10]
        filename = f"speech_{text_hash}"
        
        # Check if we already have this audio cached
        cached_path = self.get_cached_path(filename, voice)
        if cached_path:
            return cached_path
            
        # Generate new audio file
        temp_file = os.path.join(str(self.cache_dir), f"{filename}_{voice}.mp3")
        
        # Get OpenAI API key from environment if not already initialized
        if not self.openai_client and "OPENAI_API_KEY" in os.environ:
            self.initialize_openai(os.environ["OPENAI_API_KEY"])
            
        # Generate speech
        success = self.text_to_speech(text, temp_file, voice)
        
        if success:
            return temp_file
        else:
            # Return a placeholder or error message if generation fails
            return None

def recognize_speech_from_mic():
    """Recognize speech from microphone"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for speech...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "API unavailable or too many requests."

def text_to_speech(text, output_file, voice=TTSVoice.NOVA.value, provider=TTSProvider.OPENAI.value):
    """Standalone function for text-to-speech conversion"""
    service = SpeechService()
    if provider == TTSProvider.OPENAI.value:
        # Get OpenAI API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return False
        service.initialize_openai(api_key)
    
    return service.text_to_speech(text, output_file, voice, provider)
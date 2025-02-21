from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.llm_service import generate_response
from backend.services.llm_service import generate_response, text_to_speech
from backend.services.speech_service import recognize_speech_from_mic
import uuid  
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()


# Define the expected structure of the JSON body
class QueryRequest(BaseModel):
    input_text: str

# Query endpoint
@router.post("/query/")
async def handle_query(request: dict):
    input_text = request.get("input_text")
    voice_enabled = request.get("voice_enabled", True)  # Default to True if not specified
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text is required.")
    try:
        response, audio_path = generate_response(input_text, session_id="default", voice_enabled=voice_enabled)
        return {
            "response": response,
            "audio_file": audio_path
        }
    except Exception as e:
        logging.error(f"Error in query endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/speech_input/")
async def handle_speech_input():
    try:
        session_id = str(uuid.uuid4())  # Generate a unique session ID
        recognized_text = recognize_speech_from_mic()
        response_text = generate_response(recognized_text, session_id=session_id)  # Pass session_id
        audio_path = text_to_speech(response_text)
        logging.info(f"Recognized Text: {recognized_text}")
        logging.info(f"Response Text: {response_text}")
        logging.info(f"Audio Path: {audio_path}")

        return {
            "recognized_text": recognized_text,
            "response": response_text,
            "audio_file": audio_path
        }
    except Exception as e:
        logging.error(f"Error in speech_input endpoint: {e}")
        return {"error": str(e)}
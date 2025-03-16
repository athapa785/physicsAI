"""
Endpoints for the physics learning system.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import logging
import os
from ..services.physics_service import PhysicsService
from ..services.speech_service import text_to_speech

router = APIRouter(prefix="/physics")
physics_service = PhysicsService()

class TopicRequest(BaseModel):
    chapter_number: int

class LessonRequest(BaseModel):
    topic: str
    voice_enabled: bool = True

class QuestionRequest(BaseModel):
    question: str
    topic: str
    voice_enabled: bool = True
    chat_history: List[Dict[str, str]] = []

@router.get("/chapters/")
async def get_chapters():
    """Get all chapters from University Physics."""
    try:
        chapters = physics_service.get_chapters()
        return {"chapters": chapters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cached-lessons/")
async def get_cached_lessons():
    """Get all topics that have cached lessons."""
    try:
        topics = await physics_service.lesson_storage.get_all_topics()
        return {"topics": topics}
    except Exception as e:
        logging.error(f"Error retrieving cached lessons: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topics/")
async def get_topics(request: TopicRequest):
    """Get topics for a specific chapter."""
    try:
        topics = physics_service.get_topics(request.chapter_number)
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lesson/")
async def generate_lesson(request: LessonRequest):
    """Generate a lesson for a specific topic."""
    try:
        # Create a safe filename from the topic for audio caching
        safe_topic = "".join(c if c.isalnum() else "_" for c in request.topic)
        audio_cache_dir = "backend/audio/cache"
        os.makedirs(audio_cache_dir, exist_ok=True)
        audio_cache_path = os.path.join(audio_cache_dir, f"{safe_topic}.mp3")
        
        # Get the lesson (either from cache or generate new)
        lesson = await physics_service.generate_lesson(request.topic)
        
        # Generate audio if enabled
        audio_path = None
        if request.voice_enabled:
            try:
                # Check if audio is already cached
                if os.path.exists(audio_cache_path):
                    logging.info(f"Using cached audio for topic: {request.topic}")
                    audio_path = audio_cache_path
                else:
                    logging.info(f"Generating new audio for topic: {request.topic}")
                    audio_content = text_to_speech(lesson)
                    
                    # Save audio content to cache
                    with open(audio_cache_path, "wb") as f:
                        f.write(audio_content)
                    audio_path = audio_cache_path
            except Exception as audio_error:
                logging.error(f"Error generating audio: {str(audio_error)}")
                # Continue without audio if there's an error
        
        logging.info(f"Returning lesson response for topic: {request.topic}")
        return {
            "lesson": lesson,
            "audio_file": audio_path
        }
    except Exception as e:
        logging.error(f"Exception in generate_lesson: {str(e)}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/question/")
async def answer_question(request: QuestionRequest):
    """Answer a question about a specific topic."""
    try:
        # Convert chat history to the format expected by the service
        chat_history = [(msg["user"], msg["assistant"]) for msg in request.chat_history]
        
        answer = await physics_service.answer_question(
            request.question,
            request.topic,
            chat_history
        )
        
        # Generate audio if enabled
        audio_path = None
        if request.voice_enabled:
            audio_content = text_to_speech(answer)
            # Save audio content
            os.makedirs("backend/audio", exist_ok=True)
            audio_path = os.path.join("backend/audio", "answer.mp3")
            with open(audio_path, "wb") as f:
                f.write(audio_content)
        
        return {
            "answer": answer,
            "audio_file": audio_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

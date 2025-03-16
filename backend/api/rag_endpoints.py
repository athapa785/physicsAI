"""
Endpoints for the RAG-based physics learning system.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from ..services.rag_service import PhysicsRAG
from ..services.speech_service import text_to_speech
import os

router = APIRouter(prefix="/rag")
rag_service = PhysicsRAG()

# Initialize the vector store with physics content
PHYSICS_CONTENT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "physics_content")
# Removed RAG vector store initialization as it's no longer supported

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
        chapters = rag_service.get_chapters()
        return {"chapters": chapters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topics/")
async def get_topics(request: TopicRequest):
    """Get topics for a specific chapter."""
    try:
        topics = rag_service.get_topics(request.chapter_number)
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/lesson/")
async def generate_lesson(request: LessonRequest):
    """Generate a lesson for a specific topic."""
    try:
        lesson = await rag_service.generate_lesson(request.topic)
        
        # Generate audio if enabled
        audio_path = None
        if request.voice_enabled:
            audio_content = text_to_speech(lesson)
            # Save audio content
            os.makedirs("backend/audio", exist_ok=True)
            audio_path = os.path.join("backend/audio", "lesson.mp3")
            with open(audio_path, "wb") as f:
                f.write(audio_content)
        
        return {
            "lesson": lesson,
            "audio_file": audio_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/question/")
async def answer_question(request: QuestionRequest):
    """Answer a question about a specific topic."""
    try:
        # Convert chat history to the format expected by the RAG service
        chat_history = [(msg["user"], msg["assistant"]) for msg in request.chat_history]
        
        answer = rag_service.answer_question(
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

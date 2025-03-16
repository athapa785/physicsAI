"""
Lesson storage service for caching and retrieving pre-generated lessons.
"""

import os
import json
import logging
from typing import Dict, Optional, List
import aiofiles

class LessonStorage:
    """Service for storing and retrieving pre-generated lessons."""
    
    def __init__(self, storage_dir: str = "backend/data/lessons"):
        """Initialize the lesson storage service.
        
        Args:
            storage_dir: Directory to store lesson files
        """
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.lessons_index_path = os.path.join(storage_dir, "lessons_index.json")
        self.lessons_index = self._load_index()
    
    def _load_index(self) -> Dict[str, str]:
        """Load the lessons index from disk."""
        if os.path.exists(self.lessons_index_path):
            try:
                with open(self.lessons_index_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logging.error(f"Error loading lessons index: {str(e)}")
                return {}
        return {}
    
    async def _save_index(self) -> None:
        """Save the lessons index to disk."""
        try:
            async with aiofiles.open(self.lessons_index_path, 'w') as f:
                await f.write(json.dumps(self.lessons_index, indent=2))
        except Exception as e:
            logging.error(f"Error saving lessons index: {str(e)}")
    
    def _get_lesson_path(self, topic: str) -> str:
        """Get the file path for a lesson."""
        # Create a safe filename from the topic
        safe_filename = "".join(c if c.isalnum() else "_" for c in topic)
        return os.path.join(self.storage_dir, f"{safe_filename}.md")
    
    async def get_lesson(self, topic: str) -> Optional[str]:
        """Get a lesson for a topic if it exists in storage.
        
        Args:
            topic: The topic to retrieve a lesson for
            
        Returns:
            The lesson content if found, None otherwise
        """
        if topic in self.lessons_index:
            lesson_path = self._get_lesson_path(topic)
            if os.path.exists(lesson_path):
                try:
                    async with aiofiles.open(lesson_path, 'r') as f:
                        return await f.read()
                except Exception as e:
                    logging.error(f"Error reading lesson file for {topic}: {str(e)}")
        return None
    
    async def store_lesson(self, topic: str, content: str) -> None:
        """Store a lesson for a topic.
        
        Args:
            topic: The topic the lesson is about
            content: The lesson content
        """
        lesson_path = self._get_lesson_path(topic)
        try:
            async with aiofiles.open(lesson_path, 'w') as f:
                await f.write(content)
            
            # Update the index
            self.lessons_index[topic] = lesson_path
            await self._save_index()
            logging.info(f"Stored lesson for topic: {topic}")
        except Exception as e:
            logging.error(f"Error storing lesson for {topic}: {str(e)}")
    
    async def get_all_topics(self) -> List[str]:
        """Get all topics that have stored lessons.
        
        Returns:
            List of topics with stored lessons
        """
        return list(self.lessons_index.keys())
    
    async def delete_lesson(self, topic: str) -> bool:
        """Delete a stored lesson.
        
        Args:
            topic: The topic to delete the lesson for
            
        Returns:
            True if the lesson was deleted, False otherwise
        """
        if topic in self.lessons_index:
            lesson_path = self._get_lesson_path(topic)
            if os.path.exists(lesson_path):
                try:
                    os.remove(lesson_path)
                    del self.lessons_index[topic]
                    await self._save_index()
                    logging.info(f"Deleted lesson for topic: {topic}")
                    return True
                except Exception as e:
                    logging.error(f"Error deleting lesson for {topic}: {str(e)}")
        return False

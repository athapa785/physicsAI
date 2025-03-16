"""
Settings configuration for PhysicsAI.

This module contains configuration settings for the PhysicsAI application,
including paths, API settings, and other constants.
"""

import os
from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
APP_DIR = PROJECT_ROOT / "app"
TESTS_DIR = PROJECT_ROOT / "tests"

# Data paths
DATA_DIR = BACKEND_DIR / "data"
LESSONS_DIR = DATA_DIR / "lessons"
PHYSICS_CONTENT_DIR = DATA_DIR / "physics_content"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

# Static paths
STATIC_DIR = BACKEND_DIR / "static"
CSS_FILE = STATIC_DIR / "style.css"

# API settings
DEFAULT_API_TIMEOUT = 60  # seconds
MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7

# RAG settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-3-small"
SIMILARITY_TOP_K = 5

# UI settings
DEFAULT_MODE = "browse"
AVAILABLE_MODES = ["browse", "lesson", "about", "how_to_use"]
PAGE_TITLE = "Physics Learning Assistant"
PAGE_ICON = "🔭"

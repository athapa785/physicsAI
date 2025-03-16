# PhysicsAI - Physics Education Platform

PhysicsAI is an interactive physics education platform powered by Retrieval Augmented Generation (RAG) technology. The application provides personalized physics lessons, interactive content navigation, and context-aware question answering.

## Features

- **RAG-Enhanced Physics Lessons**: Content based on University Physics textbook
- **Hierarchical Content Organization**: Chapters → Topics → Lessons
- **Interactive Navigation**: Streamlit-based user interface
- **Context-Aware Q&A**: Ask questions about physics concepts
- **Text-to-Speech Integration**: Listen to generated lessons

## Project Structure

```
physicsAI/
├── app.py                  # Main application entry point
├── config/                 # Configuration settings
├── backend/                # Backend services and data
│   ├── services/           # Core services (RAG, LLM, etc.)
│   ├── data/               # Physics content and lessons
│   │   ├── physics_content/# Organized physics text content
│   │   ├── vector_store/   # FAISS vector store persistence
│   │   └── lessons/        # Generated lesson content
├── frontend/              # Frontend components
│   ├── components/        # UI components
│   ├── pages/             # Application pages
│   ├── utils/             # Frontend utilities
│   └── static/            # CSS and static assets
└── tests/                 # Test suite
```

## Technical Components

- **Vector Store**: FAISS for efficient similarity search and persistence
- **Embeddings**: OpenAI embeddings for text vectorization
- **LLM**: GPT-4 Turbo for content generation
- **Text Splitter**: RecursiveCharacterTextSplitter for optimal chunking
- **Content Hash**: Used to detect changes in physics content and optimize embedding generation

## RAG System Architecture

The RAG system uses FAISS vector store persistence to optimize performance:

1. Physics content is organized in `/backend/data/physics_content/`
2. Vector store is saved in `/backend/data/vector_store/`
3. Content hash is used to detect changes in physics content
4. Embeddings are only recomputed when content changes
5. Vector store is automatically loaded from disk if content hasn't changed

This significantly improves startup time and reduces API calls to OpenAI.

## Running the Application

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `streamlit run app.py`
4. Enter your API keys in the sidebar
5. Navigate through chapters and topics
6. Generate lessons on specific physics concepts
7. Ask questions related to the content

## Note

This application requires API keys for OpenAI and other LLM providers to function properly. Users must provide their own API keys.

# PhysicsAI - Physics Education Platform

PhysicsAI is an interactive physics education platform powered by Retrieval Augmented Generation (RAG) technology. The application provides personalized physics lessons, interactive content navigation, and context-aware question answering.

## Features

- **RAG-Enhanced Physics Lessons**: Content based on University Physics textbook
- **Hierarchical Content Organization**: Chapters → Topics → Lessons
- **Interactive Navigation**: Streamlit-based user interface
- **Context-Aware Q&A**: Ask questions about physics concepts
- **Text-to-Speech Integration**: Listen to generated lessons

## Technical Components

- **Vector Store**: FAISS for efficient similarity search
- **Embeddings**: OpenAI embeddings for text vectorization
- **LLM**: GPT-4 Turbo for content generation
- **Text Splitter**: RecursiveCharacterTextSplitter for optimal chunking

## Usage

1. Enter your API keys in the sidebar
2. Navigate through chapters and topics
3. Generate lessons on specific physics concepts
4. Ask questions related to the content

## Note

This application requires API keys for OpenAI and other LLM providers to function properly. Users must provide their own API keys.

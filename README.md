# Physics AI

A personalized physics education platform using Retrieval Augmented Generation (RAG) for comprehensive physics learning. This application uses FAISS vector store for efficient similarity search and OpenAI embeddings for text vectorization to provide an interactive physics learning experience.

## Features

- **Interactive Learning**: Navigate through physics chapters and topics with an intuitive UI
- **RAG-Enhanced Content**: Lessons generated using University Physics textbook content and LLM capabilities
- **Context-Aware Q&A**: Ask questions about any physics topic with accurate, contextual responses
- **Vector Store Persistence**: FAISS vector store is saved to disk for improved performance
- **Hierarchical Content**: Organized by Chapters → Topics → Lessons for easy navigation

## Local Setup

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/physicsAI.git
cd physicsAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
streamlit run streamlit_app.py
```

4. Enter your OpenAI API key in the sidebar when prompted.

## Streamlit Cloud Deployment

### Prerequisites

- GitHub account
- Streamlit Cloud account (free tier available)
- OpenAI API key

### Deployment Steps

1. Fork or push this repository to your GitHub account.

2. Log in to [Streamlit Cloud](https://streamlit.io/cloud).

3. Click "New app" and select your repository.

4. Configure the app:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.9 or higher

5. Add your API keys as secrets:
   - Go to the "Advanced" section
   - Add the following to the secrets configuration:
   ```toml
   [api_keys]
   openai = "your-openai-api-key"
   anthropic = ""  # Optional
   google = ""     # Optional
   deepinfra = ""  # Optional
   ```

6. Click "Deploy" and wait for the build to complete.

7. Your Physics AI application is now live on Streamlit Cloud!

## Usage

- **Browse Mode**: Navigate through physics chapters and topics from University Physics
- **Lesson Mode**: View detailed RAG-enhanced lessons on specific physics topics
- **Q&A Mode**: Ask questions about any physics concept with context-aware responses

## RAG System Architecture

- **Vector Store**: FAISS for efficient similarity search
- **Embeddings**: OpenAI embeddings for text vectorization
- **LLM**: GPT-4 Turbo for content generation
- **Text Splitter**: RecursiveCharacterTextSplitter for optimal chunking
- **Content Organization**: Hierarchical structure (Chapters → Topics → Lessons)

## Project Structure

- `backend/`: Core backend with physics content and RAG implementation
  - `data/`: Physics content and vector store
    - `physics_content/`: Text files containing physics content
    - `vector_store/`: FAISS vector store for efficient retrieval
  - `services/`: Core services (physics, RAG, LLM integration)
- `streamlit_app.py`: Main Streamlit application

## Physics Content

Physics content is organized in `/backend/data/physics_content/` with the following structure:
- Text files (.txt) containing sections from University Physics textbook
- Each file focuses on a specific topic or concept
- Files are named descriptively (e.g., kinematics_motion.txt, forces_newtons_laws.txt)
- Content is preprocessed to preserve mathematical equations in LaTeX format

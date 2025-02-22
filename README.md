# Physics Tutor

A personalized tutor using LLMs for introductory college physics. Built with FastAPI backend and Streamlit frontend.

## Setup

1. Install dependencies:
```
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

2. Add your OpenAI API key to the `.env` file.

3. Run the backend:
```
uvicorn backend.main:app --reload
```

4. Run the frontend:
```
streamlit run frontend/app.py
```

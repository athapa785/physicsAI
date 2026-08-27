# Physics Atlas

Physics Atlas is an interactive undergraduate physics library. The revived app
uses React for a fast, focused reading experience and FastAPI to serve the
project's original course material.

## What works

- Six physics domains and 18 bundled lessons
- Topic search and responsive chapter browsing
- Section-by-section lesson navigation
- Markdown and LaTeX equation rendering
- Optional, course-grounded AI follow-up questions
- Fully usable lesson library without an API key

## Architecture

```text
src/                              React application
backend/main.py                   FastAPI content and Q&A API
backend/data/lessons/             Curated lesson Markdown
backend/data/physics_content/     Source course notes
tests/test_smoke.py               Offline API smoke tests
```

The previous Streamlit UI has been retired. Some older experimental services
remain under `backend/services/` as reference material, but they are not loaded
by the maintained application.

## Run locally

Python 3.11+ and Node.js 20+ are recommended.

Start the API:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn backend.main:app --reload
```

In a second terminal, start the web app:

```bash
npm install
npm run dev
```

Open `http://localhost:5173`.

## Optional AI tutor

The lesson library works offline. To enable “Ask the atlas,” provide a key to
the API process:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_MODEL="your-model"  # optional
uvicorn backend.main:app --reload
```

Keep credentials in your local environment; never commit real keys.

## Verify

```bash
.venv/bin/python -m unittest tests.test_smoke
npm run build
```

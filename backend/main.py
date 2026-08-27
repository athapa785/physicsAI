import os
import re
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "backend" / "data" / "physics_content"
LESSONS_DIR = ROOT / "backend" / "data" / "lessons"

CHAPTERS = {
    "mechanics": (1, "Mechanics"),
    "thermodynamics": (2, "Thermodynamics"),
    "waves_oscillations": (3, "Waves & Oscillations"),
    "electromagnetism": (4, "Electromagnetism"),
    "optics": (5, "Optics"),
    "modern_physics": (6, "Modern Physics"),
}


class QuestionRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
    topic: str = Field(default="physics lab", min_length=2, max_length=120)
    lab: Optional[str] = Field(default=None, max_length=120)
    state: Dict[str, Any] = Field(default_factory=dict)
    history: List[Dict[str, str]] = Field(default_factory=list, max_length=12)


def display_name(path: Path) -> str:
    return path.stem.replace("_", " ").title()


def slug_for(path: Path) -> str:
    return path.stem.replace("_", "-")


def find_topic(slug: str) -> Optional[Path]:
    normalized = slug.lower().replace("-", "_")
    matches = list(CONTENT_DIR.glob(f"*/{normalized}.txt"))
    return matches[0] if matches else None


def lesson_path(topic_path: Path) -> Path:
    return LESSONS_DIR / f"{topic_path.stem.title()}.md"


app = FastAPI(title="PhysicsAI API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "lessons": len(list(LESSONS_DIR.glob("*.md")))}


@app.get("/api/catalog")
def catalog():
    chapters = []
    for directory, (number, title) in CHAPTERS.items():
        topics = []
        for path in sorted((CONTENT_DIR / directory).glob("*.txt")):
            cached = lesson_path(path).is_file()
            topics.append(
                {
                    "slug": slug_for(path),
                    "title": display_name(path),
                    "hasLesson": cached,
                }
            )
        chapters.append({"number": number, "title": title, "topics": topics})
    return {"chapters": chapters}


@app.get("/api/search")
def search(q: str = Query(min_length=2, max_length=120)):
    """Search topic names and the complete local lesson/source corpus."""
    query = q.strip().lower()
    terms = [term for term in re.findall(r"[a-z0-9]+", query) if len(term) > 1]
    results = []

    for topic_path in CONTENT_DIR.glob("*/*.txt"):
        title = display_name(topic_path)
        cached_path = lesson_path(topic_path)
        source_text = topic_path.read_text(encoding="utf-8")
        lesson_text = cached_path.read_text(encoding="utf-8") if cached_path.is_file() else ""
        searchable = f"{title}\n{source_text}\n{lesson_text}".lower()
        if not terms or not all(term in searchable for term in terms):
            continue

        title_lower = title.lower()
        score = sum(20 if term in title_lower else searchable.count(term) for term in terms)
        first_positions = [searchable.find(term) for term in terms if searchable.find(term) >= 0]
        position = min(first_positions) if first_positions else 0
        raw_text = f"{source_text}\n{lesson_text}"
        start = max(0, position - 90)
        end = min(len(raw_text), position + 190)
        snippet = re.sub(r"[#*$`_>\n]+", " ", raw_text[start:end])
        snippet = re.sub(r"\s+", " ", snippet).strip()
        if start > 0:
            snippet = f"…{snippet}"
        if end < len(raw_text):
            snippet = f"{snippet}…"

        results.append(
            {
                "slug": slug_for(topic_path),
                "title": title,
                "chapter": CHAPTERS[topic_path.parent.name][1],
                "snippet": snippet,
                "score": score,
            }
        )

    results.sort(key=lambda result: (-result["score"], result["title"]))
    return {"query": q, "results": results[:20]}


@app.get("/api/lessons/{slug}")
def lesson(slug: str):
    topic_path = find_topic(slug)
    if not topic_path:
        raise HTTPException(status_code=404, detail="Topic not found")

    cached_path = lesson_path(topic_path)
    source = cached_path if cached_path.is_file() else topic_path
    return {
        "slug": slug_for(topic_path),
        "title": display_name(topic_path),
        "chapter": CHAPTERS[topic_path.parent.name][1],
        "content": source.read_text(encoding="utf-8"),
        "isCuratedLesson": cached_path.is_file(),
    }


@app.post("/api/ask")
def ask(
    request: QuestionRequest,
    x_openai_api_key: Optional[str] = Header(default=None),
    x_student_session: Optional[str] = Header(default=None),
):
    api_key = x_openai_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="Q&A is not configured on this server")

    from openai import OpenAI

    topic_path = find_topic(request.topic)
    context = topic_path.read_text(encoding="utf-8")[:16000] if topic_path else ""
    lab_name = request.lab or request.topic
    state_lines = "\n".join(f"- {key}: {value}" for key, value in request.state.items())
    history = request.history[-8:]
    conversation = [
        {"role": item.get("role", "user"), "content": item.get("content", "")}
        for item in history
        if item.get("role") in {"user", "assistant"} and item.get("content")
    ]
    conversation.append(
        {
            "role": "user",
            "content": (
                f"Current lab: {lab_name}\nCurrent simulation state:\n{state_lines or '- no parameters'}"
                f"\n\nStudent question: {request.question}"
                + (f"\n\nReference notes:\n{context}" if context else "")
            ),
        }
    )
    client = OpenAI(api_key=api_key)
    session_hash = hashlib.sha256((x_student_session or "anonymous-lab-session").encode()).hexdigest()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.6-terra"),
        instructions=(
            "You are a Socratic undergraduate physics lab coach. Ground every response in the "
            "current simulation state. Help the student connect the visual, graph, equation, and "
            "physical intuition. For problem-solving, give one useful step or question at a time "
            "instead of dumping a complete solution. If the student asks for a direct explanation, "
            "answer clearly, then suggest one parameter change they can try in the lab. Use concise "
            "Markdown and LaTeX. Never claim the simulation measured something not present in state."
        ),
        input=conversation,
        reasoning={"effort": "low"},
        text={"verbosity": "medium"},
        safety_identifier=session_hash,
    )
    answer = response.output_text
    if not answer:
        raise HTTPException(status_code=502, detail="The model returned an empty answer")
    return {"answer": answer}


@app.get("/")
def root():
    return {"message": "PhysicsAI API", "docs": "/docs"}

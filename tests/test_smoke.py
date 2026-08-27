import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app


class PhysicsApiSmokeTests(unittest.TestCase):
    def setUp(self):
        # Keep smoke tests offline even if the developer has local credentials.
        self.openai_key = os.environ.pop("OPENAI_API_KEY", None)
        self.anthropic_key = os.environ.pop("ANTHROPIC_API_KEY", None)
        self.client = TestClient(app)

    def tearDown(self):
        if self.openai_key is not None:
            os.environ["OPENAI_API_KEY"] = self.openai_key
        if self.anthropic_key is not None:
            os.environ["ANTHROPIC_API_KEY"] = self.anthropic_key

    def test_catalog_contains_all_chapters_and_topics(self):
        response = self.client.get("/api/catalog")
        self.assertEqual(200, response.status_code)
        chapters = response.json()["chapters"]

        self.assertEqual(6, len(chapters))
        self.assertEqual(18, sum(len(chapter["topics"]) for chapter in chapters))

    def test_bundled_lesson_loads_without_api_key(self):
        response = self.client.get("/api/lessons/circular-motion")
        self.assertEqual(200, response.status_code)
        self.assertIn("## Introduction", response.json()["content"])

    def test_unknown_topic_returns_not_found(self):
        response = self.client.get("/api/lessons/not-a-topic")
        self.assertEqual(404, response.status_code)

    def test_search_scans_document_content(self):
        response = self.client.get("/api/search", params={"q": "centripetal acceleration"})
        self.assertEqual(200, response.status_code)
        slugs = [result["slug"] for result in response.json()["results"]]
        self.assertIn("circular-motion", slugs)

    def test_qa_explains_when_it_is_not_configured(self):
        response = self.client.post(
            "/api/ask",
            json={"topic": "circular-motion", "question": "What points inward?"},
        )
        self.assertEqual(503, response.status_code)

    @patch("openai.OpenAI")
    def test_lab_coach_receives_simulation_state(self, openai_client):
        create = openai_client.return_value.responses.create
        create.return_value = SimpleNamespace(output_text="Start with the force parallel to the incline.")
        response = self.client.post(
            "/api/ask",
            headers={"X-OpenAI-API-Key": "sk-test", "X-Student-Session": "student-1"},
            json={
                "topic": "forces-newtons-laws",
                "lab": "Forces on an incline",
                "question": "What should I calculate first?",
                "state": {"mass_kg": 8, "incline_angle_deg": 28},
                "history": [],
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("parallel", response.json()["answer"])
        call = create.call_args.kwargs
        self.assertEqual("gpt-5.6-terra", call["model"])
        self.assertIn("incline_angle_deg: 28", call["input"][-1]["content"])


if __name__ == "__main__":
    unittest.main()

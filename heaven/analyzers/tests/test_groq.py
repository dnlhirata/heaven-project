from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase
from groq._exceptions import AuthenticationError

from analyzers.clients.groq import GroqClient


class TestGroqClient(SimpleTestCase):
    @patch("analyzers.clients.groq.Groq")
    @patch("django.conf.settings.GROQ_APIKEY", "fake_api_key")
    def test_generate_questions_success(self, mock_groq):
        mock_client = mock_groq.return_value
        mock_chat = mock_client.chat
        mock_completions = mock_chat.completions
        mock_create = mock_completions.create
        mock_create.return_value.choices = [
            MagicMock(
                message=MagicMock(
                    content="Here are the questions: $Question 1?$Question 2?$Question 3?"
                )
            )
        ]

        client = GroqClient()
        chunk = "This is a test chunk of text."
        questions, status_code = client.generate_questions(chunk)

        self.assertEqual(status_code, 200)
        self.assertEqual(questions, ["Question 1?", "Question 2?", "Question 3?"])

    @patch("analyzers.clients.groq.Groq")
    @patch("django.conf.settings.GROQ_APIKEY", "fake_api_key")
    def test_generate_questions_failure(self, mock_groq):
        mock_client = mock_groq.return_value
        mock_chat = mock_client.chat
        mock_completions = mock_chat.completions
        mock_create = mock_completions.create
        mock_create.side_effect = AuthenticationError(
            "API Error", response=MagicMock(status_code=401), body={}
        )

        client = GroqClient()
        chunk = "This is a test chunk of text."
        message, status_code = client.generate_questions(chunk)

        self.assertEqual(
            message,
            "Failed to generate questions. Please try again later. If the problem persists, contact support.",
        )
        self.assertEqual(status_code, 401)

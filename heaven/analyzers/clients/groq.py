import logging
import re

from django.conf import settings
from groq import Groq

logger = logging.getLogger("django")


class GroqClient:
    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_APIKEY,
        )
        self.model = "llama3-8b-8192"

    def generate_questions(self, chunk):
        content = (
            "This is a portion of a book. Generate a set of thoughtful "
            "questions based on this section to help a reader better "
            "understand its content and implications:"
            f"{chunk}"
            "Provide at least 3-5 questions. Start each question with '$' symbol"
        )

        try:
            chat_completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": content},
                ],
            )
            content = chat_completion.choices[0].message.content
            pattern = r"\$(.*?)(?=\$|$)"
            questions = re.findall(pattern, content, re.DOTALL)
            return (
                [q.replace("\n", " ").strip() for q in questions],
                200,
            )
        except Exception as e:
            logger.error(f"Error generating questions: {e}")
            return (
                "Failed to generate questions. Please try again later. If the problem persists, contact support.",
                e.status_code,
            )

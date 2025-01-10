from django.conf import settings
from groq import Groq


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
        chat_completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": content},
            ],
        )
        return chat_completion.choices[0].message.content

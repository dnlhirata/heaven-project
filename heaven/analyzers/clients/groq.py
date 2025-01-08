from groq import Groq


class GroqClient:
    def __init__(self):
        self.client = Groq(api_key='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')
        self.model = 'llama3-8b-8192'

    def initiate_summary(self, number_of_chunks: int) -> None:
        messages = [
            {
                "role": 'user',
                'content': f'I splitted a large content into {number_of_chunks} chunks and I need you to summarize after I send them all. I will send them one by one. Please wait until I say you can summarize.',
            },
        ]
        chat_completion = self.client.chat.completions.create(messages=messages, model=self.model)
        print(chat_completion.choices[0].message.content)
    
    def send_content_chunk(self, chunk_number: int, chunk_content: str) -> None:
        messages = [
            {
                "role": 'user',
                'content': f'Chunk {chunk_number}: {chunk_content}',
            },
        ]

        chat_completion = self.client.chat.completions.create(messages=messages, model=self.model)
        print(chat_completion.choices[0].message.content)
    
    def summarize_content(self) -> str:
        messages = [
            {
                "role": 'user',
                'content': 'I sent all the chunks. Please summarize the content.',
            },
        ]
        chat_completion = self.client.chat.completions.create(messages=messages, model=self.model)
        return chat_completion.choices[0].message.content
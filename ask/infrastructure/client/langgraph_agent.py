import os
from openai import OpenAI

class LangGraphAgent:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def ask(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

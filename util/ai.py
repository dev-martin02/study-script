import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)


class AIAgent:
    """Simple wrapper around the configured chat completion client."""

    def __init__(self, model: str = "deepseek-chat") -> None:
        self.model = model

    def generate_content(
        self,
        instruction: str,
        contents: str,
        response_format: dict | None = None,
    ) -> str:
        kwargs = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": contents},
                {"role": "user", "content": instruction},
            ],
            "stream": False,
        }

        if response_format:
            kwargs["response_format"] = response_format

        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content
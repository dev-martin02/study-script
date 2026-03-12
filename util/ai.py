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


def intelligent_sorting(folders: list[str], content: str) -> str:
    folder_names = ", ".join(folders)
    instruction = (
        "You are an expert organizing content. Review the file content and choose the best folder "
        f"from this list: {folder_names}. "
        "If none fits, suggest a new folder name and set create_one to true. "
        "Return JSON only in this format: "
        '{"folder_name": "String", "create_one": "Boolean"}'
    )

    return AIAgent().generate_content(
        instruction=instruction,
        contents=content,
        response_format={"type": "json_object"},
    )
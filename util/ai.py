import os
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

# Centralized client configuration for DeepSeek
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/v1"
)

class AIAgent:
    """
    A base agent class that can be used from any file.
    Defaulted to DeepSeek configuration.
    """
    def __init__(self, model="deepseek-chat"):
        self.model = model

    def generate_content(self, instruction: str, contents: str, response_format=None) -> str: 
        kwargs = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": contents},
                {"role": "user", "content": instruction},
            ],
            "stream": False
        }
        
        if response_format:
            kwargs["response_format"] = response_format
        
        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

MODEL_MAP = {
    "llama3.2": "openai/gpt-oss-20b",
    "mistral": "openai/gpt-oss-120b",
    "gemma2": "qwen/qwen3.6-27b"
}

class GroqClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, model_name: str, query: str) -> dict:
        groq_model = MODEL_MAP.get(model_name, "openai/gpt-oss-20b")
        try:
            response = self.client.chat.completions.create(
                model=groq_model,
                messages=[{"role": "user", "content": query}],
                max_tokens=1024
            )
            return {
                "model": model_name,
                "response": response.choices[0].message.content,
                "success": True
            }
        except Exception as e:
            return {
                "model": model_name,
                "response": str(e),
                "success": False
            }

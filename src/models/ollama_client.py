import ollama
from src.models.model_profiles import get_model_profile

class OllamaClient:
    def __init__(self):
        self.client = ollama.Client()

    def generate(self, model_name: str, query: str) -> dict:
        profile = get_model_profile(model_name)
        if not profile:
            return {"error": f"Model {model_name} not found"}

        try:
            response = self.client.chat(
                model=profile.model_id,
                messages=[{"role": "user", "content": query}]
            )
            return {
                "model": profile.name,
                "response": response.message.content,
                "success": True
            }
        except Exception as e:
            return {
                "model": model_name,
                "response": str(e),
                "success": False
            }

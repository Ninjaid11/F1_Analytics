from google import genai
from google.genai import types
from src.config import get_settings

class LLMService:

    def __init__(self):
        settings = get_settings()
        self.model = genai.Client(api_key=settings.API_KEY)
        self.model_name = "gemini-2.5-flash"

    def generate(self, system_instruction: str, user_prompt: str, temperature: float = 0.8, top_p: float = 0.6, max_output_tokens: int = 6000):
        prompt = [
            types.Content(
                role="user",
                parts=[types.Part(text=user_prompt)]
            )
        ]

        response = self.model.models.generate_content(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_output_tokens
            ),
            contents=prompt,
        )

        print(response.text)
        return response.text

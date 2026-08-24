from google import genai
from google.genai import types
from app.core.config import settings
from app.models.knowledge import KbItem
from typing import List

class LlmService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            self.client = None

    async def generate_answer(self, query: str, context_items: List[KbItem], language: str) -> str:
        if not self.client:
            return "Error: Gemini API key is not configured on the server."

        # Prepare context from Knowledge Base
        context_text = "\n\n".join([f"Material: {item.title}\nContent: {item.content}" for item in context_items])

        system_instruction = f"""You are a helpful religious assistant for the IBODAT app.
Your task is to answer the user's question ONLY using the provided verified materials from the Knowledge Base.
Rules:
1. Answer in the requested language: {language}.
2. Use ONLY the provided materials. Do not use your internal knowledge for religious facts.
3. If the materials do not contain the answer, say that you don't have enough information.
4. Be respectful, calm, and professional.
5. Do not invent hadiths, verses, or sources.
"""

        user_message = f"Verified Materials from Knowledge Base:\n{context_text}\n\nUser Question: {query}"

        try:
            # Using the new Google GenAI SDK v1 (google-genai)
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1,
                    max_output_tokens=500
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error connecting to Gemini service: {str(e)}"

llm_service = LlmService()

from openai import AsyncOpenAI
from app.core.config import settings
from app.models.knowledge import KbItem
from typing import List

class LlmService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

    async def generate_answer(self, query: str, context_items: List[KbItem], language: str) -> str:
        if not self.client:
            return "Error: AI API key is not configured on the server."

        # Prepare context from Knowledge Base
        context_text = "\n\n".join([f"Material: {item.title}\nContent: {item.content}" for item in context_items])

        system_prompt = f"""You are a helpful religious assistant for the IBODAT app.
Your task is to answer the user's question ONLY using the provided verified materials from the Knowledge Base.
Rules:
1. Answer in the requested language: {language}.
2. Use ONLY the provided materials. Do not use your internal knowledge for religious facts.
3. If the materials do not contain the answer, say that you don't have enough information.
4. Be respectful, calm, and professional.
5. Do not invent hadiths, verses, or sources.
"""

        user_message = f"Verified Materials:\n{context_text}\n\nUser Question: {query}"

        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.3, # Low temperature for factual accuracy
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error connecting to AI service: {str(e)}"

llm_service = LlmService()

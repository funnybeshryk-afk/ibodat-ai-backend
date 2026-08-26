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

        # Prepare context from Knowledge Base (may be empty — that's fine now)
        context_text = "\n\n".join(
            [f"Material: {item.title}\nContent: {item.content}" for item in context_items]
        )
        if context_text:
            context_block = f"Verified Materials from Knowledge Base (prefer these when relevant):\n{context_text}"
        else:
            context_block = "No matching materials were found in the Knowledge Base for this question."

        system_instruction = f"""You are "IBODAT Yordamchi", a helpful general-purpose AI assistant built into the IBODAT app (a prayer-times / Islamic lifestyle app for Uzbek users). You are NOT limited to a fixed knowledge base — you can and should answer questions on any topic the user asks about (religion, daily life, general knowledge, practical advice, etc.), using your own knowledge just like a normal AI assistant would.

Rules:
1. Answer in the requested language: {language}.
2. If verified Knowledge Base materials are provided below and are relevant to the question, prefer and prioritize them, and you may quote them directly (they are trusted/verified).
3. If no Knowledge Base materials are provided, or they are not relevant, answer anyway using your own general knowledge. Do not refuse to answer and do not say "I don't have information" just because the Knowledge Base had nothing — the Knowledge Base is only a small supplementary set of curated items, not your only source.
4. Be respectful, calm, and professional, especially on religious and sensitive topics.
5. Special care for concrete fiqh rulings (e.g. specific halal/haram determinations, exact ayah or hadith citations, precise numbers/wording of a religious text): only cite a specific ayah, hadith, or source if you are confident it is accurate. Never invent or fabricate a citation, reference number, or exact wording. If you are not fully certain of an exact citation, say so plainly and give your best general understanding, and add a brief, natural reminder that for an exact ruling the user should double-check with a qualified scholar (alim) or local mufti — keep this reminder short and do not repeat it for every message or attach it to unrelated (non-fiqh) questions.
6. For everyday, factual, or non-religious questions, just answer normally and helpfully, without any religious caveats.
"""

        user_message = f"{context_block}\n\nUser Question: {query}"

        try:
            # Using the new Google GenAI SDK v1 (google-genai)
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                    max_output_tokens=800
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Error connecting to Gemini service: {str(e)}"

llm_service = LlmService()

from app.models.ai import AiQuestion, AiAnswer, AiSource
from app.services.knowledge_base import knowledge_base
from app.services.llm_service import llm_service

class AiService:
    async def get_answer(self, question: AiQuestion) -> AiAnswer:
        # 1. Search the knowledge base
        kb_results = knowledge_base.search(question.query, question.language)

        # 2. If no info found, return early
        if not kb_results:
            return AiAnswer(
                text=self._get_not_found_text(question.language),
                sources=[],
                status="NO_INFORMATION"
            )

        # 3. Use LLM to synthesize the answer using found materials
        ai_text = await llm_service.generate_answer(
            query=question.query,
            context_items=kb_results,
            language=question.language
        )

        # 4. Prepare sources
        sources = [
            AiSource(
                title=item.title,
                reference=item.sourceReference,
                url=None
            ) for item in kb_results
        ]

        return AiAnswer(
            text=ai_text,
            sources=sources,
            status="SUCCESS"
        )

    def _get_not_found_text(self, language: str) -> str:
        if language == "uz":
            return "Kechirasiz, ushbu savol bo'yicha ma'lumot topilmadi. Yordamchi bazasi doimiy ravishda boyitib boriladi."
        elif language == "ru":
            return "К сожалению, информация по данному вопросу не найдена. База помощника постоянно пополняется."
        else:
            return "Sorry, no information found for this question. The assistant's database is constantly being updated."

ai_service = AiService()

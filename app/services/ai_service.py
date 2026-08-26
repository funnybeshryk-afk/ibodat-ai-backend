from app.models.ai import AiQuestion, AiAnswer, AiSource
from app.services.knowledge_base import knowledge_base
from app.services.llm_service import llm_service

class AiService:
    async def get_answer(self, question: AiQuestion) -> AiAnswer:
        # 1. Search the knowledge base (used as optional grounding context,
        # not as a gate on whether we answer at all).
        kb_results = knowledge_base.search(question.query, question.language)

        # 2. Always ask the LLM. If we found relevant KB materials, pass them
        # in as verified context it should prefer; if not, it still answers
        # from its own general knowledge (with a fiqh caveat baked into the
        # system prompt for concrete religious rulings).
        ai_text = await llm_service.generate_answer(
            query=question.query,
            context_items=kb_results,
            language=question.language
        )

        # 3. Prepare sources (only present when we actually had KB matches)
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

ai_service = AiService()

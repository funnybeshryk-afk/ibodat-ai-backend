from fastapi import APIRouter, HTTPException
from app.models.ai import AiQuestion, AiAnswer
from app.services.ai_service import ai_service

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "IBODAT AI Backend"}

@router.post("/ai/ask", response_model=AiAnswer)
async def ask_ai(question: AiQuestion):
    try:
        return await ai_service.get_answer(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

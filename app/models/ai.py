from pydantic import BaseModel
from typing import List, Optional

class AiSource(BaseModel):
    title: str
    reference: Optional[str] = None
    url: Optional[str] = None

class AiQuestion(BaseModel):
    query: str
    userId: Optional[str] = None
    language: str = "uz"

class AiAnswer(BaseModel):
    text: str
    sources: List[AiSource] = []
    status: str = "SUCCESS"

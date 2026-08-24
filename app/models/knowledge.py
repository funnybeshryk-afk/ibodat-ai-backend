from pydantic import BaseModel
from typing import List, Optional

class KbItem(BaseModel):
    id: str
    title: str
    category: str
    content: str
    language: str = "uz"
    source: str
    sourceReference: Optional[str] = None
    verified: bool = True

from pydantic import BaseModel
from typing import Dict, List, Literal

class ChatMessage(BaseModel):
    role: Literal['user', 'assistant']
    content: str

class SearchRequest(BaseModel):
    query: str
    history: List[ChatMessage] = []
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    text: str
    metadata: Dict
    score: float

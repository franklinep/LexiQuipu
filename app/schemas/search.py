from pydantic import BaseModel
from typing import Dict

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    text: str
    metadata: Dict
    distance: float

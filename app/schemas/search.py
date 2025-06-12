from pydantic import BaseModel
from typing import Dict, List

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    text: str
    metadata: Dict
    distance: float

class GeneratedResponse(BaseModel): # respuesta generada por la LLM basado en la query
    generated_answer: str
    source_documents:List[SearchResult]

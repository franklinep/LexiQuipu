from fastapi import APIRouter
from app.schemas.search import SearchRequest, SearchResult
from app.crud.vector_query import search_documents

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=list[SearchResult])
def perform_search(request: SearchRequest):
    return search_documents(query=request.query, top_k=request.top_k)

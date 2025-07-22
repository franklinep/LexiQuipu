from fastapi import APIRouter
from app.schemas.search import SearchRequest, SearchResult
from app.crud.vector_query import search_documents
from app.services.generative_ai import stream_answer_from_context 
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=list[SearchResult])
def perform_search(request: SearchRequest):
    return search_documents(query=request.query, top_k=request.top_k)

@router.post("/generate") # Eliminamos el response_model porque StreamingResponse no funciona bien con él
def perform_generation_stream(request: SearchRequest):
    """
    Endpoint para el RAG completo con streaming.
    1. Busca documentos relevantes.
    2. Pasa los documentos y la query a la LLM (Gemini).
    3. Transmite la respuesta del LLM en tiempo real.
    """
    # Busca los documentos relevantes
    relevant_docs = search_documents(query=request.query, top_k=request.top_k)

    # Obtiene el generador de respuesta de la LLM
    response_generator = stream_answer_from_context(request.query, request.history, relevant_docs)

    # Retorna la respuesta como un stream
    return StreamingResponse(response_generator, media_type="text/event-stream")

from fastapi import APIRouter
from app.schemas.search import SearchRequest, SearchResult, GeneratedResponse
from app.crud.vector_query import search_documents
from app.services.generative_ai import generate_answer_from_context

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("/", response_model=list[SearchResult])
def perform_search(request: SearchRequest):
    return search_documents(query=request.query, top_k=request.top_k)

@router.post("/generate", response_model=GeneratedResponse)
def perform_generation(request: SearchRequest):
    """
    Endpoint para el RAG completo: busca documentos y genera una respuesta basado en la query del usuario
    pero suporteada por una LLM.
    """

    # Busca documentos relevantes desde la base de datos vectorizada
    relevant_docs = search_documents(query=request.query, top_k=request.top_k)

    # Genera una respuesta de un LLM basada en el contexto   
    answer = generate_answer_from_context(request.query, relevant_docs)

    # Retorna la respuesta generada y los documentos fuente
    return GeneratedResponse(
        generated_answer=answer,
        source_documents=relevant_docs
    )

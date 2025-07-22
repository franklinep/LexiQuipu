from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
import chromadb
from app.schemas.search import SearchResult
import os
from dotenv import load_dotenv

def search_documents(query: str, top_k: int) -> list[SearchResult]:
    """
    Busca documentos relevantes en el índice vectorial utilizando embeddings de Google.
    """
    # 1. Cargamos la API Key y configurar el modelo de embedding
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada.")

    embed_model = GoogleGenAIEmbedding(
        model_name="models/embedding-001",
        api_key=api_key
    )
    Settings.embed_model = embed_model

    # 2. Conectamos a la base de datos y obtenemos el índice
    db = chromadb.PersistentClient(path="./db")
    chroma_collection = db.get_or_create_collection("lexiquipu")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(vector_store)

    # 3. Realizamos la búsqueda
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(query)

    # 4. Formateamos y devolvemos los resultados
    return [
        SearchResult(
            id=node.id_,
            text=node.get_content(),
            metadata=node.metadata,
            score=node.score  # Usar score en lugar de distance
        )
        for node in nodes
    ]

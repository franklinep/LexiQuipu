from app.utils.embedding_model import embedding_model
from app.external_services.chromadb_client import collection
from app.schemas.search import SearchResult

def search_documents(query: str, top_k: int) -> list[SearchResult]:
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    return [
        SearchResult(
            id=results["ids"][0][i],
            text=results["documents"][0][i],
            metadata=results["metadatas"][0][i],
            distance=results["distances"][0][i]
        )
        for i in range(len(results["ids"][0]))
    ]

from app.schemas.search import SearchResult
from typing import List

def generate_answer_from_context(query: str, search_results: List[SearchResult]) -> str:
    """
        Formula un prompt para la LLM para generar una respuesta basada en los resultados de la búsqueda
    """

    context = "\n\n----------\n\n".join([result.text for result in search_results])

    prompt = f"""
    Basado estrictamente en el siguiente contexto de sentencias judiciales peruanas, 
    responde a la pregunta del usuario de manera clara y concisa.

    Contexto:
    {context}

    Pregunta: {query}

    Respuesta:
    """

    # Queda pendiente el uso de un modelo de LLM para generar la respuesta

    top_result_metadata = search_results[0].metadata if search_results else {}
    n_casacion = top_result_metadata.get("n_casacion", "desconocido")

    simulated_answer = (
        f"Según la jurisprudencia analizada, en relación a '{query}', "
        f"se destaca la Casación N° {n_casacion}. Los documentos indican que este tema "
        "se trata en el contexto de la desnaturalización de contratos y el reconocimiento de "
        "derechos laborales, siendo un punto central en varias decisiones judiciales."
    )

    return simulated_answer

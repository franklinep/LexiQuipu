from app.schemas.search import SearchResult
from typing import List, Generator
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY no esta configurada en el archivo .env")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash-latest')


def stream_answer_from_context(query: str, search_results: List[SearchResult]) -> Generator[str, None, None]:
    """
    Formula un prompt y transmite la respuesta de la LLM en chunks (token a token).
    Esta es una función generadora.
    """
    if not search_results:
        yield "No encontré información relevante en la base de datos de jurisprudencia para responder a tu pregunta. Por favor, intenta con otra consulta."
        return

    context = "\n\n---\n\n".join([result.text for result in search_results])

    prompt = f"""
    Eres un asistente legal experto en jurisprudencia peruana llamado LexiQuipu.
    Basado ESTRICTAMENTE en el siguiente contexto de sentencias judiciales peruanas, responde a la pregunta del usuario.
    Tu respuesta debe ser clara, concisa y profesional. No inventes información que no esté en el contexto.
    Si la respuesta no se encuentra en el contexto, indica que no tienes suficiente información en los documentos proporcionados.

    Contexto:
    {context}

    Pregunta: {query}

    Respuesta:
    """

    try:
        # Usamos stream=True para obtener la respuesta en tiempo real
        response_stream = model.generate_content(prompt, stream=True)

        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        print(f"Error al generar la respuesta con Gemini: {e}")
        yield "Hubo un error al comunicarse con el modelo de lenguaje. Por favor, intente más tarde."
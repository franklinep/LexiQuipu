from app.schemas.search import SearchResult, ChatMessage
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


def format_history_for_prompt(history: List[ChatMessage]) -> str:
    """Formatea el historial de chat en un string para el prompt."""
    if not history:
        return "No hay historial previo en esta conversación."
    
    formatted_history = ""
    for msg in history:
        role = "Tú" if msg.role == 'user' else "LexiQuipu"
        formatted_history += f"{role}: {msg.content}\n\n"
    return formatted_history


def stream_answer_from_context(query: str, history: List[ChatMessage], search_results: List[SearchResult]) -> Generator[str, None, None]:
    """
    Genera y transmite una respuesta de la LLM, ahora con memoria conversacional.
    """
    if not search_results:
        yield "No encontré información relevante en mi base de datos para responder a tu pregunta. Por favor, intenta con otra consulta."
        return

    context = "\n\n---\n\n".join([result.text for result in search_results])
    formatted_history = format_history_for_prompt(history)

    prompt = f"""
    Eres un asistente legal experto en jurisprudencia peruana llamado LexiQuipu.
    Tu tarea es responder las preguntas del usuario basándote en dos fuentes de información: 
    1. El historial de la conversación actual.
    2. El contexto de sentencias judiciales peruanas que se proporciona a continuación.
    
    Responde de manera clara, concisa y profesional. No inventes información. Si la respuesta no se encuentra en el contexto o en el historial, indícalo.

    ---
    HISTORIAL DE LA CONVERSACIÓN:
    {formatted_history}
    ---
    CONTEXTO DE DOCUMENTOS RELEVANTES PARA LA PREGUNTA ACTUAL:
    {context}
    ---

    PREGUNTA ACTUAL: {query}

    Respuesta:
    """

    try:
        response_stream = model.generate_content(prompt, stream=True)
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        print(f"Error al generar la respuesta con Gemini: {e}")
        yield "Hubo un error al comunicarme con el modelo de lenguaje. Por favor, intente más tarde."
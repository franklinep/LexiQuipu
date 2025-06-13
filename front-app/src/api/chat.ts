import { ChatMessage } from "../types/chat";
/**
 * Llama al endpoint de generación de chat y maneja el stream.
 * @param query La pregunta del usuario.
 * @param onToken Callback que se ejecuta con cada nuevo trozo de texto (token).
 * @param onComplete Callback que se ejecuta cuando el stream ha terminado.
 * @param onError Callback que se ejecuta si hay un error.
 */
export async function streamChat(
    query: string,
    history: ChatMessage[],
    onToken: (token: string) => void,
    onComplete: () => void,
    onError: (error: Error) => void
  ) {
    try {
      const response = await fetch("http://127.0.0.1:8000/search/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query, history: history,top_k: 5 }), 
      });
  
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error del servidor: ${response.status} ${errorText}`);
      }
  
      if (!response.body) {
        throw new Error("El cuerpo de la respuesta está vacío.");
      }
  
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let reading = true;
  
      while (reading) {
        const { done, value } = await reader.read();
        if (done) {
          reading = false;
          break;
        }
        const chunk = decoder.decode(value, { stream: true });
        onToken(chunk); 
      }
  
      onComplete(); 
  
    } catch (err) {
      console.error("Error al hacer streaming del chat:", err);
      onError(err instanceof Error ? err : new Error("Ocurrió un error desconocido"));
    }
  }
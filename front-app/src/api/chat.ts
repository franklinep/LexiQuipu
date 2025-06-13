import { ChatMessage, SourceDocument } from "../types/chat";
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
    onSources: (sources: SourceDocument[]) => void,
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
        body: JSON.stringify({ query: query, history: history,top_k: 10 }), 
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
      //let reading = true;

      let buffer = "";
      const separator = "\n<END_OF_SOURCES>\n";
      let sourcesFound = false;

  
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
  
        buffer += decoder.decode(value, { stream: true });
  
        if (!sourcesFound) {
          const separatorIndex = buffer.indexOf(separator);
          if (separatorIndex !== -1) {
            const sourcesJsonString = buffer.substring(0, separatorIndex);
            const restOfBuffer = buffer.substring(separatorIndex + separator.length);
            
            try {
              const parsed = JSON.parse(sourcesJsonString);
              if (parsed.type === 'sources') {
                onSources(parsed.data);
              }
            } catch (e) {
              console.error("Error al parsear las fuentes JSON:", e);
            }
            
            if (restOfBuffer) {
              onToken(restOfBuffer);
            }
            sourcesFound = true;
            buffer = "";
          }
        } else {
          onToken(buffer);
          buffer = "";
        }
      }
      onComplete();
  
    } catch (err) {
      console.error("Error al hacer streaming del chat:", err);
      onError(err instanceof Error ? err : new Error("Ocurrió un error desconocido"));
    }
  }
export interface SearchRequest {
    query: string;
    top_k?: number;
  }

  export interface SearchResult {
    id: string;
    text: string;
    metadata: Record<string, any>;
    distance: number;
  }

  export interface GeneratedResponse {
    generated_answer: string;
    source_documents: SearchResult[];
  }

  export async function searchJurisprudencia(query: string, topK: number = 5): Promise<GeneratedResponse> {
    const response = await fetch("http://127.0.0.1:8000/search/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, top_k: topK }),
    });

    if (!response.ok) {
      throw new Error("Error en la búsqueda y generación");
    }

    const data = await response.json();
    return data;
  }

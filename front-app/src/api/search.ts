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

  export async function searchJurisprudencia(query: string, topK: number = 5): Promise<SearchResult[]> {
    const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query, top_k: topK }),
    });

    if (!response.ok) {
      throw new Error("Error en la búsqueda");
    }

    const data = await response.json();
    return data;
  }

import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os


def vectorize_corpus(input_path, output_path):
    """
    Carga un corpus procesado, genera embeddings para cada chunk y
    guarda el corpus enriquecido.
    """
    print("Cargando corpus.json...")
    with open(input_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    print("Cargando modelo de embeddings...")
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    print("Modelo cargado.")

    print("Iniciando vectorización de chunks...")

    for document in tqdm(corpus, desc="Vectorizando documentos"):

        chunk_texts = [chunk for chunk in document['chunks']]

        embeddings = model.encode(chunk_texts, show_progress_bar=False)

        enriched_chunks = []
        for i, chunk_text in enumerate(chunk_texts):
            enriched_chunks.append({
                "text": chunk_text,
                "embedding": embeddings[i].tolist()
            })

        document['chunks'] = enriched_chunks

    print("\nVectorización completada.")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"Corpus vectorizado guardado en: {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    input_file = os.path.abspath(os.path.join(script_dir, '..', 'corpus.json'))
    output_file = os.path.abspath(os.path.join(script_dir, '..', 'output', 'corpus_vectorizado.json'))

    vectorize_corpus(input_file, output_file)

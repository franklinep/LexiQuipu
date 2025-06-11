import json
import chromadb
from tqdm import tqdm
import os

def build_vector_database(corpus_path, db_path, collection_name):
    """
    Carga el corpus vectorizado y lo indexa en una base de datos ChromaDB.
    """
    print("Cargando corpus vectorizado...")
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)

    print(f"Inicializando base de datos en: {db_path}")
    client = chromadb.PersistentClient(path=db_path)

    print(f"Obteniendo o creando la colección: {collection_name}")
    collection = client.get_or_create_collection(name=collection_name)

    print("Preparando datos para la indexación...")
    
    all_embeddings = []
    all_documents = []
    all_metadatas = []
    all_ids = []

    for doc in tqdm(corpus, desc="Procesando documentos para DB"):
        doc_metadata = doc.get('metadatos', {})
        doc_id = doc_metadata.get('id', os.path.basename(doc.get('archivo', ''))) # Usar ID o nombre de archivo

        for i, chunk in enumerate(doc['chunks']):
            chunk_id = f"{doc_id}_chunk_{i}"
            
            chunk_metadata = doc_metadata.copy()
            chunk_metadata['chunk_index'] = i # Guardamos el índice del chunk también

            all_embeddings.append(chunk['embedding'])
            all_documents.append(chunk['text'])
            all_metadatas.append(chunk_metadata)
            all_ids.append(chunk_id)

    print(f"\nIndexando {len(all_ids)} chunks en la base de datos...")
    collection.add(
        embeddings=all_embeddings,
        documents=all_documents,
        metadatas=all_metadatas,
        ids=all_ids
    )

    count = collection.count()
    print("\n¡Indexación completada!")
    print(f"La colección '{collection_name}' ahora contiene {count} chunks.")

if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    corpus_file = os.path.abspath(os.path.join(script_dir, '..', 'output', 'corpus_vectorizado.json'))
    db_directory = os.path.abspath(os.path.join(script_dir, '..', 'db'))
    
    COLLECTION = "jurisprudencia_peruana"

    build_vector_database(corpus_file, db_directory, COLLECTION)
import json
import chromadb
from tqdm import tqdm
import os

def build_vector_database(corpus_path, db_path, collection_name):
    """
    Carga el corpus vectorizado y lo indexa en una base de datos ChromaDB
    procesando los datos en lotes para evitar errores de tamaño.
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
        doc_id_base = doc_metadata.get('id', os.path.basename(doc.get('archivo', ''))) 

        for i, chunk in enumerate(doc['chunks']):
            chunk_id = f"{doc_id_base}_chunk_{i}"
            chunk_metadata = doc_metadata.copy()
            chunk_metadata['chunk_index'] = i

            all_embeddings.append(chunk['embedding'])
            all_documents.append(chunk['text'])
            all_metadatas.append(chunk_metadata)
            all_ids.append(chunk_id)

    batch_size = 5000
    total_chunks = len(all_ids)
    
    print(f"\nIndexando {total_chunks} chunks en la base de datos en lotes de {batch_size}...")

    for i in tqdm(range(0, total_chunks, batch_size), desc="Indexando lotes"):
        end_index = i + batch_size
        
        batch_embeddings = all_embeddings[i:end_index]
        batch_documents = all_documents[i:end_index]
        batch_metadatas = all_metadatas[i:end_index]
        batch_ids = all_ids[i:end_index]

        collection.add(
            embeddings=batch_embeddings,
            documents=batch_documents,
            metadatas=batch_metadatas,
            ids=batch_ids
        )
        
    count = collection.count()
    print("\n¡Indexación completada!")
    print(f"La colección '{collection_name}' ahora contiene {count} chunks.")
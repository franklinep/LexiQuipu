import chromadb
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from app.utils.pdf_processing import procesar_pdf_completo
import os
from tqdm import tqdm
from dotenv import load_dotenv

def build_index(collection_name: str, persist_dir: str, input_dir: str):
    """
    Construye un índice vectorial a partir de PDFs, utilizando embeddings de Google
    y procesando los archivos para limpiar texto y extraer metadatos.
    """
    # 1. Cargamos la API Key de Google
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada.")

    # 2. Configuramos el modelo de embedding globalmente en Llama-index
    print("Configurando el modelo de embedding: models/embedding-001")
    embed_model = GoogleGenAIEmbedding(
        model_name="models/embedding-001",
        api_key=api_key
    )
    Settings.embed_model = embed_model

    # 3. Conectamos con la base de datos de vectores
    print(f"Conectando a la base de datos en: {persist_dir}")
    db = chromadb.PersistentClient(path=persist_dir)
    print(f"Obteniendo o creando la colección: {collection_name}")
    chroma_collection = db.get_or_create_collection(collection_name)

    # 4. Procesamos todos los PDFs en el directorio de entrada
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print(f"No se encontraron archivos PDF en '{input_dir}'. Abortando.")
        return

    print(f"Procesando {len(pdf_files)} archivos PDF de '{input_dir}'...")

    documentos_llama = []
    for pdf_file in tqdm(pdf_files, desc="Procesando PDFs"):
        pdf_path = os.path.join(input_dir, pdf_file)
        texto_limpio, metadatos = procesar_pdf_completo(pdf_path)

        if texto_limpio:
            documento = Document(text=texto_limpio, metadata=metadatos)
            documentos_llama.append(documento)
        else:
            print(f"Advertencia: No se pudo extraer texto del archivo {pdf_file}. Será omitido.")

    if not documentos_llama:
        print("No se pudo procesar ningún documento PDF con éxito. Abortando.")
        return

    # 5. Configuramos el almacenamiento y construimos el índice
    print("Configurando el contexto de almacenamiento con ChromaDB...")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print(f"Indexando {len(documentos_llama)} documentos procesados...")
    index = VectorStoreIndex.from_documents(
        documentos_llama,
        storage_context=storage_context,
        show_progress=True
    )

    print("\n¡Índice construido y guardado exitosamente!")
    print(f"Total de documentos indexados: {len(documentos_llama)}")
    print(f"Total de chunks en la colección '{collection_name}': {chroma_collection.count()}")

    return index

if __name__ == "__main__":
    build_index(
        collection_name="lexiquipu",
        persist_dir="./db",
        input_dir="./pdfs"
    )

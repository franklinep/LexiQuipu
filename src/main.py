from pipeline_data import procesar_todos_los_pdfs
import json
import os
from vectorize import vectorize_corpus
from build_database import build_vector_database

if __name__ == "__main__":
    # 1. Procesar todos los PDFs y generar el corpus
    carpeta = "pdfs"
    salida = "corpus.json"
    script_dir = os.path.dirname(__file__)
    resultados = procesar_todos_los_pdfs(carpeta)
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"Procesamiento completo. Resultados en {salida}")

    # 2. Vectorizar el corpus
    input_file = os.path.abspath(os.path.join(script_dir, '..', 'corpus.json'))
    output_file = os.path.abspath(os.path.join(script_dir, '..', 'output', 'corpus_vectorizado.json'))
    vectorize_corpus(input_file, output_file)

    # 3. Construir la base de datos vectorizada indexada
    corpus_file = os.path.abspath(os.path.join(script_dir, '..', 'output', 'corpus_vectorizado.json'))
    db_directory = os.path.abspath(os.path.join(script_dir, '..', 'db'))
    COLLECTION = "jurisprudencia_peruana"
    build_vector_database(corpus_file, db_directory, COLLECTION)

## Informe del Proyecto LexiQuipu: Actualización a Llama-index

### 1. Visión General del Proyecto

LexiQuipu es una aplicación diseñada para facilitar la búsqueda y recuperación de información en un corpus de sentencias judiciales peruanas en formato PDF. Su objetivo principal es permitir a los usuarios realizar consultas en lenguaje natural y obtener respuestas contextualizadas, aprovechando las capacidades de los modelos de lenguaje grandes (LLMs) y las bases de datos vectoriales.

### 2. Sistema de Indexación Original

Inicialmente, el sistema de indexación de LexiQuipu se basaba en un pipeline manual y modular:
*   **Extracción y Limpieza:** Scripts en `src/pipeline_data.py` utilizaban `PyMuPDF` (fitz) para extraer texto de los PDFs, aplicar recortes para eliminar ruido visual (como notificaciones SEO en los márgenes) y limpiar el texto con expresiones regulares. También se utilizaban regex para extraer metadatos específicos (número de casación, lugar, materia) y para dividir el texto en "chunks" semánticos basados en marcadores como "Sumilla:", "CONSIDERANDO:", etc.
*   **Generación de Embeddings:** El script `src/vectorize.py` tomaba el texto limpio y utilizaba el modelo `sentence-transformers` (`paraphrase-multilingual-mpnet-base-v2`) para generar embeddings vectoriales.
*   **Almacenamiento:** El script `src/build_database.py` se encargaba de cargar estos embeddings y el texto asociado en una base de datos vectorial `ChromaDB`.
*   **Consulta:** La lógica de consulta en `app/crud/vector_query.py` interactuaba directamente con `ChromaDB` y utilizaba el mismo modelo `sentence-transformers` para vectorizar las consultas de usuario.

### 3. Motivación para la Actualización a Llama-index

Aunque el sistema original era funcional, presentaba oportunidades de mejora en términos de orquestación, estandarización y aprovechamiento de frameworks especializados. La integración de `Llama-index` se propuso para:
*   **Simplificar el Pipeline:** Consolidar los pasos de procesamiento, embedding e indexación bajo un único framework.
*   **Aprovechar Capacidades Avanzadas:** Utilizar las abstracciones y optimizaciones que `Llama-index` ofrece para la gestión de documentos, nodos y la interacción con bases de datos vectoriales.
*   **Estandarizar la Integración de LLMs:** Facilitar el cambio y la configuración de modelos de embedding y LLMs.

### 4. Cambios Clave y Migración a Llama-index

La actualización implicó una refactorización significativa de los componentes de procesamiento e indexación:

#### 4.1. Procesamiento de PDFs y Metadatos (`app/utils/pdf_processing.py`)
*   **Reutilización de Lógica:** La lógica de limpieza de texto y extracción de metadatos (incluyendo el recorte visual y las regex para metadatos específicos) del antiguo `pipeline_data.py` fue encapsulada en un nuevo módulo `app/utils/pdf_processing.py`. Esto asegura que el pre-procesamiento especializado se mantenga.
*   **Manejo de Ruido:** Se confirmó que `Llama-index` por sí mismo no maneja el ruido visual de los PDFs. Por lo tanto, la función `procesar_pdf_completo` en `pdf_processing.py` sigue siendo crucial para aplicar el recorte de márgenes y la limpieza de texto antes de que `Llama-index` lo procese.
*   **Robustez de Metadatos:** Se añadió una salvaguarda en `extraer_metadatos_desde_texto` para truncar metadatos excesivamente largos (ej. el campo "materia" si la regex captura demasiado texto), previniendo errores de `ValueError` durante la indexación de `Llama-index`.

#### 4.2. Modelo de Embedding (`models/embedding-001` de Google)
*   **Transición:** Se decidió migrar del modelo `sentence-transformers` local al modelo `models/embedding-001` de Google, alineando la generación de embeddings con el uso del modelo Gemini para la generación de respuestas.
*   **Resolución de Dependencias e Importaciones:** Se identificó y corrigió un error común de `Llama-index` relacionado con la importación de modelos de embedding de Google. Esto implicó:
    *   Cambiar la dependencia en `requirements.txt` de `llama-index-embeddings-google` a `llama-index-embeddings-google-genai`.
    *   Actualizar las importaciones en los scripts a `from llama_index.embeddings.google_genai import GoogleGenAIEmbedding`.
    *   Corregir la instanciación de la clase a `GoogleGenAIEmbedding`.
*   **Configuración Global:** El modelo de embedding se configura globalmente en `Llama-index` utilizando `Settings.embed_model` y cargando la `GOOGLE_API_KEY` desde el archivo `.env`.

#### 4.3. Proceso de Indexación (`src/build_index.py`)
*   **Orquestación Centralizada:** Este script ahora es el punto central para construir el índice.
*   **Flujo de Trabajo:**
    1.  Carga la `GOOGLE_API_KEY`.
    2.  Configura `Settings.embed_model` con `GoogleGenAIEmbedding`.
    3.  Se conecta a `ChromaDB` y obtiene/crea la colección.
    4.  Itera sobre los PDFs en la carpeta `./pdfs`.
    5.  Para cada PDF, llama a `procesar_pdf_completo` para obtener el texto limpio y los metadatos.
    6.  Crea objetos `Document` de `Llama-index` con el texto limpio y los metadatos extraídos.
    7.  Construye el `VectorStoreIndex` a partir de estos objetos `Document`, utilizando `ChromaVectorStore` para la persistencia en ChromaDB.

#### 4.4. Proceso de Consulta (`app/crud/vector_query.py`)
*   **Consistencia de Embeddings:** Se actualizó este script para asegurar que las consultas de usuario se vectoricen utilizando el mismo modelo `models/embedding-001` de Google, garantizando la coherencia entre la indexación y la búsqueda.
*   **Uso del Retriever de Llama-index:** Ahora utiliza el `retriever` del `VectorStoreIndex` de `Llama-index` para realizar las búsquedas, aprovechando las optimizaciones del framework.
*   **Ajuste de Esquema:** El esquema `SearchResult` en `app/schemas/search.py` fue modificado para reflejar el campo `score` en lugar de `distance`, que es el término utilizado por `Llama-index`.

#### 4.5. Limpieza de Código
*   Los scripts antiguos (`src/vectorize.py`, `src/build_database.py`, `src/pipeline_data.py`) fueron eliminados para mantener el proyecto limpio y evitar redundancias.

### 5. Beneficios de la Nueva Arquitectura

La migración a `Llama-index` y la integración del modelo de embedding de Google han aportado los siguientes beneficios:
*   **Pipeline Unificado:** Un flujo de trabajo más cohesivo y fácil de entender para el procesamiento y la indexación de documentos.
*   **Consistencia de Modelos:** Uso del mismo ecosistema de Google (embeddings y LLM) para todo el proceso RAG, lo que puede mejorar la calidad de las respuestas.
*   **Robustez Mejorada:** La lógica de pre-procesamiento de PDFs se mantiene y se ha hecho más robusta para manejar casos de metadatos problemáticos.
*   **Mantenibilidad:** Al apoyarse en un framework maduro como `Llama-index`, el código es más modular, extensible y fácil de mantener.
*   **Rendimiento Potencial:** `Llama-index` está optimizado para el manejo de grandes volúmenes de datos y la interacción eficiente con bases de datos vectoriales.

### 6. Conclusión

La actualización de LexiQuipu a `Llama-index` representa una mejora significativa en la arquitectura del proyecto. Al integrar un framework especializado y unificar el modelo de embedding con el LLM de generación, el sistema es ahora más robusto, eficiente y preparado para futuras expansiones en el ámbito de la búsqueda y recuperación de información legal.

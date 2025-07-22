# LexiQuipu

LexiQuipu es una aplicación de búsqueda y respuesta basada en jurisprudencia peruana, diseñada para facilitar la consulta de sentencias judiciales. Utiliza modelos de lenguaje avanzados y bases de datos vectoriales para proporcionar respuestas relevantes y contextualizadas a partir de un corpus de documentos PDF.

## Características

- **Procesamiento de PDFs:** Extrae y limpia texto de documentos PDF, eliminando ruido y extrayendo metadatos clave.
- **Indexación Vectorial:** Construye un índice vectorial utilizando `Llama-index` y `ChromaDB` con embeddings de Google (`models/embedding-001`).
- **Búsqueda Semántica:** Permite realizar consultas en lenguaje natural para encontrar sentencias relevantes.
- **Generación de Respuestas (RAG):** Utiliza el modelo Gemini de Google para generar respuestas coherentes basadas en el contexto de los documentos recuperados.
- **API REST:** Proporciona una API para interactuar con el backend.
- **Frontend (React):** Incluye una aplicación web para una interfaz de usuario interactiva.

## Requisitos Previos

Asegúrate de tener instalado lo siguiente:

- [**Python 3.9+**](https://www.python.org/downloads/)
- [**pip**](https://pip.pypa.io/en/stable/installation/) (gestor de paquetes de Python)
- [**Node.js y npm**](https://nodejs.org/en/download/) (para el frontend)

## Configuración del Entorno

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/LexiQuipu.git
    cd LexiQuipu
    ```

2.  **Crear y Activar un Entorno Virtual (Python):**
    Es altamente recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

    ```bash
    python -m venv env
    # En Windows:
    .\env\Scripts\activate
    # En macOS/Linux:
    source env/bin/activate
    ```

3.  **Instalar Dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la API Key de Google:**
    Necesitarás una clave de API de Google para usar los modelos de embedding y generación de Gemini.
    - Obtén tu clave de API en [Google AI Studio](https://aistudio.google.com/app/apikey).
    - Crea un archivo `.env` en la raíz del proyecto (`LexiQuipu/`) y añade tu clave:
        ```
        GOOGLE_API_KEY="TU_CLAVE_DE_API_AQUI"
        ```

## Uso

### 1. Construir el Índice Vectorial

Este paso procesa tus documentos PDF, extrae el texto, los metadatos y crea los embeddings para construir el índice en ChromaDB.

Asegúrate de colocar tus archivos PDF en la carpeta `./pdfs`.

```bash
python -m src.build_index
```
Este proceso puede tardar un tiempo dependiendo del número y tamaño de tus PDFs. Verás un progreso en la consola.

### 2. Ejecutar el Backend (API FastAPI)

El backend proporciona la API para interactuar con el índice vectorial y el modelo de lenguaje.

```bash
uvicorn app.main:app --reload
```
El servidor estará disponible en `http://127.0.0.1:8000`. Puedes acceder a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`.

### 3. Ejecutar el Frontend (Aplicación React)

El frontend es una aplicación React que consume la API del backend.

1.  **Navega al directorio del frontend:**
    ```bash
    cd front-app
    ```

2.  **Instalar dependencias de Node.js:**
    ```bash
    npm install
    ```

3.  **Iniciar la aplicación React:**
    ```bash
    npm start
    ```
    Esto abrirá la aplicación en tu navegador predeterminado (normalmente `http://localhost:3000`).

## Dependencias Clave

Aquí se listan las principales bibliotecas utilizadas en el proyecto y su propósito:

-   **`llama-index`**: Framework para construir aplicaciones LLM con datos personalizados, orquestando el procesamiento, indexación y consulta.
-   **`chromadb`**: Base de datos vectorial de código abierto utilizada para almacenar y buscar embeddings.
-   **`llama-index-vector-stores-chroma`**: Integración de `Llama-index` con `ChromaDB`.
-   **`llama-index-embeddings-google-genai`**: Integración de `Llama-index` con los modelos de embedding de Google Generative AI (`models/embedding-001`).
-   **`google-generativeai`**: SDK de Google para interactuar con los modelos Gemini (utilizado para la generación de respuestas).
-   **`fastapi`**: Framework web de Python para construir APIs rápidas y eficientes.
-   **`uvicorn`**: Servidor ASGI para ejecutar aplicaciones FastAPI.
-   **`pymupdf` (fitz)**: Biblioteca para trabajar con PDFs, utilizada para la extracción y manipulación de texto.
-   **`python-dotenv`**: Para cargar variables de entorno desde un archivo `.env`.
-   **`tqdm`**: Para mostrar barras de progreso en la consola.
-   **`react`**: Biblioteca JavaScript para construir interfaces de usuario (utilizada en el frontend).

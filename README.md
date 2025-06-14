# Generación aumentada por recuperación (RAG) con Transformers

## Colaboradores:

* Espinoza Pari, Franklin
* De la Cruz Valdiviezo, Pedro

![Demo LexiQuipu](https://s4.ezgif.com/tmp/ezgif-4c8c50fd8d3ca8.gif)

## Descripcion del Proyecto:

El conocimiento de un modelo de lenguaje está limitado a la información presente en sus datos de entrenamiento (conocimiento paramétrico). Esto lo hace propenso a "alucinar" hechos y a quedar desactualizado. La Generación Aumentada por Recuperación (RAG) es una técnica que mitiga este problema al permitir que el modelo consulte una base de conocimiento externa y actualizada en tiempo de inferencia. El proceso típico implica:

* Recuperador (Retriever): Ante una pregunta, este componente busca y extrae los fragmentos de texto más relevantes de una base de datos vectorial (e.g., un índice de Wikipedia).

* Generador (Generator): El texto recuperado se concatena con la pregunta original y se le entrega como contexto a un modelo de lenguaje generativo (como GPT o T5) para que formule una respuesta informada y fundamentada.

## Objetivos:

* Construir un pipeline de RAG completo.
* Utilizar un modelo de embeddings pre-entrenado (e.g., sentence-transformers) para indexar un corpus de documentos (puedes usar un subconjunto de Wikipedia o artículos de un tema específico) en una base de datos vectorial como FAISS o ChromaDB.
* Implementar la lógica que, dada una consulta, recupera los `k` documentos más relevantes.
* Integrar el contexto recuperado con un LLM pre-entrenado (e.g., Flan-T5, GPT-2) para generar la respuesta final.

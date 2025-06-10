import fitz
import os
import json
import re
import unicodedata

def recortar_pdf(ruta_original):
    """
    Recorta cada página del PDF original a un área específica y guarda el resultado.
    """
    try:
        pdf_original = fitz.open(ruta_original)
        pdf_recortado = fitz.open()

        print(f"Procesando '{ruta_original}'...")
        for i, pagina_original in enumerate(pdf_original):
            ancho = pagina_original.rect.width
            alto = pagina_original.rect.height
            rect = fitz.Rect(ancho * 0.1, 50, ancho, alto)

            nueva_pagina = pdf_recortado.new_page(width=rect.width, height=rect.height)
            nueva_pagina.show_pdf_page(nueva_pagina.rect, pdf_original, pno=i, clip=rect)
            print(f"  -> Página {i+1} recortada.")

        # print(f"\nPDF recortado guardado en: '{ruta_salida}'")
        return pdf_recortado
    except Exception as e:
        print(f"Error al recortar PDF: {e}")

def extraer_y_filtrar_bloques(pdf_path):
    """
    Extrae texto de bloques, omitiendo contenido considerado ruido.
    """
    texto_limpio = ""
    noise_keywords = [
        'SINOE', 'Vocal Supremo', 'FIRMA DIGITAL', 'Servicio Digital',
        'Razón: RESOLUCIÓN', 'D.Judicial:', 'Secretario De Sala', 'DEPA'
    ]
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            bloques = page.get_text("blocks", sort=True)
            for _, _, _, _, texto, *_ in bloques:
                es_ruido = any(k in texto for k in noise_keywords)
                if "SEGUNDA SALA DE DERECHO CONSTITUCIONAL" in texto:
                    es_ruido = True
                if re.match(r"Página \d+ de \d+", texto.strip()):
                    es_ruido = True
                if not es_ruido:
                    texto_limpio += texto
        doc.close()
        return texto_limpio
    except Exception as e:
        print(f"Error extrayendo bloques de {pdf_path}: {e}")
        return ""

def limpiar_texto(texto):
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    texto = re.sub(r' +', ' ', texto)
    texto = re.sub(r'\n \n', '\n', texto)
    texto = re.sub(r'\n?Página\s+\d+\s+de\s+\d+\s*\n?', '\n', texto)
    return texto.strip()

def normalizar_texto(texto):
    texto = texto.replace("\n", " ")
    texto = re.sub(r'\s{2,}', ' ', texto)
    # texto = texto.lower()
    # texto = ''.join(
    #     c for c in unicodedata.normalize('NFKD', texto)
    #     if not unicodedata.combining(c)
    # )
    # texto = texto.replace('n.o', 'n').replace('nº', 'n').replace('n°', 'n').replace('no', 'n').replace('n.°', 'n')
    return texto

def extraer_texto(pdf_path):
    try:
        with fitz.open(pdf_path) as doc:
            return "".join(page.get_text("text", sort=True) for page in doc)
    except Exception as e:
        print(f"Error extrayendo texto de {pdf_path}: {e}")
        return ""

def extraer_texto_2(pdf_en_memoria):
    """
    Extrae todo el texto de un objeto PDF en memoria (fitz.Document).
    """
    try:
        texto = ""
        for page in pdf_en_memoria:
            texto += page.get_text("text", sort=True)
        return texto
    except Exception as e:
        print(f"Error al extraer texto del PDF en memoria: {e}")
        return ""

def extraer_metadatos(texto):
    metadatos = {}
    texto_norm = normalizar_texto(texto)

    # materias = [
    #     "desnaturalización de contrato y otros",
    #     "homologación de remuneraciones y otros",
    #     "relación laboral indeterminado y otros"
    # ]
    # patron_materias = "|".join(map(re.escape, materias))

    patron = re.compile(
        # r'casacion laboral n[.º ]+(\d{4,6}-\d{4})\s+([a-zñ ]+?)\s+(desnaturalizacion de contrato y otros|homologacion de remuneraciones y otros|relacion laboral indeterminado y otros)(?=\s+proceso| sumilla|$)',
        # r"CASACIÓN LABORAL (?:Nº|N\.º|N\.°|N°)\s*(\d+-\d+)\s+([A-ZÁÉÍÓÚÜÑa-zñáéíóúü\s]+?)\s+(.+?)\s+PROCESO",
        r"CASACIÓN LABORAL (?:Nº|N\.º|N\.°|N°)\s*(\d+-\d+)\s+((?:El|La)\s+[A-ZÁÉÍÓÚÜÑa-zñáéíóúü]+|[A-ZÁÉÍÓÚÜÑa-zñáéíóúü]+)\s+(.+?)\s+PROCESO",
        re.IGNORECASE
    )

    match = patron.search(texto_norm)
    if match:
        return {
            "n_casacion": match.group(1).strip(),
            "lugar": match.group(2).strip().title(),
            "materia": match.group(3).strip().capitalize()
        }
    else:
        print("No se encontraron metadatos en:\n", texto_norm[:500])
    return metadatos

def dividir_en_chunks_semanticos(texto):
    patron = r'(?=Sumilla:?|VISTA;?|MATERIA DEL RECURSO|CAUSALES DEL RECURSO|CAUSAL DEL RECURSO|CONSIDERANDO:?|DECISIÓN:?|Por estas consideraciones:\n)'
    chunks = re.split(patron, texto)
    chunks = [c.strip() for c in chunks if c.strip() and c.strip() != "Por estas consideraciones:"]

    return chunks

def procesar_pdf(pdf_path):
    texto_limpio = limpiar_texto(extraer_y_filtrar_bloques(pdf_path))
    pdf_recortado = recortar_pdf(pdf_path)
    texto_crudo = extraer_texto_2(pdf_recortado)
    return {
        "archivo": os.path.basename(pdf_path),
        "metadatos": extraer_metadatos(texto_crudo),
        "chunks": dividir_en_chunks_semanticos(texto_limpio)
    }

def procesar_todos_los_pdfs(directorio):
    return [procesar_pdf(os.path.join(directorio, f))
            for f in os.listdir(directorio) if f.lower().endswith(".pdf")]

if __name__ == "__main__":
    carpeta = "pdfs"
    salida = "salida_pdfs.json"
    resultados = procesar_todos_los_pdfs(carpeta)
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"Procesamiento completo. Resultados en {salida}")

import fitz  # PyMuPDF
import re
import os

def limpiar_texto(texto: str) -> str:
    """Limpia y normaliza el texto extraído de los PDFs."""
    texto = re.sub(r'\n{3,}', '\n\n', texto)  # Reduce saltos de línea múltiples
    texto = re.sub(r' +', ' ', texto)  # Elimina espacios extra
    texto = re.sub(r'\n \n', '\n', texto)  # Elimina espacios en líneas vacías
    # Elimina encabezados/pies de página de paginación
    texto = re.sub(r'\n?Página\s+\d+\s+de\s+\d+\s*\n?', '\n', texto, flags=re.IGNORECASE)
    return texto.strip()

def normalizar_texto_para_metadatos(texto: str) -> str:
    """Normaliza el texto específicamente para la extracción de metadatos."""
    texto = texto.replace("\n", " ")
    texto = re.sub(r'\s{2,}', ' ', texto)
    return texto

def extraer_metadatos_desde_texto(texto: str) -> dict:
    """Extrae metadatos clave de una cadena de texto usando regex."""
    texto_norm = normalizar_texto_para_metadatos(texto)

    patron = re.compile(
        r"CASACIÓN LABORAL (?:Nº|N\\.º|N\\.°|N°)\\s*(\\d+-\\d+)\\s+([A-ZÁÉÍÓÚÜÑa-zñáéíóúü\\s]+?)\\s+(.+?)(?=PROCESO|SUMILLA)",
        re.IGNORECASE
    )

    match = patron.search(texto_norm)
    if match:
        # Limpia y formatea los grupos capturados
        n_casacion = match.group(1).strip()
        lugar = ' '.join(match.group(2).strip().title().split())
        materia = match.group(3).strip().capitalize()
        
        # Salvaguarda para evitar metadatos demasiado largos
        if len(materia) > 500:
            materia = materia[:500] + "..."

        return {
            "n_casacion": n_casacion,
            "lugar": lugar,
            "materia": materia
        }
    else:
        # Fallback por si el patrón principal no funciona
        patron_simple = re.compile(r"CASACIÓN(?: LABORAL)? (?:Nº|N\\.º|N\\.°|N°)\\s*(\\d+-\\d+)", re.IGNORECASE)
        match_simple = patron_simple.search(texto_norm)
        if match_simple:
            return {"n_casacion": match_simple.group(1).strip()}

    return {}

def procesar_pdf_completo(pdf_path: str) -> tuple[str, dict]:
    """
    Procesa un único archivo PDF para extraer su texto limpio y metadatos.
    Aplica un recorte para eliminar ruido de los márgenes.
    """
    try:
        with fitz.open(pdf_path) as doc_original:
            # 1. Recortar el PDF en memoria para eliminar ruido de los bordes
            pdf_recortado = fitz.open()
            for pagina in doc_original:
                ancho, alto = pagina.rect.width, pagina.rect.height
                # Recorte generoso para eliminar cabeceras y pies de página
                rect = fitz.Rect(ancho * 0.1, alto * 0.1, ancho * 0.9, alto * 0.9)

                nueva_pagina = pdf_recortado.new_page(width=rect.width, height=rect.height)
                # La función show_pdf_page con el parámetro 'clip' hace el recorte
                nueva_pagina.show_pdf_page(nueva_pagina.rect, doc_original, pno=pagina.number, clip=rect)

            # 2. Extraer texto del PDF recortado
            texto_completo = ""
            for pagina in pdf_recortado:
                texto_completo += pagina.get_text("text", sort=True)

            pdf_recortado.close()

        # 3. Extraer metadatos del texto crudo (antes de la limpieza final)
        metadatos = extraer_metadatos_desde_texto(texto_completo)
        metadatos['file_name'] = os.path.basename(pdf_path)

        # 4. Limpiar el texto para la indexación
        texto_limpio = limpiar_texto(texto_completo)

        return texto_limpio, metadatos
    except Exception as e:
        print(f"Error procesando el archivo {pdf_path}: {e}")
        return "", {"file_name": os.path.basename(pdf_path)}

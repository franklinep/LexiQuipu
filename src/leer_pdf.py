# Este script probaremos la extraccion de un pdf con pymupdf
import fitz

pdf_path = "../pdfs/Resolucion_S_N_2025-01-09 15_07_49.383,id=1007485398.pdf"

try:
    doc = fitz.open(pdf_path) # Abrimos el pdf

    print(f"El PDF tiene {doc.page_count} paginas")

    full_text = ""

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        full_text += page.get_text("text")
        full_text += "\n---Fin de la pagina---".format(page_num+1)

    doc.close()

    print("---Inicio del PDF---")
    print(full_text)
    print("---Fin del PDF---")

except Exception as e:
    print(f"Error al abrir el PDF: {e}")




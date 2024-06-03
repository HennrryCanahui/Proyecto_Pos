import os
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def generar_codigos_barras(ids):
    codigos_barras = []
    for id in ids:
        EAN = barcode.get_barcode_class('ean13')
        codigo_barra = EAN(str(id).zfill(12), writer=ImageWriter())
        filename = f"codigo_barra_{id}"
        full_filename = codigo_barra.save(filename)
        codigos_barras.append(full_filename)
    return codigos_barras

def generar_pdf(codigos_barras, output_filename='codigos_barras.pdf'):
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    x = 0.05 * cm  # Margen izquierdo de 1 cm
    y = height - 0.5 * cm  # Margen superior de 1 cm
    
    barra_ancho = 3 * cm
    barra_alto = 2 * cm  # Ajustar el alto según sea necesario
    margen = 0.05 * cm
    
    for codigo_barra in codigos_barras:
        if os.path.exists(codigo_barra):
            c.drawImage(codigo_barra, x, y - barra_alto, width=barra_ancho, height=barra_alto)
            x += barra_ancho + margen
            if x + barra_ancho > width - 1 * cm:  # Si se sale del ancho de la página
                x = 1 * cm  # Reiniciar al margen izquierdo
                y -= barra_alto + margen  # Bajar a la siguiente fila
            
            if y - barra_alto < 1 * cm:  # Si se sale del alto de la página
                c.showPage()
                x = 1 * cm
                y = height - 1 * cm
        else:
            print(f"Archivo no encontrado: {codigo_barra}")
    
    c.save()
    print(f"PDF generado: {output_filename}")

    # Eliminar archivos de imagen temporales
    for codigo_barra in codigos_barras:
        try:
            if os.path.exists(codigo_barra):
                os.remove(codigo_barra)
            else:
                print(f"No se pudo encontrar el archivo para eliminar: {codigo_barra}")
        except Exception as e:
            print(f"No se pudo eliminar el archivo {codigo_barra}: {e}")

def main(ids):
    codigos_barras = generar_codigos_barras(ids)
    generar_pdf(codigos_barras)

# Ejemplo de uso
if __name__ == "__main__":
    ids = [123456789012]
    main(ids)

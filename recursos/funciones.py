import sqlite3
import random
import os
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from barcode import get_barcode_class
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import xml.etree.ElementTree as ET
import platform
import glob





def conexion():
    database = r'database\comercial.sqlite'
    try:
        conn = sqlite3.connect(database)
        print(f"Conexión exitosa a la base de datos: {database}")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
def registro(id, nombre, precio_unidad, precio_mayor):
    conn = conexion()
    if conn is None:
        return False, "Error al conectar con la base de datos."
    
    try:
        cur = conn.cursor()
        
        # Verificar si el id ya existe
        cur.execute("SELECT id FROM datos WHERE id = ?", (id,))
        if cur.fetchone() is not None:
            return False, f"El id {id} ya existe. No se puede insertar duplicado."
        
        # Insertar nuevo registro
        sql = '''INSERT INTO datos(id, nombre, precio_unidad, precio_mayor) VALUES (?, ?, ?, ?)'''
        cur.execute(sql, (id, nombre, precio_unidad, precio_mayor))
        conn.commit()
        return True, "Registro insertado con éxito."
        
    except sqlite3.IntegrityError as e:
        return False, f"Error de integridad al insertar los datos: {e}"
    except sqlite3.Error as e:
        return False, f"Error en la operación de base de datos: {e}"
    finally:
        conn.close()

        

def consulta(id):
    conn = conexion()
    if conn is None:
        return
    try:
        sql = '''SELECT * FROM datos WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (id,))
        resultado = cur.fetchone()
        if resultado is not None:
            pass
            #print("Precio Unidad: ", resultado[2])
        else:
            pass
            #print("No se encontró el producto con el id dado.")
        return resultado
    except sqlite3.Error as e:
        pass
        #print(f"Error en la operación de base de datos: {e}")
    finally:
        conn.close()

def consulta_mayor(id):
    conn = conexion()
    if conn is None:
        return
    try:
        sql = '''SELECT * FROM datos WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (id,))
        resultado = cur.fetchone()
        if resultado is not None:
            pass
            #print("Precio Mayorista: ", resultado[3])
        else:
            pass
            #print("No se encontró el producto con el id dado.")
        return resultado
    except sqlite3.Error as e:
        pass
        #print(f"Error en la operación de base de datos: {e}")
    finally:
        conn.close()

########################################################

def verificar_campos(id, nombre, precio_unidad, precio_mayor):
    if not id:
        while True:
            id = random.randint(10**12, 10**13 - 1)
            if len(str(id)) == 13:
                break
        id = str(id)
    
    if not (nombre and precio_unidad and precio_mayor):
        return False, id, "Hay campos vacíos. Por favor, complete todos los campos."

    return True, id, None

def verificar_precios(precio_unidad, precio_mayor):
    try:
        precio_unidad = float(precio_unidad)
        precio_mayor = float(precio_mayor)
        if precio_unidad <= precio_mayor:
            return False, "El precio unitario debe ser mayor que el precio mayorista."
        return True, None
    except ValueError:
        return False, "Los precios deben ser valores numéricos."
    

######################################################################################################################
# AQUI TIENE QUE IR LA FUNCION PARA COMVERTIR LOS ID EN CODIGOS DE BARRAS PARA LUEGO MANDARLOS A IMPRIMIR EN UN PDF  #
######################################################################################################################

def generar_codigos_barras_pdf(id_copias_list, output_filename='codigos_barras.pdf'):
    # Generar códigos de barras y guardar nombres de archivos
    codigos_barras = []
    for id, copias in id_copias_list:
        CODE128 = get_barcode_class('code128')
        for i in range(copias):
            codigo_barra = CODE128(str(id), writer=ImageWriter())
            filename = f"codigo_barra_{id}_{i}"
            full_filename = codigo_barra.save(filename)
            codigos_barras.append(full_filename)

    # Crear el PDF con los códigos de barras
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter
    x = 1 * cm  # Margen izquierdo de 1 cm
    y = height - 1 * cm  # Margen superior de 1 cm
    
    barra_ancho = 3.5 * cm
    barra_alto = 2 * cm  # Ajustar el alto según sea necesario
    margen = 0.5 * cm
    
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


###############################################
##  Aqui tiene que ir las funciones de ventas
#######################################







###########################################################
##  Funcion para imprimir recibos y pdf de archivos xml  ##
###########################################################



# Función para buscar el archivo XML en la carpeta de descargas
def buscar_archivo_xml(carpeta_descargas):
    archivos_xml = glob.glob(os.path.join(carpeta_descargas, '*.xml'))
    if archivos_xml:
        return archivos_xml[0]
    else:
        return None

# Función para extraer datos del XML
def extraer_datos_xml(archivo_xml):
    tree = ET.parse(archivo_xml)
    root = tree.getroot()
    
    namespaces = {
        'dte': 'http://www.sat.gob.gt/dte/fel/0.2.0', 
    }

    # Extraer datos generales
    datos_generales = root.find('.//dte:DatosGenerales', namespaces)
    fecha_hora_emision = datos_generales.get('FechaHoraEmision')
    tipo = datos_generales.get('Tipo')

    # Extraer datos del emisor
    emisor = root.find('.//dte:Emisor', namespaces)
    nit_emisor = emisor.get('NITEmisor')
    direccion_emisor = emisor.find('.//dte:Direccion', namespaces).text

    # Extraer datos del receptor
    receptor = root.find('.//dte:Receptor', namespaces)
    nombre_receptor = receptor.get('NombreReceptor')
    id_receptor = receptor.get('IDReceptor')

    # Extraer los ítems
    items = root.findall('.//dte:Item', namespaces)
    lista_items = []
    for item in items:
        descripcion = item.find('.//dte:Descripcion', namespaces).text
        cantidad = int(float(item.find('.//dte:Cantidad', namespaces).text))
        precio_unitario = int(float(item.find('.//dte:PrecioUnitario', namespaces).text))
        total = int(float(item.find('.//dte:Total', namespaces).text))
        lista_items.append({
            'descripcion': descripcion,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'total': total
        })

    # Extraer el elemento GranTotal
    total = root.find('.//dte:Totales', namespaces)
    monto_total = int(float(total.find('dte:GranTotal', namespaces).text))

    return {
        'fecha_hora_emision': fecha_hora_emision,
        'tipo': tipo,
        'nit_emisor': nit_emisor,
        'direccion_emisor': direccion_emisor,
        'nombre_receptor': nombre_receptor,
        'id_receptor': id_receptor,
        'items': lista_items,
        'monto_total': monto_total
    }

# Función para centrar texto
def draw_centered_text(c, text, y_position, page_width):
    text_width = c.stringWidth(text, "Helvetica-Bold", 14)
    x_position = (page_width - text_width) / 2
    c.drawString(x_position, y_position, text)

# Función para crear el PDF
def crear_pdf(datos, pdf_filename="recibo.pdf"):

    # Tamaño de la página en puntos (10 cm de ancho por 29.7 cm de largo)
    page_width = 10 * cm
    page_height = 29.7 * cm

    # Crear un archivo PDF
    c = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))

    # Márgenes y posiciones iniciales
    x_margin = 10
    y_start = page_height - 20
    line_spacing = 10
    y_position = y_start

     # Logo y encabezado
    logo_path = os.path.abspath("recursos/Logo.jpeg") # Cambia esto a la ruta de tu imagen de logo
    logo_width = 80  # Ajusta el ancho de tu logo
    logo_height = 80  # Ajusta la altura de tu logo
    c.drawImage(logo_path, x_margin + 20, y_position - 75, width=logo_width, height=logo_height)

    
    c.drawString(page_width - 110, y_position - 15, "FACT")
    c.setFont("Helvetica", 8)
    y_position -= 30
    c.drawString(page_width - 130, y_position, f"Fecha: {datos['fecha_hora_emision'].split('T')[0]}")
    y_position -= line_spacing
    c.drawString(page_width - 130, y_position, f"Hora: {datos['fecha_hora_emision'].split('T')[1]}")
    y_position -= line_spacing
    c.drawString(page_width - 130, y_position, f"NIT: {datos['nit_emisor']}")
    y_position -= line_spacing
    c.drawString(page_width - 130, y_position, f"Dirección: {datos['direccion_emisor'][:18]}")
    y_position -= line_spacing
    c.drawString(page_width - 132, y_position, f"{datos['direccion_emisor'][30:]}")

    # Información del receptor
    y_position -= 20
    c.drawString(x_margin, y_position, "Receptor:")
    y_position -= line_spacing
    c.drawString(x_margin + 20, y_position, f"Nombre: {datos['nombre_receptor']}")
    y_position -= line_spacing
    c.drawString(x_margin + 20, y_position, f"ID: {datos['id_receptor']}")

    # Tabla de productos
    y_position -= 20
    c.drawString(x_margin, y_position, "Cant")
    c.drawString(x_margin + 30, y_position, "DESCRIPCION")
    c.drawString(x_margin + 150, y_position, "Precio")
    c.drawString(x_margin + 200, y_position, "total")
    
    y_position -= line_spacing
    for item in datos['items']:
        c.drawString(x_margin + 5, y_position, str(item['cantidad']))
        c.drawString(x_margin + 30, y_position, item['descripcion'])
        c.drawString(x_margin + 150, y_position, str(item['precio_unitario']))
        c.drawString(x_margin + 200, y_position, str(item['total']))
        y_position -= line_spacing

    # Monto total
    y_position -= 20
    c.setLineWidth(2)
    c.line(x_margin + 130, y_position + 25, x_margin + 240, y_position + 25)
    c.drawString(x_margin + 175, y_position + 10, "Total:")
    c.drawString(x_margin + 200, y_position + 10, str(datos['monto_total']))

    # Guardar el PDF
    c.save()

# Función para imprimir el PDF
def imprimir_pdf(file_path):
    system_name = platform.system()
    if system_name == "Windows":
        os.startfile(file_path, "print")
    elif system_name == "Darwin":  # macOS
        os.system(f"lp {file_path}")
    elif system_name == "Linux":
        os.system(f"lp {file_path}")

def Facturacion():
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    
    # Buscar el archivo XML en la carpeta de descargas
    archivo_xml = buscar_archivo_xml(carpeta_descargas)
    
    if archivo_xml:
        datos = extraer_datos_xml(archivo_xml)
        
        pdf_filename = "recibo.pdf"
        crear_pdf(datos, pdf_filename)

        # Imprimir el PDF
        #imprimir_pdf(pdf_filename)

        # Borrar el archivo XML
        os.remove(archivo_xml)
    else:
        print("No se encontró ningún archivo XML en la carpeta de descargas.")

        
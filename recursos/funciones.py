import sqlite3
import random
import os
import barcode
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from barcode import get_barcode_class
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm






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

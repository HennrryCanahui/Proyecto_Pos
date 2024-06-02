import sqlite3
import random

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
            print("Precio Unidad: ", resultado[2])
        else:
            print("No se encontró el producto con el id dado.")
        return resultado
    except sqlite3.Error as e:
        print(f"Error en la operación de base de datos: {e}")
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
            print("Precio Mayorista: ", resultado[3])
        else:
            print("No se encontró el producto con el id dado.")
        return resultado
    except sqlite3.Error as e:
        print(f"Error en la operación de base de datos: {e}")
    finally:
        conn.close()






########################################################


def verificar_campos(id, nombre, precio_unidad, precio_mayor):
    if not id:
        id = str(random.randint(1000000, 9999999))
    
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
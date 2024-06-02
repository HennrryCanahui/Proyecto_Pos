import sqlite3

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
        return
    try:
        cur = conn.cursor()
        
        # Verificar si el id ya existe
        cur.execute("SELECT id FROM datos WHERE id = ?", (id,))
        if cur.fetchone() is not None:
            print(f"El id {id} ya existe. No se puede insertar duplicado.")
            return
        
        # Insertar nuevo registro
        sql = '''INSERT INTO datos(id, nombre, precio_unidad, precio_mayor) VALUES (?, ?, ?, ?)'''
        cur.execute(sql, (id, nombre, precio_unidad, precio_mayor))
        conn.commit()
        print("Registro insertado con éxito.")
        
    except sqlite3.IntegrityError as e:
        print(f"Error de integridad al insertar los datos: {e}")
    except sqlite3.Error as e:
        print(f"Error en la operación de base de datos: {e}")
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

import sqlite3
from pathlib import Path

# Ruta de la carpeta actual
ruta_actual = Path.cwd()

# Ruta completa de la carpeta "database"
ruta_carpeta = ruta_actual / 'database'

# Verifica si la carpeta ya existe o créala
if not ruta_carpeta.exists():
    ruta_carpeta.mkdir(parents=True, exist_ok=True)
    print(f"Carpeta 'database' creada en {ruta_carpeta}")
else:
    print(f"La carpeta 'database' ya existe en {ruta_carpeta}")

# Ruta completa de la base de datos
ruta_base_datos = ruta_carpeta / 'comercial.sqlite'

# Conecta a la base de datos
base = sqlite3.connect(ruta_base_datos)

# Crea la tabla si no existe
db = base.cursor()
db.execute('''
    CREATE TABLE IF NOT EXISTS datos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        precio_unidad REAL,
        precio_mayor REAL
    )
''')

# Guarda los cambios y cierra la conexión
base.commit()
base.close()

print(f"Tabla 'datos' creada en la base de datos {ruta_base_datos}")

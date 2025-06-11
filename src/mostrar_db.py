import sqlite3

def mostrar_tablas(cursor):
    """Muestra todas las tablas disponibles en la base de datos."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    print("📂 Tablas disponibles en la base de datos:")
    for tabla in tablas:
        print(f"  - {tabla[0]}")
    print()

def mostrar_tabla(cursor, nombre_tabla, limite=5):
    """Muestra algunas filas de una tabla específica."""
    print(f"📄 Contenido de la tabla '{nombre_tabla}' (primeros {limite} registros):")
    try:
        cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT {limite};")
        filas = cursor.fetchall()
        for fila in filas:
            print(fila)
    except Exception as e:
        print(f"❌ Error al leer la tabla '{nombre_tabla}': {e}")
    print()

def mostrar_estructura_tabla(cursor, nombre_tabla):
    """Muestra la estructura (columnas) de una tabla."""
    print(f"🔍 Estructura de la tabla '{nombre_tabla}':")
    try:
        cursor.execute(f"PRAGMA table_info({nombre_tabla});")
        columnas = cursor.fetchall()
        for columna in columnas:
            print(columna)
    except Exception as e:
        print(f"❌ Error al obtener estructura de la tabla '{nombre_tabla}': {e}")
    print()

def main():
    db_path = "db/chroma.sqlite3"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(f"✅ Conectado a la base de datos: {db_path}\n")

        mostrar_tablas(cursor)
        mostrar_tabla(cursor, "collections")
        mostrar_estructura_tabla(cursor, "embeddings")
        mostrar_tabla(cursor, "embeddings", limite=3)

    except sqlite3.Error as db_err:
        print(f"❌ Error al conectar o consultar la base de datos: {db_err}")
    finally:
        if conn:
            conn.close()
            print("\n🔒 Conexión cerrada.")

if __name__ == "__main__":
    main()

#creacion bbdd
import sqlite3


def crear_base_datos():
    conexion = sqlite3.connect('usuarios.db') # busca la base de datos usuarios.db para hacer la conexión y si no la encuentra la crea
    cursor = conexion.cursor() # con esto vamos a interactuar con la base de datos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL UNIQUE
    )
    ''')
    conexion.commit() # hacemos el cambio dentro de la base de datos
    conexion.close() # cerramos conexión

if __name__ == '__main__': # dentro de nuestro modulo llamamos a la función
    crear_base_datos()


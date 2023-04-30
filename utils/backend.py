import sqlite3
import datetime
import json
import random

def crear_BaseDatos ():
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # crear la tabla de mensajes con las columnas id, fecha y mensaje
    cursor.execute('CREATE TABLE mensajes (id INTEGER PRIMARY KEY, fecha TEXT, mensaje TEXT)')

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()


def guardar_datos(mensaje: dict):
    mensaje = mensaje['mensaje']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # obtener el mes y día actual en el formato "MM-DD"
    fecha_actual = datetime.datetime.now().strftime("%m/%d")

    # insertar un mensaje en la tabla con un ID automático
    cursor.execute('INSERT INTO mensajes (fecha, mensaje) VALUES (?, ?)', (fecha_actual, mensaje))

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    mensaje_id = cursor.lastrowid
    print(f"Se ha insertado un mensaje con el ID {mensaje_id}")
    return mensaje_id


def obtener_mensajes():
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')
    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()
    # seleccionar todos los registros de la tabla
    cursor.execute('SELECT * FROM mensajes')
    # obtener los resultados de la consulta
    resultados = cursor.fetchall()
    # crear una lista vacía para almacenar los mensajes
    mensajes = []
    # iterar sobre los resultados y agregarlos a la lista de mensajes
    for resultado in resultados:
        mensaje = {
            'id': resultado[0],
            'fecha': resultado[1],
            'mensaje': resultado[2]
        }
        mensajes.append(mensaje)
    # cerrar la conexión a la base de datos
    conn.close()
    # convertir la lista de mensajes a un objeto JSON y devolverlo
    return json.dumps(mensajes)


# Función para obtener un mensaje por fecha
def obtener_mensaje_por_fecha_db(fecha: dict):
    fecha = fecha['fecha']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para obtener el mensaje por fecha
    cursor.execute('SELECT * FROM mensajes WHERE fecha = ?', (fecha,))

    # obtener los resultados de la consulta
    mensajes = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not mensajes:
        return None
    
    # crear una lista de diccionarios con los mensajes encontrados
    mensajes_encontrados = []
    for mensaje in mensajes:
        mensajes_encontrados.append({'id': mensaje[0], 'fecha': mensaje[1], 'mensaje': mensaje[2]})

    # retornar la lista de mensajes encontrados
    return mensajes_encontrados


# Función para obtener un mensaje por id
def obtener_mensaje_por_id_db(id: int):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para obtener el mensaje por id
    cursor.execute('SELECT * FROM mensajes WHERE id = ?', (id,))

    # obtener el resultado de la consulta
    mensaje = cursor.fetchone()

    # cerrar la conexión a la base de datos
    conn.close()

    # retornar el mensaje como un diccionario si se encontró, o None si no se encontró
    if mensaje:
        return {'id': mensaje[0], 'fecha': mensaje[1], 'mensaje': mensaje[2]}
    else:
        return False


# Función para buscar mensajes por su contenido
def buscar_mensajes_por_contenido_db(contenido: dict):
    contenido = contenido['contenido']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM mensajes WHERE mensaje LIKE '%{contenido}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    mensajes = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not mensajes:
        return None
    
    # crear una lista de diccionarios con los mensajes encontrados
    mensajes_encontrados = []
    for mensaje in mensajes:
        mensajes_encontrados.append({'id': mensaje[0], 'fecha': mensaje[1], 'mensaje': mensaje[2]})

    # retornar la lista de mensajes encontrados
    return mensajes_encontrados

def eliminar_mensaje_db(id):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para eliminar el mensaje
    query = f'DELETE FROM mensajes WHERE id = {id}'

    # Ejecutar la consulta de eliminación
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        return False

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True

def mensaje_aleatorio_db():
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # obtener el número total de mensajes
    cursor.execute('SELECT COUNT(*) FROM mensajes')
    total_mensajes = cursor.fetchone()[0]

    # cerrar la conexión a la base de datos
    conn.close()

    # generar un número aleatorio entre 1 y el número total de mensajes
    mensaje_id = random.randint(1, 1000)

    # busca un mensaje con el ID aleatorio
    mensaje = obtener_mensaje_por_id_db(mensaje_id)

    # comprobar que el mensaje existe
    if not mensaje:
        return False
    
    else:
        return mensaje
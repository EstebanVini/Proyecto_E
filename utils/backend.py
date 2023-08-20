import sqlite3
import datetime
import json
import random
import bcrypt

#____________________________________________Usuarios_______________________________________________________


def obtener_usuario_por_username(username: str):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('users.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para obtener el usuario por username
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))

    except:
        return False

    usuario = cursor.fetchone()

    # cerrar la conexión a la base de datos
    conn.close()

    # si se encontró el usuario, retornar verdadero y si no se encontró, retornar falso
    if usuario:
        return {'id': usuario[0], 'username': usuario[1], 'password': usuario[2], 'salt': usuario[3]}
    
    else:
        return False

def hash_password(password, salt=None):
    pwd_bytes = password.encode("utf-8")
    if salt is None:
        salt = bcrypt.gensalt()
    else:
        salt = salt.encode("utf-8")
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd.decode('utf-8'), salt.decode('utf-8')

def crear_usuaio(data: dict):
    username = data['username']
    password = data['password']
    hasd_password, salt = hash_password(password)



    # crear una conexión a la base de datos
    conn = sqlite3.connect('users.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # consultar si el usuario ya existe
    if obtener_usuario_por_username(username):
        return False
    
    # insertar un usuario en la tabla con un ID automático
    cursor.execute('INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', (username, hasd_password, salt))

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()


def login(data: dict):
    username = data['username']
    password = data['password']

    # crear una conexión a la base de datos
    conn = sqlite3.connect('users.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # consultar si el usuario ya existe
    usuario = obtener_usuario_por_username(username)

    # si el usuario no existe, retornar falso
    if not usuario:
        return False

    # si el usuario existe, verificar si la contraseña es correcta
    if bcrypt.hashpw(password.encode('utf-8'), usuario['salt']) == usuario['password']:
        return True
    else:
        return False
    

def eliminar_usuario(data: str):
    username = data['username']

    # crear una conexión a la base de datos
    conn = sqlite3.connect('users.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # consultar si el usuario ya existe
    usuario = obtener_usuario_por_username(username)

    # si el usuario no existe, retornar falso
    if not usuario:
        return False

    # si el usuario existe, eliminarlo de la base de datos
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True





#_______________________________________________MENSAJES_______________________________________________________

def crear_BaseDatos ():
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # crear la tabla de mensajes con las columnas id, fecha y mensaje
    cursor.execute('CREATE TABLE peliculas (id INTEGER PRIMARY KEY, nombre TEXT, genero TEXT, tipo TEXT)')

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

def guardar_datos(mensaje: dict, tabla="mensajesElena"):
    mensaje = mensaje['mensaje']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # obtener el mes y día actual en el formato "MM-DD"
    fecha_actual = datetime.datetime.now().strftime("%m/%d")

    # insertar un mensaje en la tabla con un ID automático
    cursor.execute(f'INSERT INTO {tabla} (fecha, mensaje) VALUES (?, ?)', (fecha_actual, mensaje))

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    mensaje_id = cursor.lastrowid
    print(f"Se ha insertado un mensaje con el ID {mensaje_id}")
    return mensaje_id

def obtener_mensajes(tabla="mensajesElena"):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')
    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()
    # seleccionar todos los registros de la tabla
    cursor.execute(f'SELECT * FROM {tabla}')
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

def obtener_mensaje_por_fecha_db(fecha: dict, tabla="mensajesElena"):
    fecha = fecha['fecha']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para obtener el mensaje por fecha
    cursor.execute(f'SELECT * FROM {tabla} WHERE fecha = ?', (fecha,))

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

def obtener_mensaje_por_id_db(id: int, tabla="mensajesElena"):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para obtener el mensaje por id
    cursor.execute(f'SELECT * FROM {tabla} WHERE id = ?', (id,))

    # obtener el resultado de la consulta
    mensaje = cursor.fetchone()

    # cerrar la conexión a la base de datos
    conn.close()

    # retornar el mensaje como un diccionario si se encontró, o None si no se encontró
    if mensaje:
        return {'id': mensaje[0], 'fecha': mensaje[1], 'mensaje': mensaje[2]}
    else:
        return False

def buscar_mensajes_por_contenido_db(contenido: dict, tabla="mensajesElena"):
    contenido = contenido['contenido']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM {tabla} WHERE mensaje LIKE '%{contenido}%'"

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

def eliminar_mensaje_db(id, tabla="mensajesElena"):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('mensajes.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para eliminar el mensaje
    query = f'DELETE FROM {tabla} WHERE id = {id}'

    # Ejecutar la consulta de eliminación
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        return False

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True

def mensaje_aleatorio_db(tabla="mensajesElena"):
    try:
        # crear una conexión a la base de datos
        conn = sqlite3.connect('mensajes.db')

        # crear un cursor para ejecutar consultas SQL
        cursor = conn.cursor()

        # ejecutar la consulta SQL para obtener el mensaje por fecha
        cursor.execute(f'SELECT * FROM {tabla}')

        # obtener los resultados de la consulta
        mensajes = cursor.fetchall()

        # cerrar la conexión a la base de datos
        conn.close()

        mensajes_encontrados = []
        for mensaje in mensajes:
            mensajes_encontrados.append({'id': mensaje[0], 'fecha': mensaje[1], 'mensaje': mensaje[2]})

        mensajes_aleatorios = random.choice(mensajes_encontrados)

        # retornar la lista de mensajes encontrados
        return mensajes_aleatorios
    except:
        return False


# _____________________________________________PELICULAS_______________________________________________________

def guardar_pelicula(datos: dict):

    nombre = datos['nombre']
    genero = datos['genero']
    tipo = datos['tipo']

    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # insertar una película en la tabla con un ID automático
    cursor.execute(f'INSERT INTO peliculas (nombre, genero, tipo) VALUES (?, ?, ?)', (nombre, genero, tipo))

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()
    pelicula_id = cursor.lastrowid

    print(f"Se ha insertado una película con el ID {pelicula_id}")
    return pelicula_id

def obtener_peliculas():
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')
    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()
    # seleccionar todos los registros de la tabla
    cursor.execute('SELECT * FROM peliculas')
    # obtener los resultados de la consulta
    resultados = cursor.fetchall()
    # crear una lista vacía para almacenar los mensajes
    peliculas = []
    # iterar sobre los resultados y agregarlos a la lista de mensajes
    for resultado in resultados:
        pelicula = {
            'id': resultado[0],
            'nombre': resultado[1],
            'genero': resultado[2],
            'tipo': resultado[3]
        }
        peliculas.append(pelicula)
    # cerrar la conexión a la base de datos
    conn.close()
    # convertir la lista de mensajes a un objeto JSON y devolverlo
    return json.dumps(peliculas)

def obtener_pelicula_por_id(id: int):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para obtener el mensaje por id
    cursor.execute(f'SELECT * FROM peliculas WHERE id = ?', (id,))

    # obtener el resultado de la consulta
    pelicula = cursor.fetchone()

    # cerrar la conexión a la base de datos
    conn.close()

    # retornar el mensaje como un diccionario si se encontró, o None si no se encontró
    if pelicula:
        return {'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]}
    else:
        return False

def eliminar_pelicula(id):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para eliminar el mensaje
    query = f'DELETE FROM peliculas WHERE id = {id}'

    # Ejecutar la consulta de eliminación
    try:
        cursor.execute(query)
    except sqlite3.Error as e:
        return False

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True

def actualizar_pelicula(id, datos: dict):
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # ejecutar la consulta SQL para actualizar el mensaje
    query = f'UPDATE peliculas SET nombre = ?, genero = ?, tipo = ? WHERE id = ?'

    # Ejecutar la consulta de actualización
    try:
        cursor.execute(query, (datos['nombre'], datos['genero'], datos['tipo'], id))
    except sqlite3.Error as e:
        return False

    # confirmar los cambios y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()

    return True

def buscar_peliculas_por_nombre(datos: dict):

    nombre = datos['nombre']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar la película por su nombre, con que contenga una parte del nombre
    consulta = f"SELECT * FROM peliculas WHERE nombre LIKE '%{nombre}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None
    
    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})

    # retornar la lista de mensajes encontrados
    return peliculas_encontradas

def buscar_peliculas_por_genero(datos: dict):

    genero = datos['genero']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM peliculas WHERE genero LIKE '%{genero}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None
    
    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})

    # retornar la lista de mensajes encontrados
    return peliculas_encontradas

def buscar_peliculas_por_tipo(datos: dict):
    
    tipo = datos['tipo']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM peliculas WHERE tipo LIKE '%{tipo}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None
    
    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})

    # retornar la lista de mensajes encontrados
    return peliculas_encontradas

def buscar_peliculas_por_genero_y_tipo(datos: dict):
        
    genero = datos['genero']
    tipo = datos['tipo']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM peliculas WHERE genero LIKE '%{genero}%' AND tipo LIKE '%{tipo}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None
    
    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})

    # retornar la lista de mensajes encontrados
    return peliculas_encontradas

def pelicula_aleatoria_por_genero_y_tipo(datos: dict):
        
    genero = datos['genero']
    tipo = datos['tipo']
    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM peliculas WHERE genero LIKE '%{genero}%' AND tipo LIKE '%{tipo}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None
    
    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})

    pelicula_aleatoria = random.choice(peliculas_encontradas)

    return pelicula_aleatoria

def pelicula_o_serie_aleatoria():

    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM peliculas"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None

    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})
    
    pelicula_aleatoria = random.choice(peliculas_encontradas)

    # retornar la lista de mensajes encontrados
    return pelicula_aleatoria

def pelicula_o_serie_aleatoria_por_genero(datos: dict):
        
    genero = datos['genero']

    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM peliculas WHERE genero LIKE '%{genero}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None

    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})
    
    pelicula_aleatoria = random.choice(peliculas_encontradas)

    # retornar la lista de mensajes encontrados
    return pelicula_aleatoria

def pelicula_o_serie_aleatoria_por_tipo(datos: dict):
            
    tipo = datos['tipo']

    # crear una conexión a la base de datos
    conn = sqlite3.connect('peliculas.db')

    # crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # construir la consulta SQL para buscar mensajes por su contenido
    consulta = f"SELECT * FROM peliculas WHERE tipo LIKE '%{tipo}%'"

    # ejecutar la consulta SQL para buscar mensajes por su contenido
    cursor.execute(consulta)

    # obtener los resultados de la consulta
    peliculas = cursor.fetchall()

    # cerrar la conexión a la base de datos
    conn.close()

    # si no se encontraron mensajes, regresar None
    if not peliculas:
        return None

    # crear una lista de diccionarios con los mensajes encontrados
    peliculas_encontradas = []
    for pelicula in peliculas:
        peliculas_encontradas.append({'id': pelicula[0], 'nombre': pelicula[1], 'genero': pelicula[2], 'tipo': pelicula[3]})
    
    pelicula_aleatoria = random.choice(peliculas_encontradas)

    # retornar la lista de mensajes encontrados
    return pelicula_aleatoria

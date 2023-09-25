import sqlite3
import datetime
import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from  utils.backend import *
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Running"}

#____________________________________________Usuarios_______________________________________________________

@app.post("/crear_usuario")
async def guardar_usuario(usuario: dict):
    if crear_usuaio(usuario):
        return {"message": "Se ha creado el usuario exitosamente", "estado": True}
    else:
        return {"message": "No se ha podido crear el usuario", "estado": False}

@app.post("/inicio_sesion")
async def inicio_sesion(usuario: dict):
    if login(usuario):
        return {"message": "Inicio de sesión exitoso", "estado": True}
    else:
        return {"message": "No se ha podido iniciar sesión", "estado": False}

@app.delete("/eliminar_usuario/{username}")
async def eliminar_usuario_db(username: str):
    if eliminar_usuario(username):
        return {"message": "Se ha eliminado el usuario exitosamente"}
    else:
        return {"message": "No se ha podido eliminar el usuario"}



#____________________________________________Mensajes_______________________________________________________

@app.post("/guardar_mensaje")
async def guardar_mensaje(mensaje: dict):
    mensaje_id = guardar_datos(mensaje, tabla="mensajes")
    return {"message": f"Se ha insertado un mensaje con el ID {mensaje_id}"}

@app.get("/obtener_mensajes")
async def obtener_todos_los_mensajes():
    mensajes = obtener_mensajes(tabla="mensajes")
    return {"mensajes": json.loads(mensajes)}

@app.get("/obtener_mensaje_por_fecha")
async def obtener_mensaje_por_fecha(fecha: dict):
    mensaje = obtener_mensaje_por_fecha_db(fecha, tabla="mensajes")
    if mensaje:
        return {"mensaje": mensaje}
    else:
        return {"message": "No se encontró ningún mensaje para esa fecha."}

@app.get("/obtener_mensaje_por_id/{id}")
async def obtener_mensaje_por_id(id: int):
    mensaje = obtener_mensaje_por_id_db(id, tabla="mensajes")
    if mensaje:
        return {"mensaje": mensaje}
    else:
        return {"message": "No se encontró ningún mensaje con ese ID."}

@app.get("/buscar_mensajes_por_contenido")
async def buscar_mensajes_por_contenido(contenido: dict):
    mensajes = buscar_mensajes_por_contenido_db(contenido, tabla="mensajes")
    if mensajes:
        return {"mensajes": mensajes}
    else:
        return {"message": "No se encontraron mensajes con ese contenido."}

@app.delete("/eliminar_mensaje/{id}")
async def eliminar_mensaje(id: int):
    if obtener_mensaje_por_id_db(id, tabla="mensajes"):
        eliminar_mensaje_db(id, tabla="mensajes")
        return {"message": f"Se ha eliminado el mensaje con el ID {id}"}
    else:
        return {"message": "No se encontró ningún mensaje con ese ID."}

@app.get("/obtener_mensaje_aleratorio")
async def obtener_mensaje_aleratorio():
    mensaje = mensaje_aleatorio_db(tabla="mensajes")
    while not mensaje:
        mensaje = mensaje_aleatorio_db(tabla="mensajes")
    return {"result": mensaje}

@app.post("/guardar_mensaje/Elena")
async def guardar_mensaje(mensaje: dict):
    mensaje_id = guardar_datos(mensaje)
    return {"message": f"Se ha insertado un mensaje con el ID {mensaje_id}"}

@app.get("/obtener_mensajes/Elena")
async def obtener_todos_los_mensajes():
    mensajes = obtener_mensajes()
    return {"mensajes": json.loads(mensajes)}

@app.get("/obtener_mensaje_por_fecha/Elena")
async def obtener_mensaje_por_fecha(fecha: dict):
    mensaje = obtener_mensaje_por_fecha_db(fecha)
    if mensaje:
        return {"mensaje": mensaje}
    else:
        return {"message": "No se encontró ningún mensaje para esa fecha."}

@app.get("/obtener_mensaje_por_id/Elena/{id}")
async def obtener_mensaje_por_id(id: int):
    mensaje = obtener_mensaje_por_id_db(id)
    if mensaje:
        return {"mensaje": mensaje}
    else:
        return {"message": "No se encontró ningún mensaje con ese ID."}

@app.get("/buscar_mensajes_por_contenido/Elena")
async def buscar_mensajes_por_contenido(contenido: dict):
    mensajes = buscar_mensajes_por_contenido_db(contenido)
    if mensajes:
        return {"mensajes": mensajes}
    else:
        return {"message": "No se encontraron mensajes con ese contenido."}

@app.delete("/eliminar_mensaje/Elena/{id}")
async def eliminar_mensaje(id: int):
    if obtener_mensaje_por_id_db(id):
        eliminar_mensaje_db(id)
        return {"message": f"Se ha eliminado el mensaje con el ID {id}"}
    else:
        return {"message": "No se encontró ningún mensaje con ese ID."}

@app.get("/obtener_mensaje_aleratorio/Elena")
async def obtener_mensaje_aleratorio():
    mensaje = mensaje_aleatorio_db()
    while not mensaje:
        mensaje = mensaje_aleatorio_db()
    return {"result": mensaje}



#______________________________________PELICULAS____________________________________________________

@app.post("/guardar_pelicula")
async def guardar_pelicula_en_base(pelicula: dict):
    pelicula_id = guardar_pelicula(pelicula)
    return {"message": f"Se ha insertado una pelicula con el ID {pelicula_id}"}

@app.get("/obtener_peliculas")
async def obtener_peliculasdb():
    peliculas = obtener_peliculas()
    return {"peliculas": json.loads(peliculas)}

@app.get("/obtener_pelicula_por_id/{id}")
async def obtener_pelicula_por_iddb(id: int):
    pelicula = obtener_pelicula_por_id(id)
    if pelicula:
        return {"pelicula": pelicula}
    else:
        return {"message": "No se encontró ninguna pelicula con ese ID."}

@app.delete("/eliminar_pelicula/{id}")
async def eliminar_peliculadb(id: int):
    if obtener_pelicula_por_id(id):
        eliminar_pelicula(id)
        return {"message": f"Se ha eliminado la pelicula con el ID {id}"}
    else:
        return {"message": "No se encontró ninguna pelicula con ese ID."}

@app.post("/actualizar_pelicula/{id}")
async def actualizar_peliculadb(id: int, pelicula: dict):
    if obtener_pelicula_por_id(id):
        actualizar_pelicula(id, pelicula)
        return {"message": f"Se ha actualizado la pelicula con el ID {id}"}
    else:
        return {"message": "No se encontró ninguna pelicula con ese ID."}

@app.get("/buscar_pelicula_por_titulo")
async def buscar_pelicula_por_titulodb(titulo: dict):
    pelicula = buscar_peliculas_por_nombre(titulo)
    if pelicula:
        return {"pelicula": pelicula}
    else:
        return {"message": "No se encontró ninguna pelicula con ese titulo."}

@app.get("/buscar_peliculas_por_genero")
async def buscar_peliculas_por_generodb(genero: dict):
    peliculas = buscar_peliculas_por_genero(genero)
    if peliculas:
        return {"peliculas": peliculas}
    else:
        return {"message": "No se encontraron peliculas con ese genero."}

@app.get("/buscar_peliculas_por_tipo")
async def buscar_peliculas_por_tipodb(tipo: dict):
    peliculas = buscar_peliculas_por_tipo(tipo)
    if peliculas:
        return {"peliculas": peliculas}
    else:
        return {"message": "No se encontraron peliculas con ese tipo."}

@app.get("/buscar_peliculas_por_genero_y_tipo")
async def buscar_peliculas_por_generoytipodb(datos: dict):
    peliculas = buscar_peliculas_por_genero_y_tipo(datos)
    if peliculas:
        return {"peliculas": peliculas}
    else:
        return {"message": "No se encontraron peliculas con ese genero o tipo."}

@app.get("/obtener_aleatoria_por_genero_y_tipo")
async def aleatoria_por_genero_y_tipodb(datos: dict):
    pelicula = pelicula_aleatoria_por_genero_y_tipo(datos)
    if pelicula:
        return {"pelicula": pelicula}
    else:
        return {"message": "No se encontraron peliculas con ese genero o tipo."}

@app.get("/obtener_pelicula_o_serie_aleatoria")
async def pelicula_o_serie_aleatoriadb():
    pelicula = pelicula_o_serie_aleatoria()
    if pelicula:
        return {"pelicula": pelicula}
    else:
        return {"message": "No se encontraron peliculas o series."}

@app.get("/obtener_pelicula_o_serie_aleatoria_por_tipo")
async def pelicula_o_serie_aleatoria_por_tipodb(tipo: dict):
    pelicula = pelicula_o_serie_aleatoria_por_tipo(tipo)
    if pelicula:
        return {"pelicula": pelicula}
    else:
        return {"message": "No se encontraron peliculas o series con ese tipo."}

if __name__ == "__main__":
    uvicorn.run(app, port=2681)



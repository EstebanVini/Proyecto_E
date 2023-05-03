import sqlite3
import datetime
import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from  utils.backend import guardar_datos, obtener_mensajes, obtener_mensaje_por_fecha_db, obtener_mensaje_por_id_db, buscar_mensajes_por_contenido_db, eliminar_mensaje_db, mensaje_aleatorio_db

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("vistas/index.html")

@app.get("/guardar_mensaje")
async def guardar_mensaje():
    return FileResponse("vistas/guardar_mensaje.html")

@app.post("/guardar_mensaje")
async def guardar_mensaje(mensaje: dict):
    mensaje_id = guardar_datos(mensaje, tabla="mensajes")
    return {"message": f"Se ha insertado un mensaje con el ID {mensaje_id}"}

@app.get("/todos")
async def todos_los_mensajes():
    return FileResponse("vistas/obtener_mensajes.html")

@app.get("/obtener_mensajes")
async def obtener_todos_los_mensajes():
    mensajes = obtener_mensajes(tabla="mensajes")
    return {"mensajes": json.loads(mensajes)}

@app.get("/buscar")
async def buscar_mensaje():
    return FileResponse("vistas/busquedas.html")

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

@app.get("/mensaje_aleatorio")
async def mensaje_aleratorio():
    return FileResponse("vistas/mensaje_aleratorio.html")

@app.get("/obtener_mensaje_aleratorio")
async def obtener_mensaje_aleratorio():
    mensaje = mensaje_aleatorio_db(tabla="mensajes")
    while not mensaje:
        mensaje = mensaje_aleatorio_db(tabla="mensajes")
    return {"result": mensaje}

@app.get("/guardar_mensaje/Elena")
async def guardar_mensaje():
    return FileResponse("vistas/guardar_mensaje.html")

@app.post("/guardar_mensaje/Elena")
async def guardar_mensaje(mensaje: dict):
    mensaje_id = guardar_datos(mensaje)
    return {"message": f"Se ha insertado un mensaje con el ID {mensaje_id}"}

@app.get("/todos/Elena")
async def todos_los_mensajes():
    return FileResponse("vistas/obtener_mensajes.html")

@app.get("/obtener_mensajes/Elena")
async def obtener_todos_los_mensajes():
    mensajes = obtener_mensajes()
    return {"mensajes": json.loads(mensajes)}

@app.get("/buscar/Elena")
async def buscar_mensaje():
    return FileResponse("vistas/busquedas.html")

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

@app.get("/mensaje_aleatorio/Elena")
async def mensaje_aleratorio():
    return FileResponse("vistas/mensaje_aleratorio.html")

@app.get("/obtener_mensaje_aleratorio/Elena")
async def obtener_mensaje_aleratorio():
    mensaje = mensaje_aleatorio_db()
    while not mensaje:
        mensaje = mensaje_aleatorio_db()
    return {"result": mensaje}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)



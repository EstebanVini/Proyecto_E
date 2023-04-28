import sqlite3
import datetime
import json
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from  utils.backend import guardar_datos, obtener_mensajes, obtener_mensaje_por_fecha, obtener_mensaje_por_id, buscar_mensajes_por_contenido, eliminar_mensaje

app = FastAPI()

@app.get("/")
async def root():
    return FileResponse("vistas/index.html")

@app.get("/guardar_mensaje")
async def guardar_mensaje():
    return FileResponse("vistas/guardar_mensaje.html")

@app.post("/guardar_mensaje/{mensaje}")
async def guardar_mensaje(mensaje: str):
    mensaje_id = guardar_datos(mensaje)
    return {"message": f"Se ha insertado un mensaje con el ID {mensaje_id}"}

@app.get("/todos")
async def todos_los_mensajes():
    return FileResponse("vistas/obtener_mensajes.html")

@app.get("/obtener_mensajes")
async def obtener_todos_los_mensajes():
    mensajes = obtener_mensajes()
    return {"mensajes": json.loads(mensajes)}

@app.get("/obtener_mensaje_por_fecha/{fecha}")
async def obtener_mensaje_por_fecha(fecha: str):
    mensaje = obtener_mensaje_por_fecha(fecha)
    if mensaje:
        return {"mensaje": mensaje}
    else:
        return {"message": "No se encontró ningún mensaje para esa fecha."}

@app.get("/obtener_mensaje_por_id/{id}")
async def obtener_mensaje_por_id(id: int):
    mensaje = obtener_mensaje_por_id(id)
    if mensaje:
        return {"mensaje": mensaje}
    else:
        return {"message": "No se encontró ningún mensaje con ese ID."}

@app.get("/buscar_mensajes_por_contenido/{contenido}")
async def buscar_mensajes_por_contenido(contenido: str):
    mensajes = buscar_mensajes_por_contenido(contenido)
    if mensajes:
        return {"mensajes": mensajes}
    else:
        return {"message": "No se encontraron mensajes con ese contenido."}

@app.post("/eliminar_mensaje/{id}")
async def eliminar_mensaje(id: int):
    mensaje_eliminado = eliminar_mensaje(id)
    if mensaje_eliminado:
        return {"message": f"Se ha eliminado el mensaje con el ID {id}"}
    else:
        return {"message": "No se encontró ningún mensaje con ese ID."}


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.100.239", port=80)


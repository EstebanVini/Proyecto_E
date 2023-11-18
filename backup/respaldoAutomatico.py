import requests
import json
import os
import time
import datetime

url = "https://proyectoe.eviniegra.software"

def respaldoMensajesEsteban():
    response = requests.get(f"{url}/obtener_mensajes")
    data = response.json()
    print(data)
    open('mensajesEsteban.json', "w").write(json.dumps(data, indent=4))


def respaldoMensajesElena():
    response = requests.get(f"{url}/obtener_mensajes/Elena")
    data = response.json()
    print(data)
    open('mensajesElena.json', "w").write(json.dumps(data, indent=4))

def respaldoPeliculas():
    response = requests.get(f"{url}/obtener_peliculas")
    data = response.json()
    print(data)
    open('peliculas.json', "w").write(json.dumps(data, indent=4))

def respaldoAutomatico():
    while True:
        respaldoMensajesEsteban()
        print("Respaldo de mensajes de Esteban realizado")
        time.sleep(5)
        respaldoMensajesElena()
        print("Respaldo de mensajes de Elena realizado")
        time.sleep(5)
        respaldoPeliculas()
        print("Respaldo de peliculas realizado")
        # esperar 12 horas
        time.sleep(43200)



if __name__ == "__main__":
    respaldoAutomatico()
        

        
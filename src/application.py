import numpy as np
import json
import requests
import os
from .util import ENDPOINT_TENSORFLOW_MODEL, REPOSITORIO_DE_IMAGENES_PUBLICAS, ENDPOINT_REPORTAR_MASCOTA

def obtener_mascotas_parecidas(nombre_imagen):
    print('obtener_mascotas_parecidas')
    try:
        file_imagen = open(nombre_imagen,'rb')
        files = {'upload_file': file_imagen}
        url = ENDPOINT_TENSORFLOW_MODEL

        response = requests.post(url, files=files)
        print('Respuesta de la red neuronal: {}'.format(response.text))
        respuesta = response.text.replace('/static/', REPOSITORIO_DE_IMAGENES_PUBLICAS)
        predictions = json.loads(respuesta)

        print('Predicción: {}'.format(predictions))
        
        file_imagen.close()
        eliminar_archivos_temporales(nombre_imagen)
        
        return predictions
    except Exception as e:
        print(e)
        file_imagen.close()
        eliminar_archivos_temporales(nombre_imagen)
        return None

def reportar_mascota_desaparecida(nombre_imagen):
    try:
        file_imagen = open(nombre_imagen,'rb')
        files = {'upload_file': file_imagen}
        url = ENDPOINT_REPORTAR_MASCOTA

        response = requests.post(url, files=files)
        print('Respuesta: {}'.format(response.text))
        respuesta = json.loads(response.text)

        print('Respuesta: {}'.format(respuesta))
        
        file_imagen.close()
        #eliminar_archivos_temporales(nombre_imagen)
        
        return respuesta
    except Exception as e:
        print(e)
        file_imagen.close()
        #eliminar_archivos_temporales(nombre_imagen)
        return None

def eliminar_archivos_temporales(filename):
    try:
        print('Eliminar el archivo temporal {}'.format(filename))
        os.remove(filename)
    except AssertionError as error:
        print(error)
        print('Error al eliminar el archivo temporal {}'.format(filename))
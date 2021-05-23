from .util import ENDPOINT_DOG_FACE_CROPPER, ENDPOINT_TENSORFLOW_MODEL, ENDPOINT_REPORTAR_MASCOTA
import numpy as np
import json
import requests
import os
import io
import base64
from PIL import Image

def obtener_imagen_recortada(data_imagen):
    print('obtener_imagen_recortada')
    try:
        # Recortar imagen
        if ENDPOINT_DOG_FACE_CROPPER:
            files = {'upload_file': data_imagen}
            response = requests.post(ENDPOINT_DOG_FACE_CROPPER, json=files)
            imagen_bytes = base64.b64decode(json.loads(response.text)['img'])
            print('API de recorte e identificación de rostro de perro retornó: {}'.format(type(imagen_bytes)))

            if type(imagen_bytes) == bytes:
                return True, imagen_bytes
            else:
                return False, None
        return False, 'No se ha inicializado variable de entorno ENDPOINT_DOG_FACE_CROPPER'
    except Exception as e:
        print('Error: {}'.format(e))
        return False, None

def obtener_mascotas_parecidas(image_bytes, geolocalizacion):
    print('obtener_mascotas_parecidas')
    try:
        # Predecir perros
        if ENDPOINT_TENSORFLOW_MODEL:
            files = {'upload_file': image_bytes}
            response = requests.post(ENDPOINT_TENSORFLOW_MODEL, json=files)

            print('Respuesta de la red neuronal: {}'.format(response.text))
            predictions = json.loads(response.text)

            print('Predicción: {}'.format(predictions))
        
            return True, predictions
        return False, 'No se ha inicializado variable de entorno ENDPOINT_TENSORFLOW_MODEL'
    except Exception as e:
        print(e)
        return None

def reportar_mascota_desaparecida(image_bytes):
    try:
        if ENDPOINT_REPORTAR_MASCOTA:
            files = {'upload_file': image_bytes}
            response = requests.post(ENDPOINT_REPORTAR_MASCOTA, json=files)
            print('Respuesta: {}'.format(response.text))
            respuesta = json.loads(response.text)
            
            return True, respuesta
        return False, 'No se ha inicializado variable de entorno ENDPOINT_REPORTAR_MASCOTA'
    except Exception as e:
        print(e)
        return False, None

def eliminar_archivos_temporales(filename):
    try:
        print('Eliminar el archivo temporal {}'.format(filename))
        os.remove(filename)
    except AssertionError as error:
        print(error)
        print('Error al eliminar el archivo temporal {}'.format(filename))
from .util import ENDPOINT_DOG_FACE_CROPPER, ENDPOINT_TENSORFLOW_MODEL, REPOSITORIO_DE_IMAGENES_PUBLICAS, ENDPOINT_REPORTAR_MASCOTA
import numpy as np
import json
import requests
import os
import io
import base64
from PIL import Image

def obtener_imagen_recortada(data, nombre_imagen_recortada):
    print('obtener_imagen_recortada')
    try:
        # Recortar imagen
        file_imagen = data
        files = {'upload_file': file_imagen}
        url = ENDPOINT_DOG_FACE_CROPPER

        response = requests.post(url, files=files)
        print('respuesta')
        print(type(json.loads(response.text)['img']))
        # Guardar bytecode como imagen
        imgdata = base64.b64decode(json.loads(response.text)['img'])
        print(type(imgdata))

        print('nombre_imagen_recortada')
        #with open(nombre_imagen_recortada, 'wb') as f:
        #    f.write(imgdata)
        return True, imgdata
    except Exception as e:
        print(e)
        return False, None

def obtener_mascotas_parecidas(image_bytes):
    print('obtener_mascotas_parecidas')
    try:
        # Predecir perros
        file_imagen = image_bytes
        files = {'upload_file': file_imagen}
        url = ENDPOINT_TENSORFLOW_MODEL

        response = requests.post(url, files=files)
        print('Respuesta de la red neuronal: {}'.format(response.text))
        respuesta = response.text.replace('"/static/', ('"' + REPOSITORIO_DE_IMAGENES_PUBLICAS))
        predictions = json.loads(respuesta)

        print('Predicción: {}'.format(predictions))
        
        return predictions
    except Exception as e:
        print(e)
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
        
        return True, respuesta
    except Exception as e:
        print(e)
        file_imagen.close()
        return False, None

def eliminar_archivos_temporales(filename):
    try:
        print('Eliminar el archivo temporal {}'.format(filename))
        os.remove(filename)
    except AssertionError as error:
        print(error)
        print('Error al eliminar el archivo temporal {}'.format(filename))
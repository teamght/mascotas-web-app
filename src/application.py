from .util import ENDPOINT_TENSORFLOW_MODEL, ENDPOINT_REPORTAR_MASCOTA
import json
import requests

def obtener_mascotas_parecidas(image_bytes, geolocalizacion):
    print('obtener_mascotas_parecidas')
    try:
        # Predecir perros
        if ENDPOINT_TENSORFLOW_MODEL:
            files = {'imagen_bytes': image_bytes, 'geolocalizacion': geolocalizacion}
            response = requests.post(ENDPOINT_TENSORFLOW_MODEL, json=files)

            print('Respuesta de la red neuronal: {}'.format(response.text))
            predictions = json.loads(response.text)

            print('Predicción: {}'.format(predictions))
            if predictions['codigo'] == 200:
                return True, predictions
        
            return False, predictions
        return False, 'No se ha inicializado variable de entorno ENDPOINT_TENSORFLOW_MODEL'
    except Exception as e:
        print(e)
        return False, None

def reportar_mascota_desaparecida(image_bytes, geolocalizacion, caracteristicas, fecha_de_perdida):
    try:
        if ENDPOINT_REPORTAR_MASCOTA:
            files = {'imagen_bytes': image_bytes, 
                     'geolocalizacion': geolocalizacion, 
                     'caracteristicas':caracteristicas,
                     'fecha_de_perdida': fecha_de_perdida}
            response = requests.post(ENDPOINT_REPORTAR_MASCOTA, json=files)
            print('Respuesta: {}'.format(response.text))
            respuesta = json.loads(response.text)
            
            return True, respuesta
        return False, 'No se ha inicializado variable de entorno ENDPOINT_REPORTAR_MASCOTA'
    except Exception as e:
        print(e)
        return False, None

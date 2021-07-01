from .util import ENDPOINT_TENSORFLOW_MODEL, ENDPOINT_REPORTAR_MASCOTA
import json
import requests

def obtener_mascotas_parecidas(mascota_desaparecida, flag_bytes_url):
    print('obtener_mascotas_parecidas')
    try:
        # Predecir perros
        if ENDPOINT_TENSORFLOW_MODEL:
            files = {'geolocalizacion': mascota_desaparecida.geolocalizacion_reportado,
                     'caracteristicas': mascota_desaparecida.caracteristicas,
                     'fecha_de_perdida': mascota_desaparecida.fecha_de_perdida,
                     'barrio_nombre': mascota_desaparecida.barrio_nombre,
                     'genero': mascota_desaparecida.genero, 
                     'perro_nombre': mascota_desaparecida.perro_nombre, 
                     'comportamiento': mascota_desaparecida.comportamiento, 
                     'datos_adicionales': mascota_desaparecida.datos_adicionales,
                     'dueno': {'identificador':mascota_desaparecida.dueno.identificador}}
            if flag_bytes_url == 'bytes':
                files['lista_imagenes_bytes'] = mascota_desaparecida.lista_imagenes_bytes
            if flag_bytes_url == 'url':
                files['lista_imagenes_url'] = mascota_desaparecida.lista_imagenes_bytes
            response = requests.post(ENDPOINT_TENSORFLOW_MODEL, json=files)

            #print('Respuesta de la red neuronal: {}'.format(response.text))
            predictions = json.loads(response.text)

            #print('Predicción: {}'.format(predictions))
            if predictions['codigo'] == 200:
                return True, predictions
        
            return False, predictions
        return False, 'No se ha inicializado variable de entorno ENDPOINT_TENSORFLOW_MODEL'
    except Exception as e:
        print(e)
        return False, None

def reportar_mascota_desaparecida(mascota_desaparecida):
    try:
        if ENDPOINT_REPORTAR_MASCOTA:
            files = {'imagen_bytes': mascota_desaparecida.imagen_bytes, 
                     'geolocalizacion': mascota_desaparecida.geolocalizacion_reportado, 
                     'caracteristicas': mascota_desaparecida.caracteristicas,
                     'fecha_de_perdida': mascota_desaparecida.fecha_de_perdida,
                     'barrio_nombre': mascota_desaparecida.barrio_nombre,
                     'genero': mascota_desaparecida.genero, 
                     'perro_nombre': mascota_desaparecida.perro_nombre, 
                     'comportamiento': mascota_desaparecida.comportamiento, 
                     'datos_adicionales': mascota_desaparecida.datos_adicionales}
            response = requests.post(ENDPOINT_REPORTAR_MASCOTA, json=files)
            print('Respuesta: {}'.format(response.text))
            respuesta = json.loads(response.text)
            
            return True, respuesta
        return False, 'No se ha inicializado variable de entorno ENDPOINT_REPORTAR_MASCOTA'
    except Exception as e:
        print(e)
        return False, None

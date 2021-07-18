from .util import ENDPOINT_MASCOTAS
import json
import requests

class Application():

    def __init__(self):
        pass
    
    def obtener_mascotas_parecidas(self, mascota_desaparecida, flag_bytes_url):
        print('obtener_mascotas_parecidas')
        try:
            # Predecir perros
            if ENDPOINT_MASCOTAS:
                files = {'geolocalizacion': mascota_desaparecida.geolocalizacion_reportado,
                        'caracteristicas': mascota_desaparecida.caracteristicas,
                        'fecha_de_perdida': mascota_desaparecida.fecha_de_perdida,
                        'barrio_nombre': mascota_desaparecida.barrio_nombre,
                        'genero': mascota_desaparecida.genero, 
                        'nombre': mascota_desaparecida.nombre, 
                        'comportamiento': mascota_desaparecida.comportamiento, 
                        'datos_adicionales': mascota_desaparecida.datos_adicionales,
                        'estado': mascota_desaparecida.estado,
                        'dueno': mascota_desaparecida.dueno.__dict__}
                if flag_bytes_url == 'bytes':
                    files['lista_imagenes_bytes'] = mascota_desaparecida.lista_imagenes_bytes
                if flag_bytes_url == 'url':
                    files['lista_imagenes_url'] = mascota_desaparecida.lista_imagenes_bytes
                response = requests.post(ENDPOINT_MASCOTAS + '/busqueda', json=files)

                #print('Respuesta de la red neuronal: {}'.format(response.text))
                predictions = json.loads(response.text)

                #print('Predicción: {}'.format(predictions))
                if predictions['codigo'] == 200:
                    return True, predictions
            
                return False, predictions
            return False, 'No se ha inicializado variable de entorno ENDPOINT_MASCOTAS'
        except Exception as e:
            print(e)
            return False, None

    def reportar_mascota_desaparecida(self, mascota_desaparecida):
        try:
            if ENDPOINT_MASCOTAS:
                files = {'lista_imagenes_bytes': mascota_desaparecida.lista_imagenes_bytes, 
                        'geolocalizacion': mascota_desaparecida.geolocalizacion_reportado, 
                        'caracteristicas': mascota_desaparecida.caracteristicas,
                        'fecha_de_perdida': mascota_desaparecida.fecha_de_perdida,
                        'barrio_nombre': mascota_desaparecida.barrio_nombre,
                        'genero': mascota_desaparecida.genero, 
                        'nombre': mascota_desaparecida.nombre, 
                        'comportamiento': mascota_desaparecida.comportamiento, 
                        'datos_adicionales': mascota_desaparecida.datos_adicionales,
                        'estado': mascota_desaparecida.estado,
                        'dueno': mascota_desaparecida.dueno.__dict__}
                response = requests.post(ENDPOINT_MASCOTAS, json=files)
                print('Respuesta: {}'.format(response.text))
                respuesta = json.loads(response.text)
                
                return True, respuesta
            return False, 'No se ha inicializado variable de entorno ENDPOINT_MASCOTAS'
        except Exception as e:
            print(e)
            return False, str(e)

    def actualizar_data_mascota_desaparecida(self, json_mascota_desaparecida):
        '''
        Actualizar valores de los campos en base de datos
        '''
        try:
            if ENDPOINT_MASCOTAS:
                response = requests.put(ENDPOINT_MASCOTAS + '/data', json=json_mascota_desaparecida)
                print('Respuesta: {}'.format(response.text))
                respuesta = json.loads(response.text)
                return True, respuesta
            return False, 'No se ha inicializado variable de entorno ENDPOINT_MASCOTAS'
        except Exception as e:
            print(e)
            return False, str(e)
    
    def eliminar_mascota_desaparecida(self, json_mascota_desaparecida):
        '''
        Eliminar datos de la mascota
        '''
        try:
            if ENDPOINT_MASCOTAS:
                response = requests.delete(ENDPOINT_MASCOTAS, json=json_mascota_desaparecida)
                print('Respuesta: {}'.format(response.text))
                respuesta = json.loads(response.text)
                return True, respuesta
            return False, 'No se ha inicializado variable de entorno ENDPOINT_MASCOTAS'
        except Exception as e:
            print(e)
            return False, str(e)
    
    def encontrar_mascota_desaparecida(self, json_mascota_desaparecida):
        '''
        Actualizar estado de la mascota a encontrada
        '''
        try:
            if ENDPOINT_MASCOTAS:
                response = requests.put(ENDPOINT_MASCOTAS, json=json_mascota_desaparecida)
                print('Respuesta: {}'.format(response.text))
                respuesta = json.loads(response.text)
                return True, respuesta
            return False, 'No se ha inicializado variable de entorno ENDPOINT_MASCOTAS'
        except Exception as e:
            print(e)
            return False, str(e)

    def obtener_ownerpets(self, json_mascota_desaparecida):
        '''
        Obtener todas las mascotas reportadas como desaparecidas
        Sólo retorna las mascotas que aún siguen desaparecidas
        '''
        try:
            if ENDPOINT_MASCOTAS:
                response = requests.post(ENDPOINT_MASCOTAS + '/ownerpets', json=json_mascota_desaparecida)
                print('Respuesta: {}'.format(response.text))
                respuesta = json.loads(response.text)
                return True, respuesta
            return False, 'No se ha inicializado variable de entorno ENDPOINT_MASCOTAS'
        except Exception as e:
            print(e)
            return False, str(e)

    def empadronar_mascota(self, json_mascota):
        '''
        Empadronar mascota
        '''
        try:
            if ENDPOINT_MASCOTAS:
                response = requests.post(ENDPOINT_MASCOTAS + '/data', json=json_mascota)
                print('Respuesta: {}'.format(response.text))
                respuesta = json.loads(response.text)
                return True, respuesta
            return False, 'No se ha inicializado variable de entorno ENDPOINT_MASCOTAS'
        except Exception as e:
            print(e)
            return False, str(e)


class NumpyValuesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

from flask import Flask, render_template, request, jsonify

import os
import base64

from datetime import datetime

from src.mascota_reportar_request import MascotaReportartRequest
from src.application import obtener_mascotas_parecidas, reportar_mascota_desaparecida
from src.util import mostrar_cadena_vacia, existe_campo_en_diccionario


port = int(os.environ.get("PORT", 5001))

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Mascotas', ims={})

@app.route('/search', methods=['GET','POST'])
def search_func():
    dict_respuesta = {}
    fecha_busqueda = datetime.now()
    print('Inicio de búsqueda de mascota: {}'.format(fecha_busqueda))
    try:
        data = request.json
        print(data.keys())
        if data is None:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400}
        if not 'imagen_1' in data:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400}
        
        bytes_imagen = [data['imagen_1']]

        if 'imagen_2' in data:
            bytes_imagen.append(data['imagen_2'])
        if 'imagen_3' in data:
            bytes_imagen.append(data['imagen_3'])
        
        geolocalizacion = data['geolocalizacion']
        
        flag, respuesta = obtener_mascotas_parecidas(bytes_imagen, geolocalizacion)
        
        if 'resultados' in respuesta:
            for key,value in respuesta['resultados'].items():
                dict_respuesta[key] = {'id':existe_campo_en_diccionario(value, 'id'),
                                        'image':value['image'],
                                        'caracteristicas':value['caracteristicas'],
                                        'ubicacion':value['ubicacion'],
                                        'label':value['label'],
                                        'distancia':value['distancia'],
                                        'fecha_de_perdida':value['fecha_perdida'],
                                        'timestamp_perdida':value['timestamp_perdida'],
                                        'barrio_nombre':mostrar_cadena_vacia(existe_campo_en_diccionario(value, 'barrio_nombre')),
                                        'genero':mostrar_cadena_vacia(existe_campo_en_diccionario(value, 'genero')),
                                        'perro_nombre':mostrar_cadena_vacia(existe_campo_en_diccionario(value, 'nombre')), 
                                        'comportamiento':mostrar_cadena_vacia(existe_campo_en_diccionario(value, 'comportamiento')),
                                        'datos_adicionales':mostrar_cadena_vacia(existe_campo_en_diccionario(value, 'datos_adicionales'))
                                        }
        
        if 'imagen_recortada' in respuesta:
            dict_respuesta["imagen_recortada"] = respuesta["imagen_recortada"]
        
        dict_respuesta['codigo'] = respuesta['codigo']
        dict_respuesta['mensaje'] = respuesta['mensaje']
    except Exception as e:
        print('Hubo un error en la búsqueda de mascota: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        dict_respuesta['codigo'] = 503
        dict_respuesta['mensaje'] = 'Hubo un error. Volver a ingresar la imagen.'
        return jsonify(dict_respuesta)
    
    print('Fin de búsqueda de mascota: {}'.format(datetime.now()))
    return jsonify(dict_respuesta)

@app.route('/reportar', methods=['POST'])
def reportar_func():
    fecha_busqueda = datetime.now()
    print('Inicio de reportar mascota desaparecida: {}'.format(fecha_busqueda))

    dict_respuesta = {}
    try:
        if not os.path.exists('./static/'):
            os.mkdir('./static/')
        
        data = request.json
        
        if data is None:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400}
        if not 'imagen' in data:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400}
        
        bytes_imagen = data['imagen']
        caracteristicas = data['caracteristicas']
        geolocalizacion = data['geolocalizacion']
        fecha_de_perdida = data['fecha_de_perdida'] if 'fecha_de_perdida' in data else '25/05/2020'
        barrio_nombre = data['barrio_nombre'] if 'barrio_nombre' in data else None
        genero = data['genero'] if 'genero' in data else None # Hembra (0) / Macho (1)
        perro_nombre = data['perro_nombre'] if 'perro_nombre' in data else None
        comportamiento = data['comportamiento'] if 'comportamiento' in data else None
        datos_adicionales = data['datos_adicionales'] if 'datos_adicionales' in data else None

        mascota_desaparecida = MascotaReportartRequest(geolocalizacion, bytes_imagen, caracteristicas, fecha_de_perdida, 
                                            barrio_nombre, genero, perro_nombre, comportamiento, datos_adicionales)
        
        #
        # Registrar en memoria la imagen reportada
        #
        flag, dict_respuesta = reportar_mascota_desaparecida(mascota_desaparecida)
        ## Respuesta variable dict_respuesta:
        # dict_respuesta['file_name']
        # dict_respuesta['label']
        # dict_respuesta['full_file_name']
        # dict_respuesta['codigo']
        # dict_respuesta['mensaje']

        if not flag:
            return jsonify(dict_respuesta)
        
        print('Fin de reportar mascota desaparecida: {}'.format(datetime.now()))
        return jsonify(dict_respuesta)
    except Exception as e:
        print('Hubo un error al reportar mascota desaparecida: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        return {'mensaje':'Hubo un error. Volver a reportar desaparición.'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
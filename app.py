from flask import Flask, render_template, request, jsonify

import os
import base64

from datetime import datetime

from src.application import obtener_imagen_recortada, obtener_mascotas_parecidas, reportar_mascota_desaparecida,eliminar_archivos_temporales


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
        if data is None:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400}
        if not 'imagen' in data:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400}
        
        bytes_imagen = data['imagen']
        geolocalizacion = data['geolocalizacion']
        
        flag, bytes_imagen_recortada = obtener_imagen_recortada(bytes_imagen)
        
        print('bytes_imagen_recortada')
        print(type(bytes_imagen_recortada))
        if flag == False:
            return jsonify('Hubo un error. Ingresar una nueva imagen.')

        dict_respuesta["imagen_recortada"] = base64.b64encode(bytes_imagen_recortada).decode("utf-8")
        
        flag, respuesta = obtener_mascotas_parecidas(dict_respuesta["imagen_recortada"], geolocalizacion)
        if flag == False:
            dict_respuesta['codigo'] = 404
            dict_respuesta['mensaje'] = 'Hubo un error al mostrar mascotas. Volver a ingresar la imagen.'
            return jsonify(dict_respuesta)
        
        if 'parecidos' in respuesta:
            for key,value in respuesta['parecidos'].items():
                dict_respuesta[key] = {'rutas':value['image'],
                                        'caracteristicas':value['caracteristicas'],
                                        'ubicacion':value['ubicacion'],
                                        'label':value['label'],
                                        'distancia':value['distancia'],
                                        'fecha_perdida':value['fecha_perdida'],
                                        'timestamp_perdida':value['timestamp_perdida']
                                        }

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
        fecha_de_perdida = '25/05/2020'

        #
        # Registrar en memoria la imagen reportada
        #
        flag, dict_respuesta = reportar_mascota_desaparecida(bytes_imagen, geolocalizacion, caracteristicas, fecha_de_perdida)
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
from flask import Flask, render_template, request, jsonify

import os
import json
import base64

import random
from datetime import datetime


from azure.storage.blob import BlockBlobService

import pymongo
from src.util import ACCOUNT_NAME, ACCOUNT_KEY, CONTAINER_NAME, ENDPOINT_TENSORFLOW_MODEL, DB_URI, DB_NAME, DB_COLECCION
from src.mongodb_config import MongoDB_Config
from src.application import obtener_imagen_recortada, obtener_mascotas_parecidas, reportar_mascota_desaparecida,eliminar_archivos_temporales


port = int(os.environ.get("PORT", 5001))

app = Flask(__name__)

# MongoDB
mongodb = MongoDB_Config()

#
# Configuración de cuenta de Azure
#
block_blob_service = BlockBlobService(
    account_name=ACCOUNT_NAME,
    account_key=ACCOUNT_KEY
)

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
        data = request.files['img']
        
        flag, img_recortada = obtener_imagen_recortada(data)
        print('img_recortada')
        print(type(img_recortada))
        if flag == False:
            return jsonify('Hubo un error. Volver a ingresar la imagen.')

        dict_respuesta["imagen_recortada"] = base64.b64encode(img_recortada).decode("utf-8")
        
        flag, respuesta = obtener_mascotas_parecidas(img_recortada)
        if flag == False:
            return jsonify('Hubo un error al mostrar mascotas. Volver a ingresar la imagen.')
        
        if 'parecidos' in respuesta:
            for key,value in respuesta['parecidos'].items():    
                dict_respuesta[key] = {'rutas':value['image'],
                                        'caracteristicas':value['caracteristicas'],
                                        'distancia':value['distancia']}

        dict_respuesta['codigo'] = respuesta['codigo']
        dict_respuesta['mensaje'] = respuesta['mensaje']
    except Exception as e:
        print('Hubo un error en la búsqueda de mascota: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        return jsonify('Hubo un error. Volver a ingresar la imagen.')
    
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
        
        #Aca se agrega la descripcion del input
        caracteristicas = request.form.get('inputdesc')

        data = request.files['img']

        current_date = datetime.utcnow().strftime('%Y-%m-%d_%H%M%S.%f')[:-3]
        nombre_imagen = 'image_{}.jpg'.format(current_date)
        file_path = './static' + '/' + nombre_imagen

        print(current_date)
        print(file_path)

        with open(file_path, 'wb') as f:
            f.write(data.read())

        #
        # Registrar en memoria la imagen reportada
        #
        flag, dict_respuesta = reportar_mascota_desaparecida(file_path)
        ## Respuesta variable dict_respuesta:
        # dict_respuesta['file_name']
        # dict_respuesta['label']
        # dict_respuesta['full_file_name']

        if not flag:
            dict_respuesta['mensaje'] = "Hubo un error. Volver a ingresar la imagen."
            return dict_respuesta
        
        #
        # Guardar imagen en Azure Storage
        #
        # Nombre con el que se guardará en Azure Storage
        full_file_name = dict_respuesta['full_file_name']
        print(full_file_name)
        print(file_path)
        block_blob_service.create_blob_from_path(CONTAINER_NAME, full_file_name, file_path)

        #
        # Guardar en base de datos
        #
        # Genero un valor random para la distancia
        distancia = str(random.randint(0,999))+' km.'
        file_name = dict_respuesta['file_name']
        label = dict_respuesta['label']
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        
        flag, respuesta = mongodb.registrar_mascota_reportada(encoded_string=encoded_string, full_file_name=full_file_name, image_path=file_name, label=label, caracteristicas=caracteristicas, distancia=distancia)
        if not flag:
            dict_respuesta['mensaje'] = "Hubo un error. Volver a ingresar la imagen."
            return dict_respuesta
        
        dict_respuesta['mensaje'] = respuesta

        eliminar_archivos_temporales(file_path)

        return json.dumps(dict_respuesta)
    except Exception as e:
        print('Hubo un error al reportar mascota desaparecida: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        eliminar_archivos_temporales(file_path)
        return {'mensaje':'Hubo un error. Volver a reportar desaparición.'}

    #print('Fin de reportar mascota desaparecida: {}'.format(datetime.now()))
    #return {'mensaje':'Se logró registrar mascota como desaparecida.'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
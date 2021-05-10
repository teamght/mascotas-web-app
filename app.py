from flask import Flask, render_template, request, jsonify
import pymongo
from src.util import ENDPOINT_TENSORFLOW_MODEL, DB_URI, DB_NAME, DB_COLECCION
from src.application import obtener_imagen_recortada, obtener_mascotas_parecidas, reportar_mascota_desaparecida,eliminar_archivos_temporales
from datetime import datetime
import json
from flask_mongoengine import MongoEngine
from skimage.io import imread
import os
import base64
import random

port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

# MongoDB
client = pymongo.MongoClient(DB_URI)
db = client[DB_NAME]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Mascotas', ims={})

@app.route('/search', methods=['GET','POST'])
def search_func():
    dict_rta = {}
    fecha_busqueda = datetime.now()
    print('Inicio de búsqueda de mascota: {}'.format(fecha_busqueda))
    try:
        if not os.path.exists('./static/'):
            os.mkdir('./static/')
        
        current_date = datetime.utcnow().strftime('%Y-%m-%d_%H%M%S.%f')[:-3]
        #nombre_imagen_a_predecir = './static/image_{}.jpg'.format(current_date)
        nombre_imagen_recortada = './static/image_crop_{}.jpg'.format(current_date)
        #if request.method == 'POST':
        #    file = request.files['img']
        #    file.save(nombre_imagen_a_predecir)
        data = request.files['img']
        
        flag, img_recortada = obtener_imagen_recortada(data, nombre_imagen_recortada)
        print('img_recortada')
        print(type(img_recortada))
        if flag == False:
            return jsonify('Hubo un error. Volver a ingresar la imagen.')
        respuesta = obtener_mascotas_parecidas(img_recortada)

        
        for key,value in respuesta.items():    
            #resp_mascota = Mascota.objects(file_name=str(value['image'])).first()
            
            #if resp_mascota:
            #    dict_rta[key] = {'rutas':value['image'],
            #                    'caracteristicas':resp_mascota['caracteristicas'],
            #                    'distancia':resp_mascota['distancia']}
            #else:
            #    dict_rta[key] = {'rutas':value['image'],
            #                    'caracteristicas':'',
            #                    'distancia':''}
            dict_rta[key] = {'rutas':value['image'],
                            'caracteristicas':value['caracteristicas'],
                            'distancia':value['distancia']}
            

        #with open(nombre_imagen_recortada, "rb") as image_file:
        #    encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        #dict_rta["imagen_recortada"] = encoded_string
        dict_rta["imagen_recortada"] = base64.b64encode(img_recortada).decode("utf-8")
        
        #eliminar_archivos_temporales(nombre_imagen_a_predecir)
        #eliminar_archivos_temporales(nombre_imagen_recortada)
    except Exception as e:
        print('Hubo un error en la búsqueda de mascota: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        #eliminar_archivos_temporales(nombre_imagen_a_predecir)
        #eliminar_archivos_temporales(nombre_imagen_recortada)
        return jsonify('Hubo un error. Volver a ingresar la imagen.')
    
    print('Fin de búsqueda de mascota: {}'.format(datetime.now()))
    return jsonify(dict_rta)

@app.route('/reportar', methods=['POST'])
def reportar_func():
    fecha_busqueda = datetime.now()
    print('Inicio de reportar mascota desaparecida: {}'.format(fecha_busqueda))
    try:
        if not os.path.exists('./static/'):
            os.mkdir('./static/')
        
        current_date = datetime.utcnow().strftime('%Y-%m-%d_%H%M%S.%f')[:-3]
        nombre_imagen_a_predecir = './static/image_{}.jpg'.format(current_date)
        
        #Aca se agrega la descripcion del input
        caracteristicas = request.form.get('inputdesc')

        file = request.files['img']
        file.save(nombre_imagen_a_predecir)
        flag, dict_respuesta = reportar_mascota_desaparecida(nombre_imagen_a_predecir)

        if not flag:
            print('Hubo un error. {}'.format(e))
            return {'mensaje':'Hubo un error. Volver a reportar desaparición.'}
        #
        # Guardar en base de datos
        #
        #Genero un valor random para la distancia
        distancia = str(random.randint(0,999))+' km.'
        
        with open(nombre_imagen_a_predecir, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        
        db[DB_COLECCION].insert_one({
                    'image':encoded_string, 
                    'file_name':dict_respuesta['file_name'],
                    'label':dict_respuesta['label'],
                    'caracteristicas':caracteristicas,
                    'distancia':distancia})
            
        eliminar_archivos_temporales(nombre_imagen_a_predecir)
        
    except Exception as e:
        print('Hubo un error al reportar mascota desaparecida: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        eliminar_archivos_temporales(nombre_imagen_a_predecir)
        return {'mensaje':'Hubo un error. Volver a reportar desaparición.'}

    print('Fin de reportar mascota desaparecida: {}'.format(datetime.now()))
    return {'mensaje':'Se logró registrar mascota como desaparecida.'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
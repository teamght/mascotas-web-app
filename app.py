from flask import Flask, render_template, request, jsonify

import os
import base64
import json
from datetime import datetime

from src.mascota_reportar_request import MascotaDuenoRequest, MascotaEncontrarRequest, MascotaReportartRequest
from src.application import Application,NumpyValuesEncoder
from src.util import mostrar_cadena_vacia, existe_campo_en_diccionario, retornar_valor_campo_en_diccionario


port = int(os.environ.get("PORT", 5001))

app = Flask(__name__)

application_consumer = Application()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Mascotas', ims={})

@app.route('/index_bytes')
def index_bytes():
    return render_template('index_bytes.html', title='Mascotas', ims={})

@app.route('/mascotas/busqueda', methods=['POST'])
def search_func():
    dict_respuesta = {}
    print('Inicio de búsqueda de mascota: {}'.format(datetime.now()))
    try:
        data = request.json
        
        if data is None:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400},400
        if not 'lista_imagenes_bytes' in data and not 'lista_imagenes_url' in data:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400},400
        
        flag_bytes_url = 'url'
        if 'lista_imagenes_bytes' in data:
            lista_imagenes_bytes = data['lista_imagenes_bytes']
            flag_bytes_url = 'bytes'
        if 'lista_imagenes_url' in data:
            lista_imagenes_bytes = data['lista_imagenes_url']
            flag_bytes_url = 'url'

        if len(lista_imagenes_bytes) == 0:
            return {'mensaje':'Debe ingresar al menos una imagen.', 'codigo': 400},400

        # Datos del dueño
        dueno = retornar_valor_campo_en_diccionario(data, 'dueno')
        if not dueno is None:
            identificador = retornar_valor_campo_en_diccionario(data['dueno'], 'identificador')  # Número telefónico de la persona que reportó desaparición
            email = retornar_valor_campo_en_diccionario(data['dueno'], 'email') # Correo electrónico de la persona que reportó desaparición
            contacto = retornar_valor_campo_en_diccionario(data['dueno'], 'contacto')  # Números de teléfonos asociados al perro desaparecido
            mascota_dueno_datos = MascotaDuenoRequest(identificador, email, contacto)
        
        caracteristicas = data['caracteristicas']
        geolocalizacion = data['geolocalizacion']
        fecha_de_perdida = data['fecha_de_perdida'] if 'fecha_de_perdida' in data else '25/05/2020'
        barrio_nombre = data['barrio_nombre'] if 'barrio_nombre' in data else None
        genero = data['genero'] if 'genero' in data else None # Hembra (0) / Macho (1)
        perro_nombre = data['nombre'] if 'nombre' in data else None
        comportamiento = data['comportamiento'] if 'comportamiento' in data else None
        datos_adicionales = data['datos_adicionales'] if 'datos_adicionales' in data else None
        estado = data['estado'] if 'estado' in data else None
        
        mascota_desaparecida = MascotaEncontrarRequest(mascota_dueno_datos, geolocalizacion, lista_imagenes_bytes, caracteristicas, fecha_de_perdida, 
                                            barrio_nombre, genero, perro_nombre, comportamiento, datos_adicionales, estado)
        
        flag, respuesta = application_consumer.obtener_mascotas_parecidas(mascota_desaparecida, flag_bytes_url)
        
        if 'resultados' in respuesta:
            dict_respuesta['resultados'] = respuesta['resultados']
        
        if 'imagenes_recortadas' in respuesta:
            dict_respuesta["imagenes_recortadas"] = respuesta["imagenes_recortadas"]
        
        if 'mascota' in respuesta:
            dict_respuesta["mascota"] = respuesta["mascota"]
        
        if 'list_encoded_string' in respuesta:
            dict_respuesta["list_encoded_string"] = respuesta["list_encoded_string"]
        
        dict_respuesta['codigo'] = respuesta['codigo']
        dict_respuesta['mensaje'] = respuesta['mensaje']
    except Exception as e:
        print('Hubo un error en la búsqueda de mascota: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        dict_respuesta['codigo'] = 503
        dict_respuesta['mensaje'] = 'Hubo un error. Volver a ingresar la imagen.'
        return jsonify(dict_respuesta),dict_respuesta['codigo']
    
    print('Fin de búsqueda de mascota: {}'.format(datetime.now()))
    return jsonify(dict_respuesta),200

@app.route('/mascotas', methods=['POST'])
def mascota_reportar():
    print('Inicio de reportar mascota desaparecida: {}'.format(datetime.now()))

    dict_respuesta = {}
    try:
        if not os.path.exists('./static/'):
            os.mkdir('./static/')
        
        data = request.json
        
        if data is None:
            return {'mensaje':'Debe ingresar una imagen.', 'codigo': 400},400
        if not 'lista_imagenes_bytes' in data:
            return {'mensaje':'Debe ingresar al menos una imagen.', 'codigo': 400},400
        
        lista_imagenes_bytes = data['lista_imagenes_bytes']
        # Datos del dueño
        dueno = retornar_valor_campo_en_diccionario(data, 'dueno')
        if not dueno is None:
            identificador = retornar_valor_campo_en_diccionario(data['dueno'], 'identificador')  # Número telefónico de la persona que reportó desaparición
            email = retornar_valor_campo_en_diccionario(data['dueno'], 'email') # Correo electrónico de la persona que reportó desaparición
            contacto = retornar_valor_campo_en_diccionario(data['dueno'], 'contacto')  # Números de teléfonos asociados al perro desaparecido
            mascota_dueno_datos = MascotaDuenoRequest(identificador, email, contacto)
        
        caracteristicas = data['caracteristicas']
        geolocalizacion = data['geolocalizacion']
        fecha_de_perdida = data['fecha_de_perdida'] if 'fecha_de_perdida' in data else '25/05/2020'
        barrio_nombre = data['barrio_nombre'] if 'barrio_nombre' in data else None
        genero = data['genero'] if 'genero' in data else None # Hembra (0) / Macho (1)
        perro_nombre = data['nombre'] if 'nombre' in data else None
        comportamiento = data['comportamiento'] if 'comportamiento' in data else None
        datos_adicionales = data['datos_adicionales'] if 'datos_adicionales' in data else None
        estado = data['estado'] if 'estado' in data else None
        
        mascota_desaparecida = MascotaReportartRequest(mascota_dueno_datos, geolocalizacion, lista_imagenes_bytes, caracteristicas, fecha_de_perdida, 
                                            barrio_nombre, genero, perro_nombre, comportamiento, datos_adicionales, estado)
        
        #
        # Registrar en memoria la imagen reportada
        #
        flag, dict_respuesta = application_consumer.reportar_mascota_desaparecida(mascota_desaparecida)
        ## Respuesta variable dict_respuesta:
        # dict_respuesta['file_name']
        # dict_respuesta['label']
        # dict_respuesta['full_file_name']
        # dict_respuesta['codigo']
        # dict_respuesta['mensaje']

        if not flag:
            return jsonify(dict_respuesta),200
        
        print('Fin de reportar mascota desaparecida: {}'.format(datetime.now()))
        return jsonify(dict_respuesta),200
    except Exception as e:
        print('Hubo un error al reportar mascota desaparecida: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        return {'mensaje':'Hubo un error. Volver a reportar desaparición.'},400

@app.route('/mascotas/data', methods=['PUT'])
def mascotas_update_data():
    print('Inicio de actualización de datos de mascota desaparecida: {}'.format(datetime.now()))
    dict_respuesta = {}
    try:
        data = request.json
        
        if data == None:
            return {'mensaje':'No se identifico objetos dentro del payload.', 'codigo': 400},400
        else:
            flag, dict_respuesta = application_consumer.actualizar_data_mascota_desaparecida(data)
            
            if not flag:
                return jsonify(dict_respuesta),500

            print('Fin de actualización de datos de mascota desaparecida: {}'.format(datetime.now()))
            return jsonify(dict_respuesta),dict_respuesta['codigo']
    except Exception as e:
        print('Hubo un error al actualizar datos de mascota desaparecida ({}): {}'.format(datetime.now(), e))
        return {'mensaje':'Hubo un error al actualizar datos de mascota.', 'codigo': 503},503

@app.route('/mascotas/data', methods=['POST'])
def mascotas_insert_data():
    print('Inicio de empadronamiento de mascota {}'.format(datetime.now()))
    dict_respuesta = {}
    try:
        data = request.json
        
        if data == None:
            return {'mensaje':'No se identifico objetos dentro del payload.', 'codigo': 400},400
        else:
            flag, dict_respuesta = application_consumer.empadronar_mascota(data)
            
            if not flag:
                return jsonify(dict_respuesta),500

            print('Fin de empadronamiento de mascota: {}'.format(datetime.now()))
            return jsonify(dict_respuesta),dict_respuesta['codigo']
    except Exception as e:
        print('Hubo un error al empadronar la mascota ({}): {}'.format(datetime.now(), e))
        return {'mensaje':'Hubo un error al empadronar la mascota.', 'codigo': 503},503


@app.route('/mascotas', methods=['DELETE'])
def mascotas_delete():
    print('Inicio de eliminación de datos de mascota desaparecida: {}'.format(datetime.now()))
    dict_respuesta = {}
    try:
        data = request.json
        
        if data == None:
            return {'mensaje':'No se identifico objetos dentro del payload.', 'codigo': 400},400
        else:
            flag, dict_respuesta = application_consumer.eliminar_mascota_desaparecida(data)
            
            if not flag:
                return jsonify(dict_respuesta),500

            print('Fin de eliminación de datos de mascota desaparecida: {}'.format(datetime.now()))
            return jsonify(dict_respuesta),dict_respuesta['codigo']
    except Exception as e:
        print('Hubo un error al eliminar datos de mascota desaparecida ({}): {}'.format(datetime.now(), e))
        return {'mensaje':'Hubo un error al eliminar datos de mascota.', 'codigo': 503},503

@app.route('/mascotas', methods=['PUT'])
def mascotas_encontrada():
    print('Inicio de actualización de estado de mascota desaparecida a encontrada: {}'.format(datetime.now()))
    dict_respuesta = {}
    try:
        data = request.json
        
        if data == None:
            return {'mensaje':'No se identifico objetos dentro del payload.', 'codigo': 400},400
        else:
            flag, dict_respuesta = application_consumer.encontrar_mascota_desaparecida(data)
            
            if not flag:
                return jsonify(dict_respuesta),500

            print('Fin de actualización de estado de mascota desaparecida a encontrada: {}'.format(datetime.now()))
            return jsonify(dict_respuesta),dict_respuesta['codigo']
    except Exception as e:
        print('Hubo un error al actualizar estado de mascota desaparecida a encontrada ({}): {}'.format(datetime.now(), e))
        return {'mensaje':'Hubo un error al actualizar estado de mascota desaparecida a encontrada.', 'codigo': 500},500

@app.route('/mascotas/ownerpets', methods=['POST'])
def ownerpets():
    print('Inicio de listar las mascotas de un dueño: {}'.format(datetime.now()))
    dict_respuesta = {}
    try:
        data = request.json
        
        if data == None:
            return {'mensaje':'No se identifico objetos dentro del payload.', 'codigo': 400},400
        else:
            flag, dict_respuesta = application_consumer.obtener_ownerpets(data)
            
            if not flag:
                return jsonify(dict_respuesta),500

            print('Fin de listar las mascotas de un dueño: {}'.format(datetime.now()))
            return jsonify(dict_respuesta),dict_respuesta['codigo']
    except Exception as e:
        print('Hubo un error al actualizar estado de mascota desaparecida a encontrada ({}): {}'.format(datetime.now(), e))
        return {'mensaje':'Hubo un error al listar las mascotas de un dueño.', 'codigo': 500},500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
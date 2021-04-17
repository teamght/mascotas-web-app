from flask import Flask, render_template, request, jsonify
from src.util import ENDPOINT_TENSORFLOW_MODEL,DB_URI
from src.application import obtener_mascotas_parecidas, reportar_mascota_desaparecida,eliminar_archivos_temporales
from datetime import datetime
import json
from flask_mongoengine import MongoEngine
from skimage.io import imread
import os
import random

port = int(os.environ.get("PORT", 5000))

app = Flask(__name__)

app.config['MONGODB_HOST'] = DB_URI

db = MongoEngine(app)

class Mascota(db.Document):
    caracteristicas = db.StringField()
    distancia = db.StringField()
    img_ndarray = db.StringField()
    file_name = db.StringField()

    def to_json(self):
        return {'caracteristicas':self.caracteristicas,
                'distancia':self.distancia,
                'img_ndarray':self.img_ndarray,
                'file_name':self.file_name}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Mascotas', ims={})

@app.route('/search', methods=['GET','POST'])
def search_func():
    fecha_busqueda = datetime.now()
    print('Inicio de búsqueda de mascota: {}'.format(fecha_busqueda))
    try:
        if not os.path.exists('./static/'):
            os.mkdir('./static/')
        
        current_date = datetime.utcnow().strftime('%Y-%m-%d_%H%M%S.%f')[:-3]
        nombre_imagen_a_predecir = './static/image_{}.jpg'.format(current_date)
        if request.method == 'POST':
            file = request.files['img']
            file.save(nombre_imagen_a_predecir)
        
        respuesta = obtener_mascotas_parecidas(nombre_imagen_a_predecir)

        
    except Exception as e:
        print('Hubo un error en la búsqueda de mascota: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        return jsonify('Hubo un error. Volver a ingresar la imagen.')
    
    print('Fin de búsqueda de mascota: {}'.format(datetime.now()))
    return jsonify(respuesta)

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
        inputdesc = request.form.get('inputdesc')

        file = request.files['img']
        file.save(nombre_imagen_a_predecir)
        respuesta = reportar_mascota_desaparecida(nombre_imagen_a_predecir)
        #
        # Guardar en base de datos
        #
        #Genero un valor random para la distancia
        dist = str(random.randint(0,999))+' km.'
        img_ndarray = (imread(nombre_imagen_a_predecir) / 255.0).tostring()
        mascota = Mascota(caracteristicas=inputdesc,
                         distancia=dist,
                         img_ndarray=str(img_ndarray),
                         file_name=nombre_imagen_a_predecir)
        mascota.save()
        eliminar_archivos_temporales(nombre_imagen_a_predecir)
        
    except Exception as e:
        print('Hubo un error al reportar mascota desaparecida: {}'.format(datetime.now()))
        print('Hubo un error. {}'.format(e))
        eliminar_archivos_temporales(nombre_imagen_a_predecir)
        return jsonify('Hubo un error. Volver a reportar desaparición.')


    print('Fin de reportar mascota desaparecida: {}'.format(datetime.now()))
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
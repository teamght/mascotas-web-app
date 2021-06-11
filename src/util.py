import os

def mostrar_cadena_vacia(campo):
    if campo is None:
        return ''
    return campo

ENDPOINT_TENSORFLOW_MODEL = os.environ.get('ENDPOINT_TENSORFLOW_MODEL')

ENDPOINT_REPORTAR_MASCOTA = os.environ.get('ENDPOINT_REPORTAR_MASCOTA')

import os

def mostrar_cadena_vacia(campo):
    if campo is None:
        return ''
    return campo

def existe_campo_en_diccionario(diccionario, campo):
    if campo in diccionario:
        return diccionario[campo]
    return ''

def retornar_valor_campo_en_diccionario(diccionario, campo):
    if campo in diccionario:
        return diccionario[campo]
    return None

ENDPOINT_TENSORFLOW_MODEL = os.environ.get('ENDPOINT_TENSORFLOW_MODEL')

ENDPOINT_REPORTAR_MASCOTA = os.environ.get('ENDPOINT_REPORTAR_MASCOTA')

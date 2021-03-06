class MascotaDuenoRequest:
    def __init__(self, identificador, email=None, contacto=None):
        self.identificador = identificador
        self.email = email
        self.contacto = contacto


class MascotaEncontrarRequest:
    def __init__(self, dueno, geolocalizacion_reportado, lista_imagenes_bytes, caracteristicas, fecha_de_perdida, 
        barrio_nombre, genero, nombre, comportamiento, datos_adicionales, estado):
        self.dueno = dueno
        self.geolocalizacion_reportado = geolocalizacion_reportado
        self.lista_imagenes_bytes = lista_imagenes_bytes
        self.caracteristicas = caracteristicas
        self.fecha_de_perdida = fecha_de_perdida
        self.barrio_nombre = barrio_nombre
        self.genero = genero # Hembra (0) / Macho (1)
        self.nombre = nombre
        self.comportamiento = comportamiento
        self.datos_adicionales = datos_adicionales
        self.estado = estado


class MascotaReportartRequest:
    def __init__(self, dueno, geolocalizacion_reportado, lista_imagenes_bytes, caracteristicas, fecha_de_perdida, 
        barrio_nombre, genero, nombre, comportamiento, datos_adicionales, estado):
        self.dueno = dueno
        self.geolocalizacion_reportado = geolocalizacion_reportado
        self.lista_imagenes_bytes = lista_imagenes_bytes
        self.caracteristicas = caracteristicas
        self.fecha_de_perdida = fecha_de_perdida
        self.barrio_nombre = barrio_nombre
        self.genero = genero # Hembra (0) / Macho (1)
        self.nombre = nombre
        self.comportamiento = comportamiento
        self.datos_adicionales = datos_adicionales
        self.estado = estado

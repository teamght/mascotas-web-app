class MascotaReportartRequest:
    def __init__(self, geolocalizacion_reportado, imagen_bytes, caracteristicas, fecha_de_perdida, 
        barrio_nombre, genero, perro_nombre, comportamiento, datos_adicionales):
        self.geolocalizacion_reportado = geolocalizacion_reportado
        self.imagen_bytes = imagen_bytes
        self.caracteristicas = caracteristicas
        self.fecha_de_perdida = fecha_de_perdida
        self.barrio_nombre = barrio_nombre
        self.genero = genero # Hembra (0) / Macho (1)
        self.perro_nombre = perro_nombre
        self.comportamiento = comportamiento
        self.datos_adicionales = datos_adicionales

#coding=utf-8

"""
Módulo de gestión de tatwas
"""

class Tatwa:
    _tatwas = ("akash", "teja") 
    
    def __init__(self, tatwa):
       self.tatwa = tatwa
        
    @property
    def tatwa(self):
        return self._tatwa

    @tatwa.setter
    def tatwa(self, tatwa):
        tatwa = tatwa.lower()
        if tatwa not in _tatwas:
            raise ValueError("Valor incorrecto del tatwa")
        self._tatwa = tatwa
        


class TatwaEntorno:
    def __init__(self, 
    hora_tatwa = {"hora": 0, "min": 0, "actual": True}            # Horas, minutos
    coordenadas = {"lat": 0, "lon": 0}     # Latitud, longitud
    direccion = ""
    hora_salida_sol = {"hora": 0, "min": 0}

    def inicializar():
        """
        Inicializar todos los parámetros del entorno de tatwas tomando la
        posición y fecha actuales.
        """


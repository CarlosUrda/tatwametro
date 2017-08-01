#coding=utf-8

"""
Módulo de gestión de tatwas
"""

import datetime

class Tatwa:
    """
    Clase para definir un tatwa en concreto.
    """
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
    hora_salida_sol = {"hora": 0, "min": 0}
    hora_puesta_sol

    def __init__(self):
        """
        Constructor
        """

    def inicializar():
        """
        Inicializar todos los parámetros del entorno de tatwas tomando la
        posición y fecha actuales.
        """

    @property
    def localizacion(self):
        """
        Getter del atributo localizacion.

        Retorno:
            Devuelve el valor de la cadena dirección (lugar donde 
                realizar los cálculos de tatwas)
        """
        return self._direccion \  
               + "" if _region is None else "({})".format(self._region)


    def fijar_localizacion(self, direccion, region = None):
        """
        Guardar internamente la dirección y región de la localización.
        Además obtiene las coordenadas de la misma y actualiza el atributo
        coordenadas.

        Argumentos:
            direccion: cadena con la descripción de la dirección 
                donde realizar los caĺculos.
            region: código de región donde se encuentra la direccion.
                Es opcional si se desea concretar la dirección.

        Excepciones:
            RuntimeError en caso de no obtener resultado de la API. Contiene
             el tipo de error devuelto por la API.
        """
        coordenadas = obtener_coordenadas(direccion, region)
        self.fijar_coordenadas_no_localizar(coordenadas[0], coordenadas[1])
                                              
        self._direccion = direccion        
        self._region = region


    @property
    def coordenadas(self):
        """
        Getter que obtiene las coordenadas (latitud, longitud) que
        están asignadas internamente.

        Retorno:
            Tupla con el par de valores (latitud, longitud)
        """
        return self._coordenadas["lat"], self._coordenadas["lng"]


    def fijar_coordenadas_localizar(self, latitud, longitud):
        """
        Actualiza internamente las coordenadas del lugar donde calcular
        los tatwas. Además, obtiene la dirección de dichas coordenadas
        guardándola como localización interna.

        Argumentos:
            latitud: latitud de la coordenada a fijar.
            longitud: longitud de la coordenada a fijar.

        Excepciones:
            RuntimeError en caso de no obtener resultado de la API. Contiene
                el tipo de error devuelto por la API.
        """
        direccion = obtener_direccion(latitud, longitud)

        self.fijar_coordenadas_no_localizar(latitud, longitud)

        self._direccion = direccion
        self._region = None


    def fijar_coordenadas_no_localizar(self, latitud, longitud):
        """
        Actualiza internamente las coordenadas del lugar donde calcular
        los tatwas. No obtiene la dirección de dichas coordenadas ni
        actualiza internamente la localización.

        Argumentos:
            latitud: latitud de la coordenada a fijar.
            longitud: longitud de la coordenada a fijar.

        Excepciones:
            RuntimeError en caso de no obtener resultado de la API. Contiene
                el tipo de error devuelto por la API.
        """
        self._horas_eventos_sol = obtener_horas_eventos_sol(latitud, longitud, 
                                                            self._fecha)

        # Sincronización entre las horas del sol, coordenadas y fecha.
        self._sincronizacion = True

        self._coordenadas = {"lat": latitud, "lng": longitud}
        self._direccion = None
        self._region = None


    @property
    def fecha(self):
        """
        Getter que obtiene la fecha fijada para calcular los tatwas. La
        fecha es de tipo datetime.date

        Retorno:
            Valor datetime.date con la fecha fijada.
        """
        #return self._dia.strftime("%d de %B de %Y")
        return self._fecha


    def fijar_fecha(self, dia, mes, anno):
        """
        Modificar internamente la fecha que se usará para calcular los
        tatwas.

        Argumentos:
            dia: día de la fecha.
            mes: número de mes de la fecha.
            anno: año de la fecha.

        Excepciones:
            ValueError o TypeError si los argumentos son incorrectos.
        """
        try:
            self._fecha = dt.date(anno, mes, dia)    
        except ValueError as err:
            print(err)
            raise ValueError("Error al crear tipo datetime.date")
        except TypeError as err:
            print(err)
            raise TypeError("Error al crear tipo datetime.date")

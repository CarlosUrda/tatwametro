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
       self._tatwa = tatwa
        
    @property
    def tatwa(self):
        return self._tatwa

    @tatwa.setter
    def tatwa(self, tatwa):
        tatwa = tatwa.lower()
        if tatwa not in _tatwas:
            raise ValueError("Valor incorrecto del tatwa")
        self._tatwa = tatwa
        


class EntornoTatwas:
    """
    Clase con todos los datos y operaciones necesarias para el cálculo
    de tatwas
    """
    def __init__(self):
        """
        Constructor
        """
        self._coordenadas = None
        self._fecha = None
        self._direccion = None
        self._region = None
        self._hora = None
        self._horas_eventos_sol = None


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


    def fijar_localizacion(self, direccion, region = None, ):
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
        try:
        coordenadas = obtener_coordenadas(direccion, region)
        self.fijar_coordenadas(coordenadas[0], coordenadas[1], False)
                                              
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


    def fijar_coordenadas(self, lat, lng, localizable = True, horas_sol = True):
        """
        Actualiza internamente las coordenadas del lugar donde calcular
        los tatwas. También de manera opcional actualiza la dirección
        de localización y las horas de los eventos del sol a partir de
        las coordenadas mediante API's. 

        Argumentos:
            lat: latitud de la coordenada a fijar.
            lng: longitud de la coordenada a fijar.
            localizable: flag para actualizar la dirección de
                localización a partir de las coordenadas. Si es True
                se usa la API Google Maps para obtener la dirección.
            sol: flag para actualizar las horas de los eventos del sol.
                Si es True se usa la API para obtener las horas de los 
                eventos del sol.

        Excepciones:
            ValueError o TypeError si los valores de las coordenadas
                (latitud, longitud) son incorrectos. No se modifican
                las coordinadas internas.
            RuntimeError en caso de no obtener dirección de localización
                o las horas del sol de la correspondiente API. 
        """
        comprobar_coordenadas(lat, lng)

        self._region = None
        self._direccion = obtener_direccion(lat, lng) if localizable else None

        self._coordenadas = {"lat": lat, "lng": lng}
        self._horas_eventos_sol = None

#        if horas_sol:
#            try:
#                self.actualizar_horas_eventos_sol()
#            except (RuntimeError, ValueError) as err:
#                print(err)
#                raise RuntimeError("Error al actualizar las horas de"
#                                   " los eventos del sol.")
#        else:
#            self._horas_eventos_sol = None


    def actualizar_horas_eventos_sol(self):
        """
        Actualizar las horas de los eventos del sol. Para poder obtener
        las horas es necesario que las coordenadas y la fecha estén
        fijados internamente.

        Excepciones:
            ValueError si la fecha o las coordenadas no han sido fijadas.
            RuntimeError si ocurre algún error al intentar obtener las
               horas de los eventos.
        """
        if fecha is None:
            raise ValueError("No se ha asignado un valor para la fecha")
        elif self._coordenadas is None:
            raise ValueError("No se han fijado las coordenadas")
    
        try:
            self._horas_eventos_sol = 
                obtener_horas_eventos_sol(self._coordenadas["lat"], 
                                          self._coordenadas["lng"], 
                                          self._fecha)
        except RuntimeError as err:
            print(err)
            raise RuntimeError("Error al llamar a la función "
                               "obtener_horas_eventos_sol().")


    def calcular_tatwas(self):
        """
        Calcular los tatwas en la a partir de las horas de los eventos
        del sol y la hora concreta a obtenerlos.

        Excepciones:
            ValueError si la hora para el cálculo de tatwas o las horas
                de eventos del sol no han sido fijadas.
        """
        if self._hora is None:
            raise ValueError("No se ha asignado una hora a calcular.")
        elif self._horas_eventos_sol is None:
            raise ValueError("No se han obtenido las horas de eventos del sol"))
    
        try:
            self._horas_eventos_sol = 
                obtener_horas_eventos_sol(self._coordenadas["lat"], 
                                          self._coordenadas["lng"], 
                                          self._fecha)
        except RuntimeError as err:
            print(err)
            raise RuntimeError("Error al llamar a la función "
                               "obtener_horas_eventos_sol().")


    @property
    def fecha(self):
        """
        Getter que obtiene la fecha fijada en la cual se calcularán los
        tatwas. La fecha es de tipo datetime.date

        Retorno:
            Valor datetime.date con la fecha fijada.
        """
        #return self._dia.strftime("%d de %B de %Y")
        return self._fecha


    def fijar_fecha(self, dia = None, mes = 1, anno = 1900, horas_sol = True):
        """
        Modificar internamente la fecha en la cual se calcularán los
        tatwas.

        Argumentos:
            dia: día de la fecha. Si es None, se toma la fecha actual.
            mes: número de mes de la fecha.
            anno: año de la fecha.
            horas_sol: flag para obtener las horas de los eventos del
                sol. Si es True y la fecha interna está fijada, se usa
                la API para obtener las horas de los eventos del sol.

        Excepciones:
            ValueError o TypeError si los argumentos son incorrectos.
            RuntimeError si ocurre algún error al intentar obtener las
            horas de los eventos del sol.
        """
        if dia is None:
            self._fecha = dt.date.today()
        else:
            try:
                self._fecha = dt.date(anno, mes, dia)    
            except ValueError as err:
                print(err)
                raise ValueError("Error al crear tipo datetime.date")
            except TypeError as err:
                print(err)
                raise TypeError("Error al crear tipo datetime.date")
            
         self._horas_eventos_sol = None

#        if horas_sol:
#            try:
#                self.actualizar_horas_eventos_sol()
#            except (RuntimeError, ValueError) as err:
#                print(err)
#                raise RuntimeError("Error al actualizar las horas de"
#                                   " los eventos del sol.")
#        else:
#            self._horas_eventos_sol = None


    @property
    def hora(self):
        """
        Getter que obtiene la hora en la cual se calcularán los tatwas.
        La hora es de tipo datetime.time

        Retorno:
            Valor datetime.time con la hora establecida.
        """
        return self._hora


    def fijar_hora(self, horas = None, minutos = 0, segundos = 0, 
                   horas_sol = True):
        """
        Modificar internamente la hora en la cual se calcularán los
        tatwas.

        Argumentos:
            horas: valor de las horas de la hora. Si es None se toma
                la hora actual.
            minutos: valor de los minutos de la hora. 
            segundos: valor de los segundos de la hora. Por defecto 0. 
            horas_sol: flag para obtener las horas de los eventos del
                sol. Si es True y la fecha interna está fijada, se usa
                la API para obtener las horas de los eventos del sol.

        Excepciones:
            ValueError o TypeError si los argumentos son incorrectos.
        """
        if horas is None:
            self._hora = dt.datetime.now().time()
        else:
            try:
                self._hora = dt.time(horas, minutos, segundos)    
            except ValueError as err:
                print(err)
                raise ValueError("Error al crear tipo datetime.time.")
            except TypeError as err:
                print(err)
            raise TypeError("Error al crear tipo datetime.time.")

        if horas_sol:
            try:
                self.calcular_tatwas()
            except as err:
                print(err)
                raise RuntimeError("Error al intentar calcular los tatwas")
                

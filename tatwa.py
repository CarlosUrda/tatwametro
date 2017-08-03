#coding=utf-8

"""
Módulo de gestión de tatwas
"""

import datetime as dt


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
    
    _EVENTOS_SOL_ING_ESP = \
        {"sunrise": "salida", "sunset": "puesta", "solar_noon": "mediodia", 
         "civil_twilight_begin": "amanecer_civil",
         "civil_twilight_end": "ocaso_civil",
         "nautical_twilight_begin": "amanecer_nautico",
         "nautical_twilight_end": "ocaso_nautico",
         "astronomical_twilight_begin": "amanecer_astronomico",
         "astronomical_twilight_end": "ocaso_astronomico"}

    EVENTOS_SOL_DESCRIPCION = \
        {"salida": "salida del sol", "puesta": "puesta del sol",
         "mediodia": "sol del mediodía", 
         "amanecer_civil": "inicio del amanecer civil",
         "ocaso_civil": "fin del ocaso civil", 
         "amanecer_nautico": "inicio del amanecer náutico",
         "ocaso_nautico": "fin del ocaso náutico", 
         "amanecer_astronomico": "inicio del amanecer astronómico",
         "ocaso_astronomico": "fin del ocaso astronómico"} 
    

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
        self._tatwas = None


    @property
    def localizacion(self):
        """
        Getter del atributo localizacion.

        Retorno:
            Devuelve la localización en el siguiente formato:
            dirección (región).
        """
        if self._direccion is None
            return None

        region = " ({})".format(self._region) if self._region else ""
        return "{0}{1}".format(self._direccion, region)  


    @property
    def direccion(self):
        """
        Getter del atributo dirección.

        Retorno:
            Valor del atributo dirección.
        """
        return self._direccion


    @property
    def region(self):
        """
        Getter del atributo región.

        Retorno:
            Valor del atributo región.
        """
        return self._region


    def fijar_localizacion(self, direccion, region = None):
        """
        Guardar internamente la dirección y región de la localización.
        Además obtiene las coordenadas de la misma y las fija 
        internamente.

        Argumentos:
            direccion: cadena con la descripción de la dirección 
                donde realizar los caĺculos.
            region: código de región donde se encuentra la direccion.
                Es opcional si se desea concretar la dirección.

        Excepciones:
            RuntimeError en caso de haber error al intentar obtener
            las coordenas.
        """
        try:
            coordenadas = obtener_coordenadas(direccion, region)
        except RuntimeError as err:
            print(err)
            raise RuntimeError("Error al intentar obtener las coordenadas")

        self.fijar_coordenadas(coordenadas[0], coordenadas[1], False)
                                              
        self._direccion = direccion        
        self._region = region


    @property
    def coordenadas(self):
        """
        Getter que obtiene las coordenadas (latitud, longitud) que
        están asignadas internamente.

        Retorno:
            Tupla con el par de valores (latitud, longitud) o None si
            las coordenas no han sido fijadas aún.
        """
        if self._coordenadas is None
            return None
        else:
            return self._coordenadas["lat"], self._coordenadas["lng"]


    def fijar_coordenadas(self, latitud, longitud, localizable = True):
        """
        Actualiza internamente las coordenadas del lugar donde calcular
        los tatwas. También de manera opcional actualiza la dirección
        de localización a partir de las coordenadas. 

        Argumentos:
            latitud: latitud de la coordenada a fijar.
            longitud: longitud de la coordenada a fijar.
            localizable: flag para actualizar la dirección de
                localización a partir de las coordenadas. Si es True
                se usa la API Google Maps para obtener la dirección.

        Excepciones:
            ValueError o TypeError si los valores de las coordenadas
                (latitud, longitud) son incorrectos. No se modifican
                las coordinadas internas.
            RuntimeError en caso de haber error al obtener dirección 
                de localización. 
        """
        comprobar_coordenadas(latitud, longitud)

        if localizable:
            try:
                self._direccion = obtener_direccion(latitud, longitud)
            except RuntimeError as err:
                print(err)
                raise RuntimeError("Error al obtener la dirección a partir "
                                   "de las coordenadas")
        else:
            self._direccion = None

        self._region = None
        self._coordenadas = {"lat": latitud, "lng": longitud}
        self._horas_eventos_sol = None


    def fijar_horas_eventos_sol(self, salida = None, puesta = None, 
                                mediodia = None, amanecer_civil = None, 
                                ocaso_civil = None, amanecer_nautico = None, 
                                ocaso_nautico = None, 
                                amanecer_astronomico = None, 
                                ocaso_astronomico = None):
        """
        Fijar las horas de los eventos del sol manualmente. Los datos
        de coordenadas, localización y fecha se eliminan. Los eventos
        cuyos argumentos reciban valor None no son registrados.

        Argumentos:
            salida: hora de salida del sol. Tipo datetime.time.
            puesta: hora de puesta del sol. Tipo datetime.time.
            mediodia: hora del sol al mediodía. Tipo datetime.time.
            amanecer_civil: hora del amanecer civil (datetime.time).
            ocaso_civil: hora del ocaso civil. Tipo datetime.time.
            amanecer_nautico: hora del amanecer náutico (datetime.time).
            ocaso_nautico: hora del ocaso náutico. Tipo datetime.time.
            amanecer_astronómico: hora ama. astronómico (datetime.time).
            ocaso_astronómico: hora ocaso astronómico (datetime.time).

        Excepciones:
            TypeError si alguno de los argumentos no es de tipo 
                datetime.time.
        """
        self._horas_eventos_sol = dict()

        for evento, hora in locals().items():
            if hora is None or evento == "self":
                continue
            if not isinstance(hora, dt.time):
                self._horas_eventos_sol = None
                raise TypeError("La hora {} no es datetime.time".format(evento)
            
            self._horas_eventos_sol[evento] = hora

        self._fecha = None
        self._coordenadas = None
        self._region = None
        self._direccion = None
        

    def actualizar_horas_eventos_sol(self):
        """
        Actualizar las horas de los eventos del sol a partir de
        coordenadas y fecha. Para poder obtener las horas es necesario 
        que las coordenadas y la fecha estén ya fijados internamente.

        Excepciones:
            ValueError si la fecha o las coordenadas no han sido fijadas.
            RuntimeError si ocurre algún error al intentar obtener las
               horas de los eventos.
        """
        if self._fecha is None:
            raise ValueError("No se ha asignado un valor para la fecha")
        elif self._coordenadas is None:
            raise ValueError("No se han fijado las coordenadas")
    
        try:
            horas_eventos_sol = 
                obtener_horas_eventos_sol(self._coordenadas["lat"], 
                                          self._coordenadas["lng"], 
                                          self._fecha)
        except RuntimeError as err:
            print(err)
            raise RuntimeError("Error al obtener las horas de eventos del sol")

        if len(horas_eventos_sol) == 0:
            raise RuntimeError("La lista obtenida de horas de los eventos del"
                               " sol está vacía.")
              
        self._horas_eventos_sol = \ 
            {_EVENTOS_SOL_ING_ESP[evento_ing]: hora 
             for evento_ing, hora in horas_eventos_sol.items()}


    def calcular_tatwas(self):
        """
        Calcular los tatwas a partir de las horas de los eventos
        del sol y la hora concreta a ser calculados.

        Excepciones:
            ValueError si la hora para el cálculo de tatwas o las horas
                de eventos del sol no han sido fijadas.
        """
        if self._hora is None:
            raise ValueError("No se ha asignado una hora a calcular.")
        elif self._horas_eventos_sol is None:
            raise ValueError("No se han obtenido las horas de eventos del sol"))
    
        # Cálculo.


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


    def fijar_fecha(self, dia = None, mes = 1, anno = 1900):
        """
        Modificar internamente la fecha en la cual se calcularán los
        tatwas.

        Argumentos:
            dia: día de la fecha. Si es None, se toma la fecha actual.
            mes: número de mes de la fecha.
            anno: año de la fecha.

        Excepciones:
            ValueError o TypeError si los argumentos son incorrectos.
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


    @property
    def hora(self):
        """
        Getter que obtiene la hora en la cual se calcularán los tatwas.
        La hora es de tipo datetime.time

        Retorno:
            Valor datetime.time con la hora establecida.
        """
        return self._hora


    def fijar_hora(self, horas = None, minutos = 0, segundos = 0):
        """
        Modificar internamente la hora en la cual se calcularán los
        tatwas.

        Argumentos:
            horas: valor de las horas de la hora. Si es None se toma
                la hora actual.
            minutos: valor de los minutos de la hora. 
            segundos: valor de los segundos de la hora. Por defecto 0. 

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

        self._tatwas = None
                

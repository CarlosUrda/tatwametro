#coding=utf-8

"""
Módulo de gestión de tatwas
"""

import datetime as dt
import util


class Tatwa:
    """
    Clase para definir un tatwa en concreto.
    """
    
    # Constantes de clase
    SEGUNDOS_POR_TATWA = 24 * 60
    NOMBRES_TATWAS = ("akash", "vayu", "tejas", "prithvi", "apas") 
    

    def __init__(self, tatwa):
        """
        Constructor.

        Argumentos:
            tatwa: nombre del tatwa o posición (>= 1) del tatwa en el 
                ciclo de tatwas.

        Excepciones:
            TypeError si el argumento no es str o int.
            ValuError si la posición no es > 0. 

        """
        if isinstance(tatwa, int):
            if tatwa < 1:
                raise ValueError("La posición debe ser > 0")
            self._nombre_tatwa = NOMBRES_TATWAS[(tatwa - 1) 
                                                % len(NOMBRES_TATWAS)]
        else:
            self.nombre_tatwa = nombre_tatwa
        

    @property
    def nombre_tatwa(self):
        """
        Getter del atributo nombre_tatwa
        """
        return self._nombre_tatwa

    @tatwa.setter
    def nombre_tatwa(self, nombre_tatwa):
        """
        Setter del atributo nombre_tatwa
        """
        if not isinstance(nombre_tatwa, str):
            raise TypeError("El nombre del tatwa debe ser un str.")

        nombre_tatwa = nombre_tatwa.lower()
        if nombre_tatwa not in NOMBRES_TATWAS:
            raise ValueError("Valor incorrecto del nombre del tatwa")
        self._nombre_tatwa = nombre_tatwa

    
    def _indice(self):
        """
        Obtener el índice del tatwa en el el ciclo de los tatwas.
        """
        return NOMBRES_TATWAS.index(self._nombre_tatwa)


    @property
    def posicion(self):
        """
        Getter para obtener el número de posición en el ciclo de
        los tatwas.
        """
        return self._indice() + 1


    def __str__(self):
        return self._nombre_tatwa.capitalize()
        

    def distancia(self, tatwa):
        """
        Calcular la distancia relativa entre las posiciones de dos 
        tatwas.

        Argumento:
            tatwa: Tatwa o nombre de tatwa a calcular la diferencia de
                posiciones con el tatwa self.

        Retorno:
            Número de posiciones existentes entre los dos tatwas. 
                Partiendo del tatwa self se cuenta el número de 
                posiciones existentes hasta el tatwa parámetro.

        Excepciones:
            TypeError si el argumento no es un Tatwa o un str.
            ValueError si el argumento es str pero no es un nombre de
                tatwa válido.
        """
        if isinstance(tatwa, Tatwa):
            return tatwa.indice() - self._indice() 
        if isinstance(tatwa, str):
            try:
                indice = NOMBRES_TATWAS.index(tatwa)
            except ValueError:
                raise ValueError("Nombre de argumento tatwa incorrecto.")
            else:
                return indice - self._indice()
        raise TypeError("Tatwa comparado con un tipo de dato incorrecto.")

   
    # Operadores de suma y resta 
     
    def __add__(self, entero):
        """
        Operador suma para obtener el tatwa de una posición concreta
        relativa a partir de este tatwa. 
        
        Argumentos:
            entero: posición relativa del siguente tatwa a obtener.

        Retorno:
            Tatwa con la posición relativa correspondiente al entero
            a partir del tatwa self.
        """
        if not isinstance(entero, int):
            return NotImplemented
        
        indice = (self._indice() + entero) % len(NOMBRES_TATWAS)
        return Tatwa(NOMBRES_TATWAS[indice])

    __radd__ = __add__

    def __sub__(self, entero):
        """
        Operador resta para obtener el tatwa de una posición concreta
        relativa a partir de este tatwa. 
        
        Argumentos:
            entero: posición relativa del siguente tatwa a obtener.

        Retorno:
            Tatwa con la posición relativa correspondiente al entero
            a partir del tatwa self.
        """
        return self + -entero


    # Operadores de comparación

    def __eq__(self, tatwa):
        try:
            return self.distancia(tatwa) == 0
        except TypeError:
            return NotImplemented

    def __gt__(self, tatwa):
        try:
            return self.distancia(tatwa) < 0
        except TypeError:
            return NotImplemented

    def __ge__(self, tatwa):
        try:
            return self.distancia(tatwa) <= 0
        except TypeError:
            return NotImplemented

    def __lt__(self, tatwa):
        try:
            return self.distancia(tatwa) > 0
        except TypeError:
            return NotImplemented

    def __le__(self, tatwa):
        try:
            return self.distancia(tatwa) >= 0
        except TypeError:
            return NotImplemented



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

    _EVENTOS_SOL_PARA_TATWAS = ("salida", "amanecer_civil", 
                                "amanecer_nautico", "amanecer_astronomico")

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
        return "{}{}".format(self._direccion, region)  


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
            coordenadas = util.obtener_coordenadas(direccion, region)
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
        util.comprobar_coordenadas(latitud, longitud)

        if localizable:
            try:
                self._direccion = util.obtener_direccion(latitud, longitud)
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
                util.obtener_horas_eventos_sol(self._coordenadas["lat"], 
                                               self._coordenadas["lng"], 
                                               self._fecha)
        except RuntimeError as err:
            print(err)
            raise RuntimeError("Error al obtener las horas de eventos del sol")
        else:
            if len(horas_eventos_sol) == 0:
                raise RuntimeError("La lista obtenida de horas de los eventos"
                                   " del sol está vacía.")
              
        self._horas_eventos_sol = \ 
            {_EVENTOS_SOL_ING_ESP[evento_ing]: hora 
             for evento_ing, hora in horas_eventos_sol.items()}


    def calcular_tatwas(self):
        """
        Calcular los tatwas a partir de las horas de los eventos
        del sol y la hora concreta a ser calculados.

        Excepciones:
            ValueError si la hora para el cálculo de tatwas o las horas
                de eventos del sol para tatwas no han sido fijadas.
        """
        if self._hora is None:
            raise ValueError("No se ha asignado una hora a calcular.")
        elif self._horas_eventos_sol is None:
            raise ValueError("No se han obtenido las horas de eventos del sol"))
    
        self._tatwas = dict()

        for evento in _EVENTOS_SOL_PARA_TATWAS:
            hora_evento = self._horas_eventos_sol.get(evento)
            if hora_evento is None:
                continue

            segundos = -util.restar_horas_sg(hora_evento, self._hora, 
                                             self._hora >= hora_evento)
            posicion = segundos // Tatwa.SEGUNDOS_POR_TATWA + 1
            self._tatwas[evento] = Tatwa(posicion)

        if len(self._tatwas) == 0:
            self._tatwas = None
            raise ValueError("No hay ninguna hora de eventos para calcular"
                             " tatwas: {}".format(_EVENTOS_SOL_PARA_TATWAS))


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
                

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
    

    def __init__(self, tatwa, ciclo=None):
        """
        Constructor.

        Argumentos:
            tatwa: nombre del tatwa (str) o posición (int >= 1) del 
                tatwa en el ciclo de tatwas.
            ciclo: número (int >= 1) del ciclo al cual está asociado 
                este tatwa. None si no se quiere considerar el número
                de ciclo para este tatwa.
                Si el primer parámetro tatwa es una posición, el 
                ciclo es calculado a partir de la misma, siendo el 
                parámetro ciclo ignorado.

        Excepciones:
            TypeError si los tipos de los argumentos no son permitidos.
            ValueError si el valor de los argumentos no son permitidos.
        """
        try:
            self.cambiar_tatwa_por_posicion(tatwa)
        except TypeError:
            pass
        else:
            return

        try:
            self.nombre = tatwa
        except TypeError:
            raise TypeError("El primer argumento debe ser str o int")
    
        self.ciclo = ciclo
        

    @property
    def nombre(self):
        """
        Getter del atributo nombre
        """
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        """
        Setter del atributo nombre_tatwa

        Argumentos:
            nombre: nombre del tatwa a asignar.

        Excepciones:
            TypeError si el argumento no es de tipo str.
            ValueError si el nombre del tatwa no es uno de los nombres
                válidos.
        """
        if not isinstance(nombre, str):
            raise TypeError("El nombre del tatwa debe ser un str.")

        nombre = nombre.strip().lower()
        if nombre not in self.NOMBRES_TATWAS:
            raise ValueError("Valor incorrecto del nombre del tatwa")

        self._nombre = nombre


    @property
    def ciclo(self):
        """
        Getter del atributo ciclo.
        """
        return self._ciclo

    @ciclo.setter
    def ciclo(self, ciclo):
        """
        Setter del atributo ciclo.

        Argumentos:
            ciclo: número entero int del ciclo a asignar al tatwa.
                None si no se desea considerar ningún número de ciclo
                para este tatwa. 

        Excepciones:
            TypeError si el ciclo no es un entero int o None.
            ValueError si el ciclo int es < 1.
        """
        if isinstance(ciclo, int):
            if ciclo < 1:
                raise ValueError("El valor entero de ciclo debe ser >= 1")
        elif ciclo is not None:
            raise TypeError("El ciclo debe ser un entero o None.")

        self._ciclo = ciclo


    def cambiar_tatwa_por_posicion(self, posicion):
        """
        Cambiar el tatwa por el correspondiente a la nueva posición
        en el ciclo de tatwas (empezando por 1). También modifica
        el número de ciclo en función de la posición indicada.

        Argumentos:
            posicion: posición (>= 1) del tatwa en el ciclo de tatwas.

        Excepciones:
            TypeError si el argumento no es un entero int.
            ValueError si la posición no es > 0. 
        """
        if not isinstance(posicion, int):
            raise TypeError("La nueva posición debe ser un entero int.")

        if posicion < 1:
            raise ValueError("La nueva posición debe ser > 0.")

        numero_de_tatwas = len(self.NOMBRES_TATWAS)
        indice = (posicion - 1) % numero_de_tatwas
        self._ciclo = (posicion - 1) // numero_de_tatwas + 1       
        self._nombre = self.NOMBRES_TATWAS[indice]
     

    @classmethod
    def _indice_de_nombre_tatwa(cls, nombre):
        """
        Obtener el índice en el primer ciclo de tatwas asociado al
        correspondiente nombre de un tatwa (empezando por 0).

        Argumentos:
            nombre: nombre del tatwa en minúsculas.

        Retorno:
            Índice del ciclo correspondiente al nombre del tatwa.

        Excepciones:
            ValueError si el nombre no es de ningún tatwa.
        """
        try:
            return cls.NOMBRES_TATWAS.index(nombre)
        except ValueError:
            raise ValueError("El nombre no corresponde a ningún tatwa")


    def _indice(self):
        """
        Obtener el índice del tatwa en el primer ciclo de los tatwas
        (empezando por 0).
        
        Retorno:
            Entero índice del tatwa (>= 0) en el ciclo de tatwas.
        """
        return self._indice_de_nombre_tatwa(self.nombre)


    @property
    def posicion(self):
        """
        Getter para obtener el número de posición del tatwa en los 
        ciclos de los tatwas. 

        Retorno:
            Número de posición en función del ciclo asignado al 
            tatwa. Si no tiene ciclo, se toma el primero.
        """
        indice_ciclo = 0 if self.ciclo is None else self.ciclo - 1
        return (self._indice() + 1) + indice_ciclo * len(self.NOMBRES_TATWAS)


    def __str__(self):
        return self._nombre.capitalize()
        
    def __repr__(self):
        return "{}, {} ({})".format(self, self.posicion, self.ciclo) 


    def distancia(self, tatwa):
        """
        Calcular la distancia relativa entre las posiciones de dos 
        tatwas.

        Argumento:
            tatwa: Objeto Tatwa, nombre de un tatwa (str) o posición
                de un tatwa en el ciclo (int). En caso de ser un nombre
                se considera su posición en el primer ciclo.

        Retorno:
            Número de posiciones existentes entre los dos tatwas. 
                Partiendo del tatwa self se cuenta el número de 
                posiciones existentes hasta el tatwa asociado al
                parámetro.

        Excepciones:
            TypeError si el argumento no es un Tatwa o un str.
            ValueError si el argumento es str pero no es un nombre de
                tatwa válido.
        """
        if isinstance(tatwa, int):
            if tatwa < 1:
                raise ValueError("La posición debe ser > 0")
            return tatwa - self.posicion
        if isinstance(tatwa, Tatwa):
            return tatwa.posicion - self.posicion
        if isinstance(tatwa, str):
            indice = self._indice_de_nombre_tatwa(tatwa.strip().lower())
            return (indice + 1) - self.posicion
        
        raise TypeError("Tipo de dato del argumento incorrecto.")

   
    # Operadores de suma y resta 
     
    def __add__(self, entero):
        """
        Operador suma para obtener el tatwa de una posición concreta
        relativa a partir de este tatwa. 
        Si el tatwa tiene ciclo, la nueva posición debe ser > 1, ya
        que al tener en cuenta los ciclos no hay tatwas de posición
        menor a 1 (anteriores al primer ciclo).
        Si el tatwa no tiene ciclo, el tatwa resultante tampoco lo 
        tendrá y la nueva posición puede ser < 1, a la cual se le 
        aplicará el operado % para obtener una posición siempre
        entre 1 y número de tatwas.
        
        Argumentos:
            entero: posición relativa del siguente tatwa a obtener.

        Retorno:
            Tatwa con la posición relativa correspondiente al entero
            a partir del tatwa self. Si el tatwa self no tiene ciclo
            el tatwa resultado tampoco tendrá ciclo (None).
        """
        if not isinstance(entero, int):
            return NotImplemented
        
        if self.ciclo is None:
            indice = (self._indice() + entero) % len(self.NOMBRES_TATWAS)
            tatwa_resultado = Tatwa(self.NOMBRES_TATWAS[indice])
        else:
            tatwa_resultado = Tatwa(self.posicion + entero)

        return tatwa_resultado


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
        """
        Operador == para comparar tatwas.

        Argumentos:
            tatwa: puede ser un objeto Tatwa, una posición de un tatwa
                o el nombre de un tatwa. Si es un objeto sin ciclo o
                un nombre, se les consideran del primer ciclo.

        Retorno:
            True/False dependiendo si ambos se refieren al mismo tatwa 
            en el mismo ciclo.
        """
        try:
            return self.distancia(tatwa) == 0
        except TypeError:
            return NotImplemented


    def __gt__(self, tatwa):
        """
        Operador > para comparar tatwas.

        Argumentos:
            tatwa: puede ser un objeto Tatwa, una posición de un tatwa
                o el nombre de un tatwa. Si es un objeto sin ciclo o
                un nombre, se les consideran del primer ciclo.

        Retorno:
            True/False dependiendo si el primer tatwa tiene una 
            posición mayor al segundo.
        """
        try:
            return self.distancia(tatwa) < 0
        except TypeError:
            return NotImplemented


    def __ge__(self, tatwa):
        """
        Operador >= para comparar tatwas.

        Argumentos:
            tatwa: puede ser un objeto Tatwa, una posición de un tatwa
                o el nombre de un tatwa. Si es un objeto sin ciclo o
                un nombre, se les consideran del primer ciclo.

        Retorno:
            True/False dependiendo si el primer tatwa tiene una 
            posición mayor o igual al segundo.
        """
        try:
            return self.distancia(tatwa) <= 0
        except TypeError:
            return NotImplemented


    def __lt__(self, tatwa):
        """
        Operador < para comparar tatwas.

        Argumentos:
            tatwa: puede ser un objeto Tatwa, una posición de un tatwa
                o el nombre de un tatwa. Si es un objeto sin ciclo o
                un nombre, se les consideran del primer ciclo.

        Retorno:
            True/False dependiendo si el primer tatwa tiene una 
            posición menor al segundo.
        """
        try:
            return self.distancia(tatwa) > 0
        except TypeError:
            return NotImplemented


    def __le__(self, tatwa):
        """
        Operador <= para comparar tatwas.

        Argumentos:
            tatwa: puede ser un objeto Tatwa, una posición de un tatwa
                o el nombre de un tatwa. Si es un objeto sin ciclo o
                un nombre, se les consideran del primer ciclo.

        Retorno:
            True/False dependiendo si el primer tatwa tiene una 
            posición menor o igual al segundo.
        """
        try:
            return self.distancia(tatwa) >= 0
        except TypeError:
            return NotImplemented



class EntornoTatwas:
    """
    Clase con todos los datos y operaciones necesarias para el cálculo
    de tatwas
    """
    
    _EVENTOS_SOL_PARA_TATWAS = ("salida", "amanecer_civil", 
                                "amanecer_nautico", "amanecer_astronomico")


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
            dirección (región). None si no se ha fijado aún la
            localización.
        """
        if self._direccion is None:
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


    def fijar_localizacion(self, direccion, region=None, localizable=False):
        """
        Guardar internamente la dirección y región de la localización.
        De manera opcional actualiza las coordenadas de localización 
        a partir de dichas dirección y región.

        Argumentos:
            direccion: cadena con la descripción de la dirección 
                donde realizar los caĺculos.
            region: código de región donde se encuentra la direccion.
                Es opcional si se desea concretar la dirección.
            localizable: flag para indicar si debe actualizar las
                coordenadas a partir de la dirección y región.

        Excepciones:
            RuntimeError en caso de haber error al intentar obtener
            las coordenas.
            ValueError si dirección tiene un valor vacío.
        """
        if not direccion:
            raise ValueError("Valor de dirección vacío")
        if localizable:
            try:
                coordenadas = util.obtener_coordenadas(direccion, region)
            except RuntimeError as err:
                print(err)
                raise RuntimeError("Error al intentar obtener las coordenadas")

            self.fijar_coordenadas(coordenadas[0], coordenadas[1], False)
                                    
        self._direccion = direccion        
        self._region = region
        self._horas_eventos_sol = None


    @property
    def coordenadas(self):
        """
        Getter que obtiene las coordenadas (latitud, longitud) que
        están asignadas internamente.

        Retorno:
            Tupla con el par de valores (latitud, longitud) o None si
            las coordenas no han sido fijadas aún.
        """
        if self._coordenadas is None:
            return None
        else:
            return self._coordenadas["lat"], self._coordenadas["lng"]


    def fijar_coordenadas(self, latitud, longitud, localizable = False):
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
        latitud, longitud = util.convertir_coordenadas(latitud, longitud)

        if localizable:
            try:
                self._direccion = util.obtener_direccion(latitud, longitud)
            except RuntimeError as err:
                print(err)
                raise RuntimeError("Error al obtener la dirección a partir "
                                   "de las coordenadas")

        self._coordenadas = {"lat": latitud, "lng": longitud}
        self._horas_eventos_sol = None


    def fijar_horas_eventos_sol(self, salida = None, puesta = None, 
                                mediodia = None, duracion_dia = None
                                amanecer_civil = None, ocaso_civil = None, 
                                amanecer_nautico = None, ocaso_nautico = None, 
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
            duracion_dia: duración del día. Tipo datetime.timedelta.
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
            if evento == "duracion_dia":
                if not isinstance(hora, dt.timedelta):
                    self._horas_eventos_sol = None
                    raise TypeError("Duración {} no es datetime.timedelta"
                                    .format(evento))
            elif not isinstance(hora, dt.time):
                self._horas_eventos_sol = None
                raise TypeError("Hora {} no es datetime.time".format(evento))
            
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
            horas_eventos_sol = \
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
              
        self._tatwas = None


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
            raise ValueError("No se han obtenido las horas de eventos del sol")
    
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
        Modificar la fecha en la cual se calcularán los tatwas.

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
        self._tatwas = None


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
                

#coding=utf-8

"""
Módulo de gestión de tatwas
"""

import datetime as dt
import util as ut
import pytz as tz


class Tatwa:
    """
    Clase para definir un tatwa en concreto.
    """
    
    # Constantes de clase
    SEGUNDOS_TATWA = 24 * 60 #+ 20
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
            self.posicion = tatwa
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
        if self._posicion is None:
            return self._nombre

        numero_tatwas = len(self.NOMBRES_TATWAS)
        return self.NOMBRES_TATWAS[(self._posicion - 1) % numero_tatwas] 
     

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
        self._posicion = None


    @property
    def ciclo(self):
        """
        Getter del atributo ciclo.
        """
        if self._posicion is None:
            return self._ciclo
        
        return (self._posicion - 1) // len(self.NOMBRES_TATWAS) + 1


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
        if self._posicion is not None:
            raise RuntimeError("Ya has marcado este tatwa con una posición."
                               " Si deseas asignar un ciclo marca antes este" 
                               " tatwa con un nombre.")
        if isinstance(ciclo, int):
            if ciclo < 1:
                raise ValueError("El valor entero de ciclo debe ser >= 1")
        elif ciclo is not None:
            raise TypeError("El ciclo debe ser un entero o None.")

        self._ciclo = ciclo


    @property
    def posicion(self):
        """
        Getter para obtener el número de posición del tatwa en los 
        ciclos de los tatwas. 

        Retorno:
            Si está marcado por la posición, devuelve la posición.
            Si no, devuelve la posición en función del ciclo asignado
            al tatwa. Si no tiene ciclo, se toma el primero.
        """
        if self._posicion is not None:
            return self._posicion

        indice_ciclo = 0 if self.ciclo is None else self.ciclo - 1
        return (self._indice() + 1) + indice_ciclo * len(self.NOMBRES_TATWAS)
    
    
    @posicion.setter    
    def posicion(self, posicion):
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

        self._posicion = posicion
        self._nombre = self._ciclo = None


    @property
    def atributo(self):
        """
        Getter que informa de qué determina el tatwa: nombre o posición.
        """
        return "nombre" if self._posicion is None else "posicion"


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
        if self._posicion is not None:
            return (self._posicion - 1) % len(self.NOMBRES_TATWAS)

        return self._indice_de_nombre_tatwa(self.nombre)


    def __str__(self):
        return self.nombre.capitalize()
        
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
        self._fecha_sol = None
        self._direccion = None
        self._zona_horaria = None
        self._fecha_tw = None
        self._hora_tw = None
        self._fechahora_tw = None
        self._fechahoras_eventos_sol = None
        self._tatwas = None


    def __repr__(self):
        return ("{}: {}\n"*9).format("Coordenadas", self._coordenadas, 
                                     "Fecha sol", self._fecha_sol, 
                                     "Dirección", self._direccion, 
                                     "Zona horaria", self._zona_horaria, 
                                     "Hora tatwa", self._hora_tw,
                                     "Fecha tatwa", self._fecha_tw,
                                     "Fechahora tatwa usada", 
                                     self._fechahora_tw,
                                     "Fechahoras eventos sol", 
                                     self._fechahoras_eventos_sol, 
                                     "Tatwas", self._tatwas)


    @property
    def direccion(self):
        """
        Getter del atributo dirección.

        Retorno:
            Devuelve la dirección fijada. None si no se ha fijado
        """
        return self._direccion


    @property
    def zona_horaria(self):
        """
        Getter del atributo zona_horaria.

        Retorno:
            Devuelve la zona horaria fijada por las coordenadas.
                None si no ha sido fijada.
        """
        return self._zona_horaria.zone


    def fijar_direccion(self, direccion, localizable=False):
        """
        Guardar internamente la dirección de la localización.
        De manera opcional actualiza las coordenadas de localización 
        a partir de dichas dirección y región.

        Argumentos:
            direccion: cadena con la descripción de la dirección 
                donde realizar los caĺculos.
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
                coordenadas = ut.API_google_geocode(direccion)
            except RuntimeError as err:
                print(err)
                raise RuntimeError("Error al intentar obtener las coordenadas")

            self.fijar_coordenadas(coordenadas[0], coordenadas[1], False)
                                    
        self._direccion = direccion        


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
        latitud, longitud = ut.convertir_coordenadas(latitud, longitud)

        try:
            datos = ut.API_timezonedb_get((latitud, longitud))
        except RuntimeError as err:
            print(err)
            raise RuntimeError("Error al obtener dirección y zona horaria.")

        if localizable:
            self._direccion = datos["direccion"]
        
        self._zona_horaria = tz.timezone(datos["zona_horaria"])
        self._coordenadas = {"lat": latitud, "lng": longitud}
        self._fechahoras_eventos_sol = None
        self._tatwas = None
        self._fechahora_tw = None


    def fijar_fechahoras_eventos_sol(self, salida = None, 
                                     amanecer_civil = None, 
                                     amanecer_nautico = None, 
                                     amanecer_astronomico = None):
        """
        Fijar las horas de los eventos del sol manualmente. Los datos
        de coordenadas, localización y fecha se eliminan. Los eventos
        cuyos argumentos reciban valor None no son registrados.

        Argumentos:
            salida: hora de salida del sol. Tipo datetime.datetime.
            amanecer_civil: hora del amanecer civil datetime.datetime.
            amanecer_nautico: hora amanecer náutico datetime.datetime.
            amanecer_astronómico: hora ama astronómico datet.datetime.

        Excepciones:
            ValueError si las coordenadas no han sido fijadas.
            TypeError si alguno de los argumentos no es de tipo 
                datetime.datetime.
        """
        if self._coordenadas is None:
            raise ValueError("No se han fijado las coordenadas")
        
        self._fechahoras_eventos_sol = dict()

        for evento, fechahora in locals().items():
            if fechahora is None or evento == "self":
                continue
            
            if not isinstance(fechahora, dt.datetime):
                self._fechahoras_eventos_sol = None
                raise TypeError("{} no es datetime.datetime".format(evento))
           
            self._fechahoras_eventos_sol[evento] = \
                self._zona_horaria.localize(fechahora.replace(tzinfo=None))

        self._fecha_sol = None
        self._coordenadas = None
        self._fechahora_tw = None
        self._direccion = None
        

    def actualizar_fechahoras_eventos_sol(self):
        """
        Actualizar las horas de los eventos del sol en las
        coordenadas y fecha elegida. Si la fecha elegida es None
        se obtienen las horas de los últimos eventos del sol 
        ocurridos antes de la fecha y hora actuales. 

        Excepciones:
            ValueError si la fecha o las coordenadas no han sido fijadas.
            RuntimeError si ocurre algún error al intentar obtener las
               horas de los eventos.
        """
        if self._coordenadas is None:
            raise ValueError("No se han fijado las coordenadas")

        if self._fecha_sol is None:
            fechahora_actual = ut.obtener_fechahora(self._zona_horaria)
            fecha_sol = fechahora_actual.date()
            fecha_sol_ayer = (fechahora_actual - dt.timedelta(days=1)).date() 
        else:
            fecha_sol = self._fecha_sol

        try:
            fechahoras_eventos_sol = \
                ut.API_sunrise_sunset(self._coordenadas["lat"], 
                                      self._coordenadas["lng"], fecha_sol)
            
            self._fechahoras_eventos_sol = \
                {evento: self._zona_horaria.fromutc(fhora.replace(tzinfo=None)) 
                    for evento, fhora in fechahoras_eventos_sol.items() 
                        if evento in self._EVENTOS_SOL_PARA_TATWAS}

            if self._fecha_sol is None:
                fh_evts_sol_ayer = \
                    ut.API_sunrise_sunset(self._coordenadas["lat"], 
                                          self._coordenadas["lng"], 
                                          fecha_sol_ayer)
    
                for evento, fechahora in self._fechahoras_eventos_sol.items():
                    if fechahora_actual < fechahora:
                        fh_ayer = fh_evts_sol_ayer[evento].replace(tzinfo=None)
                        self._fechahoras_eventos_sol[evento] = \
                            self._zona_horaria.fromutc(fh_ayer) 
                            
        
        except RuntimeError as err:
            print(err) # Log
            raise RuntimeError("Error al obtener las horas de eventos del sol")
              
        self._tatwas = None
        self._fechahora_tw = None


    def calcular_tatwas(self):
        """
        Calcular los tatwas a partir de las horas de los eventos
        del sol y la hora concreta a ser calculados.

        Excepciones:
            ValueError si las horas de eventos del sol para tatwas 
                no han sido fijadas.
        """
        if self._fechahoras_eventos_sol is None:
            raise ValueError("No se han obtenido las horas de eventos del sol")
  
        self._fechahora_tw = ut.combinar_fecha_hora(self._fecha_tw,
                                                    self._hora_tw,
                                                    self._zona_horaria)
        self._tatwas = dict()

        for evento, fechahora_evento in self._fechahoras_eventos_sol.items():
            if self._fechahora_tw < fechahora_evento \
               or (self._fechahora_tw >= 
                   fechahora_evento + dt.timedelta(1, Tatwa.SEGUNDOS_TATWA)):
                self._tatwas[evento] = None
                continue

            segundos_evento_tw = \
                (self._fechahora_tw - fechahora_evento).total_seconds()
            posicion_tatwa = segundos_evento_tw // Tatwa.SEGUNDOS_TATWA + 1
            segundos_restantes = Tatwa.SEGUNDOS_TATWA - \
                                 segundos_evento_tw % Tatwa.SEGUNDOS_TATWA
            segundos_inicio = (posicion_tatwa - 1) * Tatwa.SEGUNDOS_TATWA
            fechahora_inicio = fechahora_evento \
                               + dt.timedelta(seconds=segundos_inicio)
            fechahora_fin = fechahora_inicio \
                            + dt.timedelta(seconds=Tatwa.SEGUNDOS_TATWA)
        
            self._tatwas[evento] = \
                {"tatwa": Tatwa(int(posicion_tatwa)), 
                 "fechahora_fin": fechahora_fin, 
                 "fechahora_inicio": fechahora_inicio,
                 "segundos_restantes": 
                 dt.timedelta(seconds=segundos_restantes)}

        if len(self._tatwas) == 0:
            self._tatwas = None
            self._fechahora_tw = None
            raise ValueError("No hay ninguna hora de los siguientes eventos"
                             " para calcular tatwas: {}"
                             .format(_EVENTOS_SOL_PARA_TATWAS))


    @property
    def fecha_sol(self):
        """
        Getter que obtiene la fecha fijada en la cual se calcularán los
        tatwas. La fecha es de tipo datetime.date

        Retorno:
            Valor datetime.date con la fecha fijada.
        """
        return self._fecha_sol


    @fecha_sol.setter
    def fecha_sol(self, fecha):
        """
        Modificar la fecha en la cual se calcularán los tatwas.

        Argumentos:
            fecha: Objeto datetime.date con la fecha a calcular los
                eventos del sol. None para fecha local actual.

        Excepciones:
            TypeError si los argumentos son incorrectos.
        """
        if fecha is not None and not isinstance(fecha, dt.date):
            raise TypeError("Argumento no es de tipo datetime.date")
            
        self._fecha_sol = fecha
        self._fechahoras_eventos_sol = None
        self._fechahora_tw = None
        self._tatwas = None


    @property
    def hora_tw(self):
        """
        Getter que obtiene la hora local en la cual se calcularán 
        los tatwas.

        Retorno:
            Valor datetime.time con la hora establecida.
        """
        return self._hora_tw


    @hora_tw.setter
    def hora_tw(self, hora):
        """
        Modificar internamente la hora en la cual se calcularán
        los tatwas.

        Argumentos:
            hora: objeto datetime.time con la hora a calcular los 
                tatwas. None para la hora local actual.

        Excepciones:
            TypeError si el argumentos es incorrectos.
        """
        if hora is not None and not isinstance(hora, dt.time):
            raise TypeError("Argumento no es de tipo datetime.time")

        self._hora_tw = hora
        self._tatwas = None
        self._fechahora_tw = None
   
   
             
    @property
    def fecha_tw(self):
        """
        Getter que obtiene la fecha en la cual se calcularán 
        los tatwas.

        Retorno:
            Valor datetime.date con la fecha establecida.
        """
        return self._fecha_tw


    @fecha_tw.setter
    def fecha_tw(self, fecha):
        """
        Modificar internamente la fecha local en la cual se calcularán
        los tatwas.

        Argumentos:
            fecha: objeto datetime.date con la fecha local a
                calcular los tatwas.

        Excepciones:
            TypeError si el argumentos es incorrectos.
        """
        if fecha is not None and not isinstance(fecha, dt.date):
            raise TypeError("Argumento no es de tipo datetime.date")

        self._fecha_tw = fecha
        self._tatwas = None
        self._fechahora_tw = None

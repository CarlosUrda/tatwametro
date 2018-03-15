#coding=utf-8

"""
Módulo con funciones de utilidades sobre fechas.
"""

import datetime as dt
import pytz as tz
import ntplib
import api

NTP_URL = "europe.pool.ntp.org"


def restar_horas(hora1, hora2, es_mismo_dia=True):
    """
    Calcular la diferencia en segundos entre dos horas. Es similar a
    realizar hora1 - hora2. No se tienen en cuenta los microsegundos,
    solo las horas, minutos y segundos.

    Argumentos:
        hora1: primer operando hora. Es de tipo datetime.time.
        hora2: segundo operando hora. Es de tipo datetime.time.
        es_mismo_dia: True si hora2 pertenecen al mismo día que hora1.
            False si hora2 pertenece al día siguiente que hora1.

    Retorno:
        Segundos de diferencia entre las dos horas.

    Excepciones:
        TypeError si alguno de los argumentos no es datetime.time.
    """
    if not isinstance(hora1, dt.time):
        raise TypeError("El primer argumento no es de tipo datetime.time")
    if not isinstance(hora2, dt.time):
        raise TypeError("El segundo argumento no es de tipo datetime.time")

    segundos1 = hora1.hour * 3600 + hora1.minute * 60 + hora1.second 
    segundos2 = hora2.hour * 3600 + hora2.minute * 60 + hora2.second 
    segundos_por_dia = 24 * 3600

    return segundos1 - segundos2 - (0 if es_mismo_dia else segundos_por_dia)



def obtener_actual_timestamp(modo="ntp"):
    """
    Obtener el actual timestamp UTC.

    Argumentos:
        modo: "ntp" si se usa el servidor NTP.
              "api" si se usa la api TimeZoneDB.
              "local" si se usa la máquina local.
    Retorno:
        Número de segundos representando el timestamp UTC actual.

    Excepciones:
        RuntimeError si no se obtiene la hora del servidor ntp.
    """
    if modo == "ntp":
        try:
            return ntplib.NTPClient().request(NTP_URL).tx_time
        except ntplib.NTPException as err:
            print(err) #Log
            raise RuntimeError("Error al acceder al servidor NTP")
    
    if modo == "api":
        try:
            return api.timezonedb_get("UTC")["timestamp"]
        except RuntimeError as err:
            print(err) #Log
            raise RuntimeError("Error al acceder al API TimeZoneDB")
    
    if modo == "local":
        return dt.datetime.utcnow().timestamp()
    
    raise TypeError("Argumento modo {} incorrecto".format(modo))



def obtener_fechahora(zona_horaria, timestamp=None):
    """
    Obtener la fecha y hora de una zona horaria concreta en un
    timestamp determinado (sin usar API, sólo herramientas del
    sistema)

    Argumentos:
        zona_horaria: implementación de datetime.tzinfo 
            (tz.tzfile.DstTzInfo, tz.UTC)) con la zona horaria donde
            obtener la fecha y hora.
        timestamp: valor int representando el número de segundos en 
            UTC desde el 01/01/1970 (tiempo UNIX). Si es None se
            toma el momento presente.

    Retorno:
        Objeto datetime.datetime con fecha y hora local establecida 
        en las coordenadas para un timestamp UTC.
    
    Excepciones:
        ValueError, TypeError si argumentos erróneos.
        RuntimeError si no se obtiene el timestamp actual.
    """
    if timestamp is None:
        timestamp = obtener_actual_timestamp()

    try:
        return dt.datetime.fromtimestamp(timestamp, zona_horaria)
    except ValueError as err:
        raise ValueError("Zona horaria o timestamp inválido: {}".format(err))
    except TypeError as err:
        raise TypeError("Zona horaria o timestamp inválido: {}".format(err))



def combinar_fecha_hora(fecha = None, hora = None, zona_horaria = None):
    """
    Combinar hora (datetime.time) y fecha (datetime.date) en un objeto
    datetime.datetime.

    Argumentos:
        hora: objeto datetime.time. Si None se toma la hora actual.
        fecha: objeto datetime.date. Si None se toma la fecha actual.
        zona_horaria: zona horaria a usar para obtener la fecha y hora
            actuales. Implementación de datetime.tzinfo
            (pytz.tzfile.DstTzInfo o pytz.UTC)

    Retorno:
        Objeto datetime.datetime con la fecha y hora unidas.

    Excepciones:
        TypeError si hora y fecha no son datetime.time y datetime.date
            respectivamente, o zona_horaria no es una implementación
            de datetime.tzinfo (tz.tzfile.DstTzInfo, tz.UTC):
        RuntimeError si no se puede acceder al servidor ntp para
            obtener la hora actual.
    """
    if hora is None or fecha is None:
        try:
            fechahora = obtener_fechahora(zona_horaria)
        except TypeError as err:
            print(err) #Log
            raise TypeError("combinar_fecha_hora: Inválida zona_horaria")

        if hora is None:
            if fecha is None:
                return fechahora
            else:
                hora = fechahora.time()
        else:
            fecha = fechahora.date()
    elif zona_horaria is None:
        try:
            return dt.datetime.combine(fecha, hora)
        except TypeError as err:
            print(err) #Log
            raise TypeError("combinar_fecha_hora: Fecha u hora inválida.")
    elif not isinstance(zona_horaria, tz.tzfile.DstTzInfo) \
         and zona_horaria != tz.UTC:
        raise TypeError("combinar_fecha_hora: zona_horaria inválida.")
    
    try:
        return zona_horaria.localize(dt.datetime.combine(fecha, hora))
    except TypeError as err:
        print(err) #Log
        raise TypeError("combinar_fecha_hora: Fecha u hora inválida")
                

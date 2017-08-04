#/usr/bin/env python3
#!coding=utf-8

"""
Módulo con utilidades generales.
"""

# imports
import requests
import datetime as dt
import claves as clv
from collections import Sequence
from numbers import Number

# API's
SOL_API_URL      = "https://api.sunrise-sunset.org/json"
GEOCODE_API_URL  = "https://maps.googleapis.com/maps/api/geocode/json"
TIMEZONE_API_URL = "https://maps.googleapis.com/maps/api/timezone/json"

# Rango coordenadas API Google MAPS
RANGO_LAT = {"max": 90,  "min": -90}
RANGO_LNG = {"max": 180, "min": -180}


def restar_horas_sg(hora1, hora2, es_mismo_dia = True):
    """
    Calcular la diferencia en segundos entre dos horas. Es similar a
    realizar hora1 - hora2. No se tienen en cuenta los microsegundos,
    solo las horas, minutos y segundos.

    Argumentos:
        hora1: primer operando hora. Es de tipo datetime.time.
        hora2: segundo operando hora. Es de tipo datetime.time.
        es_mismo_dia: True hora2 pertenecen al mismo día que hora1. 
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



def comprobar_coordenadas(latitud, longitud):
    """
    Comprobar si los datos latitud y longitud de unas coordenadas son
    correctos.

    Argumentos:
        latitud: valor de la latitud a comprobar.
        longitud: valor de la longitud a comprobar.

    Excepciones:
        ValueError si los valores de las coordenadas están fuera de 
            rango.
        TypeError si los tipos de datos de las coordenadas son
            incorrectos.
    """
    if not isinstance(latitud, (float, int)):
        raise TypeError("La latitud no es float o int")
    if not isinstance(longitud, (float, int)):
        raise TypeError("La longitud no es float o int")

    if not RANGO_LAT["min"] <= latitud <= RANGO_LAT["max"]:
        raise ValueError("Valor latitud fuera de rango {}".format(RANGO_LAT))
    if not RANGO_LNG["min"] <= longitud <= RANGO_LNG["max"]:
        raise ValueError("Valor longitud fuera de rango {}".format(RANGO_LNG))


def obtener_desfase_horario(latitud, longitud, fecha_hora = None):
    """
    Obtener la diferencia horaria de una ubicación en una fecha 
    concreta teniendo en cuenta el horario de verano.

    Argumentos:
        latitud: latitud donde obtener el desfase (int o float).
        longitud: longitud donde obtener el desfase (int o float).
        fecha: día y hora en el cual obtener el desfase. Tiene que
            ser de tipo datetime.datetime. Si es None se toma la 
            fecha y hora actual.

    Retorno:
        Segundos de desfase (diferencia horaria respecto a UTC +
            diferencia horaria de verano)

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        TypeError si los tipos de argumentos no son correctos.
        ValueError si el rango de las coordenadas no es correcto.
    """
    comprobar_coordenadas(latitud, longitud)
    
    if fecha_hora is None:
        fecha_hora = dt.datetime.today()
    elif not isinstance(fecha_hora, dt.datetime):
        raise TypeError("La fecha no es de tipo datetime.datetime.")

    return _obtener_desfase_horario(latitud, longitud, fecha_hora)



def _obtener_desfase_horario(latitud, longitud, fecha_hora):
    """
    Obtener la diferencia horaria de una ubicación en una fecha 
    concreta teniendo en cuenta el horario de verano (al ser para
    uso interno del módulo no comprueba argumentos).

    Argumentos:
        latitud: latitud donde obtener el desfase.
        longitud: longitud donde obtener el desfase.
        fecha_hora: día y hora en el cual obtener el desfase. Tiene
            que ser de tipo datetime.datetime. 

    Retorno:
        Segundos de desfase (diferencia horaria respecto a UTC +
            diferencia horaria de verano)

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
    """
    timestamp = int(fecha_hora.timestamp())

    parametros_url = {"location":  "{}, {}".format(latitud, longitud),
                      "key": clv.TIMEZONE_API_KEY, "timestamp": timestamp,
                      "language": "es"}

    res = requests.get(TIMEZONE_API_URL, parametros_url).json()
    if res["status"] == "OK":
        return res["dstOffset"] + res["rawOffset"]

    raise RuntimeError("Error API de Google: {}".format(res["status"]))





def obtener_horas_eventos_sol(latitud, longitud, fecha_dt = None):
    """
    Obtener los datos de las horas de la puesta, salida y crepúsculo
    del sol usando la API sunrise-sunset.org.

    Argumentos:
        latitud: latitud donde obtener las horas del sol (int o float) 
        longitud: longitud donde obtener las horas del sol (int o float)
        fecha: día en el cual obtener las horas del sol. Tiene que ser
            tipo datetime.date. Si es None se toma la fecha actual.
    
    Retorno:
        Diccionario con las horas de cada evento del sol en formato 
            datetime.time, excepto  "day_length" que tiene formato 
            datetime.timdelta. 
    
    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        TypeError si los tipos de argumentos no son correctos.
        ValueError si el rango de las coordenadas no es correcto.
    """
    comprobar_coordenadas(latitud, longitud)
    if not isinstance(fecha_dt, dt.date) and fecha_dt is not None:
        raise TypeError("La fecha no es de tipo datetime.date")

    parametros_url = {"lat": latitud, "lng": longitud, "formatted": 0}
    if fecha_dt is not None:
        parametros_url["date"] = fecha_dt.strftime("%Y-%m-%d")

    res = requests.get(SOL_API_URL, parametros_url).json()
    if res["status"] != "OK":
        raise RuntimeError("Error API sunrise-sunset.org: {}"
                           .format(res["status"]))

    horas_eventos_sol = dict()
    for evento, hora_utc in res["results"].items():
        if evento == "day_length":
            horas_eventos_sol["day_length"] = dt.timedelta(seconds=hora_utc)
            continue

        fecha_hora_utc = dt.datetime.strptime(hora_utc, 
                                              "%Y-%m-%dT%H:%M:%S+00:00")
        segundos_desfase = _obtener_desfase_horario(latitud, longitud, 
                                                    fecha_hora_utc)
        segundos_desfase_td = dt.timedelta(seconds=segundos_desfase)
        horas_eventos_sol[evento] = (fecha_hora_utc 
                                     + segundos_desfase_td).time()

    return horas_eventos_sol



def obtener_coordenadas(direccion, region = None):
    """
    Obtener las coordenadas (latitud, longitud) de una dirección
    usando la API Google Maps.
    
    Argumentos:
        direccion: direccion a obtener sus coordenadas.
        region: código de región donde está la dirección solicitada.
            En caso de no pasar nada, no se tendrá en cuenta.

    Retorno:
        Tupla con el par (latitud, longitud)

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
    """
    parametros_url = {"address": direccion, "key": clv.GEOCODE_API_KEY, 
                      "language": "es"}
    if region is not None:
        parametros_url["region"] = region

    res = requests.get(GEOCODE_API_URL, parametros_url).json()
    if res["status"] == "OK":
        return (res["results"][0]["geometry"]["location"]["lat"],
                res["results"][0]["geometry"]["location"]["lng"])

    raise RuntimeError("Error API de Google: {}".format(res["status"]))



def obtener_direccion(latitud, longitud):
    """
    Obtener direccion a partir de unas coordenadas (latitud, longitud)
    usando la API Google Maps.
    
    Argumentos:
        latitud: latitud de la coordenada. Tipo int o float.
        longitud: longitud de la coordenada. Tipo int o float.

    Retorno:
        Cadena con la dirección de la coordenada.

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        ValueError si los valores de las coordenadas están fuera de 
            rango.
        TypeError si los tipos de datos de las coordenadas son
            incorrectos.
    
    Mejoras:
        Tener en cuenta los parámetros result_type y location_type de
            la API.
    """
    comprobar_coordenadas(latitud, longitud)

    latlng = "{}, {}".format(latitud, longitud)
    res = requests.get(GEOCODE_API_URL, 
                       {"latlng": latlng, "key": clv.GEOCODE_API_KEY, 
                        "language": "es"}).json()
    if res["status"] == "OK":
        return res["results"][0]["formatted_address"]

    raise RuntimeError("Error API de Google: {}".format(res["status"]))



def es_secuencia_numeros(objeto):
    """
    Comprobar si un objeto es una secuencia de números.

    Argumentos:
        objeto: objeto a comprobar si es secuencia de números.

    Retorno:
        True o False si el objeto es o no una secuencia de números.
    """
    return isinstance(objeto, Sequence) and \
           all(isinstance(e, Number) for e in objeto)



def es_iterable(objeto):
    """
    Comprobar si un objeto es de tipo iterable

    Argumentos:
        objeto: objeto a comprobar si es iterable.

    Retorno:
        True o False si el objeto es o no iterable.
    """
    return hasattr(objeto, "__getitem__") or hasattr(objeto, "__iter__")



def obtener_dato(mensaje, evaluar=None, comprobar=None, fin=None):
    """
    Leer cadenas desde el teclado hasta que una de ellas cumpla alguna de estas
    condiciones:
    - La cadena sea una de las cadenas de finalización.
    - La cadena, una vez evaluada en caso de evaluarse, pase una comprobación.

    Argumentos:
        mensaje: mensaje mostrar antes de introducir el dato por teclado.
        evaluar: función usada para evaluar la cadena introducida y obtener
            el tipo de dato deseado. Debe lanzar una excepción ValueError si
            la cadena a evaluar no tiene el formato correcto. En caso de None
            la cadena leída por teclado no se evalúa.
        comprobar: función que comprueba si el dato introducido (evaluado en
            caso de evaluarse) es correcto. Si es None, no se realiza ninguna
            comprobación del dato.
            Debe devolver True si el dato correcto o False en caso contrario.
        fin: cadena o tupla de cadenas de finalización que interrumpe lectura
            por teclado. Si es None no se realiza ninguna comprobación de
            finalización de la cadena introducida por teclado.

    Retorno:
        Los posibles valores devueltos son:
        - None si la cadena leída es una cadena de finalización.
        - Dato introducido por teclado ya evaluado y pasada la comprobación.
    """
    while True:
        dato = input(mensaje).strip()
        if fin is not None and \
           (isinstance(fin, tuple) and str.lower(dato) in map(str.lower, fin) \
            or \
            isinstance(fin, str) and str.lower(dato) == str.lower(fin)):
            return None

        if evaluar is not None:
            try:
                dato = evaluar(dato)
            except ValueError:
                print("ERROR: valor dato erróneo al evaluar cadena introducida")
                continue
            except SyntaxError:
                print("ERROR: sintaxis errónea al evaluar cadena introducida.")
                continue

        if comprobar is None or comprobar(dato):
            return dato

        print("ERROR: el dato está en formato incorrecto.")


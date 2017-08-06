#/usr/bin/env python3
#!coding=utf-8

"""
Módulo con utilidades generales.
"""

# imports
import requests
import datetime as dt
import ntplib
import pytz
import claves as key
from collections import Sequence
from numbers import Number

# API's
SOL_API_URL        = "https://api.sunrise-sunset.org/json"
GC_GOOGLE_API_URL  = "https://maps.googleapis.com/maps/api/geocode/json"
TZ_GOOGLE_API_URL  = "https://maps.googleapis.com/maps/api/timezone/json"
TIMEZONEDB_API_URL = "http://api.timezonedb.com/v2/get-time-zone"
NTP_API_URL        = "europe.pool.ntp.org"

# Eventos del sol
EVENTOS_SOL_ING_ESP = {"sunrise": "salida", "sunset": "puesta", 
                       "solar_noon": "mediodia", "day_length": "duracion_dia", 
                       "civil_twilight_begin": "amanecer_civil",
                       "civil_twilight_end": "ocaso_civil",
                       "nautical_twilight_begin": "amanecer_nautico",
                       "nautical_twilight_end": "ocaso_nautico",
                       "astronomical_twilight_begin": "amanecer_astronomico",
                       "astronomical_twilight_end": "ocaso_astronomico"}

EVENTOS_SOL_DESCRIPCION = \
    {"salida": "salida del sol", "puesta": "puesta del sol",
     "mediodia": "sol del mediodía", "duracion_dia": "duración del día", 
     "amanecer_civil": "inicio del amanecer civil",
     "ocaso_civil": "fin del ocaso civil", 
     "amanecer_nautico": "inicio del amanecer náutico",
     "ocaso_nautico": "fin del ocaso náutico", 
     "amanecer_astronomico": "inicio del amanecer astronómico",
     "ocaso_astronomico": "fin del ocaso astronómico"} 

# Rango coordenadas API Google MAPS
RANGO_LAT = {"max": 90,  "min": -90}
RANGO_LNG = {"max": 180, "min": -180}


def restar_horas_sg(hora1, hora2, es_mismo_dia=True):
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



def convertir_coordenadas(latitud, longitud):
    """
    Convertir los datos latitud y longitud a formato float, comprobando
    además si los valores están dentro del rango.

    Argumentos:
        latitud: valor de la latitud a comprobar.
        longitud: valor de la longitud a comprobar.

    Excepciones:
        ValueError si los valores de las coordenadas están fuera de 
            rango.
        TypeError si los tipos de datos de las coordenadas son
            incorrectos.

    Retorno:
        Coordenadas (latitud, longitud) convertidas a float.
    """
    try:
        latitud = float(latitud)
        longitud = float(longitud)
    except (ValueError, TypeError):
        raise TypeError("Las coordenadas no están en formato numérico.")

    if not RANGO_LAT["min"] <= latitud <= RANGO_LAT["max"]:
        raise ValueError("Valor latitud fuera de rango {}".format(RANGO_LAT))
    if not RANGO_LNG["min"] <= longitud <= RANGO_LNG["max"]:
        raise ValueError("Valor longitud fuera de rango {}".format(RANGO_LNG))

    return latitud, longitud



def obtener_actual_timestamp():
    """
    Obtener el actual timestamp UTC.

    Retorno:
        Número de segundos representando el timestamp UTC actual.
    """
    return ntplib.NTPClient().request(NTP_API_URL).tx_time



def obtener_fechahora(zona_horaria, timestamp=None):
    """
    Obtener la fecha y hora de una zona horaria concreta en un
    timestamp determinado (sin usar API, sólo herramientas del
    sistema)

    Argumentos:
        latitud: latitud donde obtener la fecha y hora.
        longitud: longitud donde obtener la fecha y hora.
        timestamp: valor int representando el número de segundos en 
            UTC desde el 01/01/1970 (tiempo UNIX). Si es None se
            toma el momento presente.

    Retorno:
        Objeto datetime.datetime con fecha y hora establecida en las 
        coordenadas para un timestamp UTC.
    """
    if timestamp is None:
        timestamp = obtener_actual_timestamp()

    return dt.datetime.fromtimestamp(timestamp, pytz.timezone(zona_horaria))



def obtener_fechahora_API(latitud, longitud, timestamp=None, api="timezonedb"):
    """
    Obtener la fecha, hora y zona horaria de una localización concreta
    en un timestamp determinado usando una API.

    Argumentos:
        latitud: latitud donde obtener los datos.
        longitud: longitud donde obtener los datos.
        timestamp: valor int representando el número de segundos en 
            UTC desde el 01/01/1970 (tiempo UNIX). Si es None se
            toma el momento presente.
        api: API a usar para obtener los datos. API's disponibles:
            "timezonedb": http://api.timezonedb.com/v2/get-time-zone
            "google": https://maps.googleapis.com/maps/api/timezone/

    Retorno:
        Diccionario con el siguiente formato:
            {"fechahora": Objeto datetime.datetime con fecha y hora 
                establecida en las coordenadas para un timestamp UTC,
             "zona_horaria": Nombre de la zona horaria.}

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        ValueError si el argumento api tiene un valor no válido.
    """
    if api == "google":
        if timestamp is None:
            timestamp = obtener_actual_timestamp()
        
        parametros_url = {"location":  "{}, {}".format(latitud, longitud),
                          "key": key.TZ_GOOGLE_API_KEY, "timestamp": timestamp,
                          "language": "es"}

        res = requests.get(TZ_GOOGLE_API_URL, parametros_url).json()
        if res["status"] != "OK":
            raise RuntimeError("Error API Google: {}".format(res["status"]))
        
        timestamp += res["dstOffset"] + res["rawOffset"]
        zona_horaria = res["timeZoneId"]

    elif api == "timezonedb":
        parametros_url = {"lat": latitud, "lng": longitud, "format": "json", 
                          "by": "position", "key": key.TIMEZONEDB_API_KEY, 
                          "fields": "timestamp,zoneName"}
        if timestamp is not None:
            parametros_url["time"] = timestamp

        res = requests.get(TIMEZONEDB_API_URL, parametros_url).json()
        if res["status"] != "OK":
            raise RuntimeError("Err API TimeZoneDB: {}".format(res["message"]))
        
        timestamp = res["timestamp"]
        zona_horaria = res["zoneName"].replace("\\", "")

    else:
        raise ValueError("Valor de tipo de API incorrecto")

    return {"fechahora": dt.datetime.utcfromtimestamp(timestamp),
            "zona_horaria": zona_horaria}



def obtener_horas_eventos_sol(latitud, longitud, fecha=None):
    """
    Obtener los datos de las horas de la puesta, salida y crepúsculo
    del sol usando la API sunrise-sunset.org.

    Argumentos:
        latitud: latitud donde obtener las horas del sol.
        longitud: longitud donde obtener las horas del sol.
        fecha: día en el cual obtener las horas del sol. Tiene que ser
            tipo datetime.date. Por defecto se toma la fecha actual de
            la localización solicitada.
    
    Retorno:
        Diccionario con las horas de cada evento del sol en formato 
            datetime.time, excepto "duracion_dia" que tiene formato 
            datetime.timdelta. 
    
    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        TypeError si los tipos de argumentos no son correctos.
        ValueError si el rango de las coordenadas no es correcto.

    Arreglar fijar_fecha de tatwa.py
    """
    datos_horario = obtener_fechahora_API(latitud, longitud)
    zona_horaria = datos_horario["zona_horaria"]
    if fecha is None:
        fecha = datos_horario["fechahora"].date()
    elif not isinstance(fecha, dt.date):
        raise TypeError("La fecha no es de tipo datetime.date o None.")

    parametros_url = {"lat": latitud, "lng": longitud, "formatted": 0}
    parametros_url["date"] = fecha.strftime("%Y-%m-%d")

    res = requests.get(SOL_API_URL, parametros_url).json()
    if res["status"] != "OK":
        raise RuntimeError("Error API sunrise-sunset {}".format(res["status"]))

    horas_eventos_sol = dict()
    for evento, valor in res["results"].items():
        evento = EVENTOS_SOL_ING_ESP[evento]
        
        if evento == "duracion_dia":
            horas_eventos_sol["duracion_dia"] = dt.timedelta(seconds=valor)
            continue
        
        fechahora_utc = dt.datetime.strptime(valor, "%Y-%m-%dT%H:%M:%S+00:00")
        timestamp = fechahora_utc.replace(tzinfo=dt.timezone.utc).timestamp()
        horas_eventos_sol[evento] = obtener_fechahora(zona_horaria, 
                                                      int(timestamp)).time()

    return horas_eventos_sol



def obtener_coordenadas_API(direccion, region=None):
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
    parametros_url = {"address": direccion, "key": key.GC_GOOGLE_API_KEY, 
                      "language": "es"}
    if region is not None:
        parametros_url["region"] = region

    res = requests.get(GC_GOOGLE_API_URL, parametros_url).json()
    if res["status"] == "OK":
        return (res["results"][0]["geometry"]["location"]["lat"],
                res["results"][0]["geometry"]["location"]["lng"])

    raise RuntimeError("Error API de Google: {}".format(res["status"]))



def obtener_direccion_API(latitud, longitud, api="timezonedb"):
    """
    Obtener direccion a partir de unas coordenadas (latitud, longitud)
    usando una API disponible.
    
    Argumentos:
        latitud: latitud de la coordenada.
        longitud: longitud de la coordenada.
        api: API a usar para obtener la dirección. API's disponibles:
            "timezonedb": http://api.timezonedb.com/v2/get-time-zone
            "google": https://maps.googleapis.com/maps/api/geocode/

    Retorno:
        API Google: Dirección exacta de las coordenadas.
        API TimeZoneDB: Ciudad y país de las coordenadas manera 
            aproximada.

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        ValueError si el valor de api es incorrecto.
    
    Mejoras:
        Tener en cuenta los parámetros result_type y location_type de
            la API de Google.
    """
    if api == "google":
        latlng = "{}, {}".format(latitud, longitud)
        res = requests.get(GC_GOOGLE_API_URL, 
                       {"latlng": latlng, "key": key.GC_GOOGLE_API_KEY, 
                        "language": "es"}).json()
        if res["status"] != "OK":
            raise RuntimeError("Error API de Google: {}".format(res["status"]))

        direccion = res["results"][0]["formatted_address"]
    
    elif api == "timezonedb":
        parametros_url = {"lat": latitud, "lng": longitud, "format": "json", 
                          "by": "position", "key": key.TIMEZONEDB_API_KEY, 
                          "fields": "zoneName,countryName,countryCode"}

        res = requests.get(TIMEZONEDB_API_URL, parametros_url).json()
        if res["status"] != "OK":
            raise RuntimeError("Err API TimeZoneDB: {}".format(res["message"]))
        
        direccion = "{}, {}({})".format(res["zoneName"].split("/")[1],
                                        res["countryName"], res["countryCode"])

    else
        raise ValueError("Valor de tipo de API incorrecto")

    return direccion



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


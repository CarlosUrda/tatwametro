#/usr/bin/env python3
#!coding=utf-8

"""
Módulo con utilidades generales.
"""

# imports
import requests
import datetime as dt
import ntplib
import pytz as tz
import claves as key
from collections import Sequence
from numbers import Number
from ast import literal_eval

# API's
SOL_API_URL            = "https://api.sunrise-sunset.org/json"
GC_GOOGLE_API_URL      = "https://maps.googleapis.com/maps/api/geocode/json"
TZ_GOOGLE_API_URL      = "https://maps.googleapis.com/maps/api/timezone/json"
GET_TIMEZONEDB_API_URL = "http://api.timezonedb.com/v2/get-time-zone"
NTP_API_URL            = "europe.pool.ntp.org"

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

# Rango coordenadas válido (basado en API Google MAPS)
RANGO_LAT = {"max": 90,  "min": -90}
RANGO_LNG = {"max": 180, "min": -180}


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



def evaluar_coordenadas(entrada):
    """
    Evaluar una cadena de entrada para convertirla en una tupla de
    dos elementos float: (latitud, longitud)

    Argumentos:
        entrada: cadena a evaluar.

    Retorno:
        Tupla (latitud, longitud) donde cada coordenada es float.

    Excepciones:
        ValueError si la cadena introducida no está en un formato 
            correcto (latitud, longitud).
    """
    try:
        return convertir_coordenadas(*literal_eval(entrada))
    except (ValueError, SyntaxError, TypeError) as err:
        #print(err) Log
        raise ValueError("Introduce solo dos valores (latitud, longitud)"
                         " separadas por coma.")



def evaluar_fechahora(entrada, formato="%H:%M:%S %d-%m-%Y"):
    """
    Evaluar una cadena de entrada para convertirla en un objeto de
    tipo datetime.datetime usando un formato determinado.

    Argumentos:
        entrada: cadena a evaluar.
        formato: formato usado para evaluar la cadena.

    Retorno:
        Objeto datetime.datetime a partir de la cadena de entrada.

    Excepciones:
        ValueError si la cadena de entrada no está en el formato
            especificado por argumento.
    """
    try:
        return dt.datetime.strptime(entrada, formato)
    except (ValueError, TypeError) as err:
        #print(err) Log
        raise ValueError("Introduce fecha/hora en formato {}".format(formato))
        


def obtener_actual_timestamp():
    """
    Obtener el actual timestamp UTC.

    Retorno:
        Número de segundos representando el timestamp UTC actual.

    Excepciones:
        RuntimeError si no se obtiene la hora del servidor ntp.
    """
    try:
        return ntplib.NTPClient().request(NTP_API_URL).tx_time
    except ntplib.NTPException as err:
        raise RuntimeError(err)



def obtener_fechahora(zona_horaria, timestamp=None):
    """
    Obtener la fecha y hora de una zona horaria concreta en un
    timestamp determinado (sin usar API, sólo herramientas del
    sistema)

    Argumentos:
        zona_horaria: objeto pytz.timezone con la zona horaria deonde
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
            actuales. Objeto pytz.timezone

    Retorno:
        Objeto datetime.datetime con la fecha y hora unidas.

    Excepciones:
        ValueError si zona_horaria tiene un valor no válido.
        TypeError si hora y fecha no son datetime.time y datetime.date
            respectivamente.
    """
    if hora is None and fecha is None:
        return obtener_fechahora(zona_horaria)
    
    if hora is None:
        hora = obtener_fechahora(zona_horaria).time()
    elif not isinstance(hora, dt.time):
        raise TypeError("Argumento hora no es datetime.time.")
    
    if fecha is None:
        fecha = obtener_fechahora(zona_horaria).date()
    elif not isinstance(fecha, dt.date):
        raise TypeError("Argumento fecha no es datetime.date.")

    return zona_horaria.localize(dt.datetime.combine(fecha, hora))



def API_timezonedb_get(localizacion, timestamp=None):
    """
    Uso de API TimeZoneDB (http://api.timezonedb.com/v2/get-time-zone)
    con la funcionalidad get-time-zone.
            
    Argumentos:
        localizacion: coordenadas (lista [latitud, longitud]) o zona 
            horaria (str) en la cual obtener la información.
        timestamp: valor int representando el número de segundos en 
            UTC desde el 01/01/1970 (tiempo UNIX) que representa el
            momento temporal a obtener los datos. Si es None se
            toma el momento presente.

    Retorno:
        Diccionario con el siguiente formato:
            {"fechahora": datetime.datetime con fecha y hora local
                establecida en las coordenadas para el timestamp UTC,
             "zona_horaria": Nombre de la zona horaria,
             "horario_verano": True/False si es horario verano,
             "segundos_desfase": segundos de desfase con UTC,
             "timestamp": segundos UNIX de la fechahora local,
             "nombre_pais": nombre del pais de la localización,
             "codigo_pais": código del país de la localización}

    Excepciones:
        TypeError si la localización está en un formato incorrecto.
        RuntimeError si el resultado de la petición get a la API
            produce algún error.
    """
    parametros_url = {"format": "json", "key": key.TIMEZONEDB_API_KEY, 
                      "fields": "timestamp,zoneName,countryCode,countryName"
                                ",gmtOffset,dst"}
    
    if isinstance(localizacion, str):
        parametros_url["by"] = "zone" 
        parametros_url["zone"] = localizacion
    else:
        parametros_url["by"] = "position"
        try:
            parametros_url["lat"] = localizacion[0]
            parametros_url["lng"] = localizacion[1]
        except (TypeError, IndexError):
            raise TypeError("Formato de localización incorrecto. Debe"
                            " pasarse una lista de dos coordenadas")

    if timestamp is not None:
        parametros_url["time"] = timestamp

    res = requests.get(GET_TIMEZONEDB_API_URL, parametros_url).json()
    if res["status"] != "OK":
        raise RuntimeError("Error API TimeZoneDB: {}".format(res["message"]))
       
    datos = {"timestamp": res["timestamp"], 
             "zona_horaria": res["zoneName"].replace("\\", ""),
             "horario_verano": bool(res["dst"]),
             "segundos_desfase": res["gmtOffset"],
             "nombre_pais": res["countryName"],
             "codigo_pais": res["countryCode"]}

    datos["direccion"] = \
        "{}, {}({})".format(datos["zona_horaria"].split("/")[1],
                            datos["nombre_pais"], datos["codigo_pais"])

    tzone = tz.timezone(datos["zona_horaria"])
    fechahora = dt.datetime.utcfromtimestamp(datos["timestamp"])
    datos["fechahora"] = tzone.localize(fechahora)
    
    return datos
 


def API_google_timezone(latitud, longitud, timestamp=None):
    """
    Uso de API Google Maps Timezone 
    https://maps.googleapis.com/maps/api/timezone/

    Argumentos:
        latitud: latitud donde obtener los datos.
        longitud: longitud donde obtener los datos.
        timestamp: valor int representando el número de segundos en 
            UTC desde el 01/01/1970 (tiempo UNIX) que representa el
            momento temporal a obtener los datos. Si es None se
            toma el momento presente.

    Retorno:
        Diccionario con el siguiente formato:
            {"fechahora": datetime.datetime con fecha y hora local
                establecida en las coordenadas para el timestamp UTC,
             "zona_horaria": Nombre de la zona horaria,
             "zona_horaria_desc": Descripción zona horaria,
             "segundos_desfase": segundos de desfase con UTC,
             "horario_verano": True/False si es horario verano,
             "timestamp": segundos UNIX de la fechahora local}

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
    """
    if timestamp is None:
        timestamp = obtener_actual_timestamp()
        
    parametros_url = {"location":  "{}, {}".format(latitud, longitud),
                      "key": key.TZ_GOOGLE_API_KEY, "timestamp": timestamp,
                      "language": "es"}

    res = requests.get(TZ_GOOGLE_API_URL, parametros_url).json()
    if res["status"] != "OK":
        mensg = "API Google {}: {}".format(res["status"], res["errorMessage"])
        raise RuntimeError(mensg)
    
    datos = \
        {"segundos_desfase": res["dstOffset"] + res["rawOffset"],
         "horario_verano": res["dstOffset"] > 0,
         "zona_horaria": res["timeZoneId"], 
         "zona_horaria_desc": res["timeZoneName"]}
    
    datos["timestamp"] = timestamp + datos["segundos_desfase"]
    
    tzone = tz.timezone(datos["zona_horaria"])
    fechahora = dt.datetime.utcfromtimestamp(datos["timestamp"])
    datos["fechahora"] = tzone.localize(fechahora)
    
    return datos



def API_google_geocode(localizacion):
    """
    Uso de API Google Maps Geocode 
    https://maps.googleapis.com/maps/api/geocode/
    
    Argumentos:
        localizacion: puede ser alguno de estos valores:
            lista [latitud, longitud] => obtener una dirección.
            dirección str => obtener unas coordenadas.

    Retorno:
        Dirección si se pasa coordenadas.
        Coordenadas (latitud, longitud) si se pasa una dirección.

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
    
    Mejoras:
        Tener en cuenta los parámetros result_type y location_type de
            la API de Google.
    """
    parametros_url = {"key": key.GC_GOOGLE_API_KEY, "language": "es"}
    
    if isinstance(localizacion, str):
        es_inversa = False
        parametros_url["address"] = localizacion
    else:
        es_inversa = True
        try:
            parametros_url["latlng"] = \
                "{},{}".format(localizacion[0], localizacion[1])
        except (TypeError, IndexError):
            raise TypeError("Formato de localización incorrecto.")
    
    res = requests.get(GC_GOOGLE_API_URL, parametros_url).json()
    if res["status"] != "OK":
        raise RuntimeError("Error API de Google: {}".format(res["status"]))

    if es_inversa:
        return res["results"][0]["formatted_address"]
    else:
        return (res["results"][0]["geometry"]["location"]["lat"],
                res["results"][0]["geometry"]["location"]["lng"])



def API_sunrise_sunset(latitud, longitud, fecha=None):
    """
    Obtener los datos de las horas de la puesta, salida y crepúsculo
    del sol usando la API sunrise-sunset.org.

    Argumentos:
        latitud: latitud donde obtener las horas del sol.
        longitud: longitud donde obtener las horas del sol.
        fecha: fecha en el cual obtener las horas del sol. Tiene que
            ser tipo datetime.date. Por defecto se toma la fecha actual
            local de la localización solicitada.
    
    Retorno:
        Diccionario con las hora y fecha UTC de cada evento del sol 
            en formato datetime.datetime, excepto "duracion_dia" que 
            tiene formato datetime.timdelta. 
    
    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        TypeError si los tipos de argumentos no son correctos.
    """
    if fecha is None:
        datos_api = API_timezonedb_get((latitud, longitud))
        fecha = datos_api["fechahora"].date()
    elif not isinstance(fecha, dt.date):
        raise TypeError("La fecha no es de tipo datetime.date o None.")

    parametros_url = {"lat": latitud, "lng": longitud, "formatted": 0}
    parametros_url["date"] = fecha.strftime("%Y-%m-%d")

    res = requests.get(SOL_API_URL, parametros_url).json()
    if res["status"] != "OK":
        raise RuntimeError("Error API sunrise-sunset {}".format(res["status"]))

    fechahoras_eventos_sol = dict()
    for evento, dato in res["results"].items():
        evento = EVENTOS_SOL_ING_ESP[evento]
        
        if evento == "duracion_dia":
            fechahoras_eventos_sol["duracion_dia"] = dt.timedelta(seconds=dato)
            continue
      
        fechahora = dt.datetime.strptime(dato, "%Y-%m-%dT%H:%M:%S+00:00")  
        fechahoras_eventos_sol[evento] = tz.UTC.localize(fechahora)

    return fechahoras_eventos_sol



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
    Leer cadenas desde el teclado hasta que una de ellas cumpla alguna
    de estas condiciones:
    - La cadena sea una de las cadenas de finalización.
    - La cadena, una vez evaluada en caso de evaluarse, pase una 
        comprobación.

    Argumentos:
        mensaje: mensaje mostrado antes de introducir el dato por 
            teclado.
        evaluar: función usada para evaluar la cadena introducida y 
            obtener el tipo de dato deseado. Debe lanzar ValueError 
            si la cadena introducida no puede ser evaluada. En caso de 
            ser None, la cadena leída por teclado no se evalúa.
        comprobar: función que comprueba si el dato introducido (ya 
            evaluado en caso de evaluarse) es correcto. Si es None, 
            no se realiza ninguna comprobación del dato. Debe lanzar
            ValueError si el dato no pasa la comprobación.
        fin: cadena o lista de cadenas de finalización que interrumpe 
            lectura por teclado. Si es None no se realiza ninguna 
            comprobación de finalización de la cadena introducida por
            teclado. Si se desea la cadena vacía como condición de
            finalización indicar "".

    Retorno:
        Los posibles valores devueltos son:
        - None si la cadena leída es una cadena de finalización.
        - Dato introducido por teclado ya evaluado y pasada la 
            comprobación.

    Excepciones:
        TypeError si evaluar o comprobar no son funciones, o 
            fin no es str o tupla de str.
    """
    if isinstance(fin, str):
        fin_lista = [fin.lower()]
    elif fin is None:
        fin_lista = []
    else:
        try:
            fin_lista = [x.lower() for x in fin]
        except (TypeError, AttributeError):
            raise TypeError("La condición de finalización debe ser un str o"
                           " una lista de str.")
    
    while True:
        dato = input(mensaje).strip()

        if dato.lower() in fin_lista:
            return None

        if evaluar is not None:
            try:
                dato = evaluar(dato)
            except (ValueError, SyntaxError) as err:
                print("Error al evaluar el dato introducido: {}".format(err))
                continue

        if comprobar is not None: 
            try:
                comprobar(dato)
            except ValueError as err:
                print("Error al comprobar el dato introducido: {}".format(err))
                continue

        return dato

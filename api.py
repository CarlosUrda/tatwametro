#coding=utf-8

"""
Módulo con funciones de acceso a diferentes API's
"""

import requests
import datetime as dt
import pytz as tz
import claves as key
import fechahora as fh


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


# URL de las API
SOL_API_URL            = "https://api.sunrise-sunset.org/json"
GC_GOOGLE_API_URL      = "https://maps.googleapis.com/maps/api/geocode/json"
TZ_GOOGLE_API_URL      = "https://maps.googleapis.com/maps/api/timezone/json"
GET_TIMEZONEDB_API_URL = "http://api.timezonedb.com/v2/get-time-zone"
GC_MAPQUEST_API_URL    = "http://www.mapquestapi.com/geocoding/v1/address"
GCI_MAPQUEST_API_URL   = "http://www.mapquestapi.com/geocoding/v1/reverse"


def timezonedb_get(localizacion, timestamp=None):
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
 


def google_timezone(latitud, longitud, timestamp=None):
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
        timestamp = fh.obtener_actual_timestamp()
        
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



def google_geocode(localizacion):
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
        TypeError si la localización está en un formato incorrecto.
    
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
        
        if len(localizacion) != 2:
            raise TypeError("Debes introducir solo dos coordenadas.")
    
    res = requests.get(GC_GOOGLE_API_URL, parametros_url).json()
    if res["status"] != "OK":
        raise RuntimeError("Error API de Google: {}".format(res["status"]))

    if es_inversa:
        return res["results"][0]["formatted_address"]
    else:
        return (res["results"][0]["geometry"]["location"]["lat"],
                res["results"][0]["geometry"]["location"]["lng"])



def mapquest_geocoding(localizacion):
    """
    Uso de API Mapquest Geocode 
    http://www.mapquestapi.com/geocoding/v1/reverse
    http://www.mapquestapi.com/geocoding/v1/address

    Argumentos:
        localizacion: puede ser alguno de estos valores:
            lista [latitud, longitud] => obtener una dirección.
            dirección str => obtener unas coordenadas.

    Retorno:
        Diccionario con los siguientes campos:
        "direccion": str con la dirección encontrada.
        "coordenadas": tupla (latitud, longitud) de coordenadas.
        "mapa_url": dirección del mapa de la localización.
        "copyright": información del copyright.

    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        TypeError si la localizaión está en un formato incorrecto.
    """
    parametros_url = {"key": key.MAPQUEST_API_KEY}
    
    if isinstance(localizacion, str):
        url = GC_MAPQUEST_API_URL
        parametros_url["location"] = localizacion
        parametros_url["ignoreLatLngInput"] = "true"
    else:
        try:
            parametros_url["location"] = \
                "{},{}".format(localizacion[0], localizacion[1])
        except (TypeError, IndexError):
            raise TypeError("Formato de localización incorrecto.")
        
        if len(localizacion) != 2:
            raise TypeError("Debes introducir solo dos coordenadas.")
        
        url = GCI_MAPQUEST_API_URL
    
    res = requests.get(url, parametros_url).json()
    if res["info"]["statuscode"] != 0:
        raise RuntimeError("Error API Mapquest: ({}) {}"
                            .format(res["info"]["statuscode"], 
                                    res["info"]["messages"]))
   
    loc = res["results"][0]["locations"][0]
    direccion = "{}{}{}{}{}{}{}".format(loc["street"], 
                    '(' + loc["postalCode"] + ')' if loc["postalCode"] else "", 
                    ", " + loc["adminArea6"] if loc["adminArea6"] else "",
                    ", " + loc["adminArea5"] if loc["adminArea5"] else "",
                    ", " + loc["adminArea4"] if loc["adminArea4"] else "",
                    ", " + loc["adminArea3"] if loc["adminArea3"] else "", 
                    ", " + loc["adminArea1"] if loc["adminArea1"] else "") 
    coordenadas = loc["latLng"]["lat"], loc["latLng"]["lng"]

    return {"direccion": direccion, "coordenadas": coordenadas, 
            "mapa_url": loc["mapUrl"], "copyright": res["info"]["copyright"]}



def sunrise_sunset(latitud, longitud, fecha=None, local=False):
    """
    Obtener los datos de las horas de la puesta, salida y crepúsculo
    del sol usando la API sunrise-sunset.org.

    Argumentos:
        latitud: latitud donde obtener las horas del sol.
        longitud: longitud donde obtener las horas del sol.
        fecha: fecha en el cual obtener las horas del sol. Tiene que
            ser tipo datetime.date. Por defecto se toma la fecha actual
            local de la localización solicitada.
        local: flag para indicar si las horas a obtener son locales
            o UTC
    
    Retorno:
        Diccionario con las hora y fecha UTC de cada evento del sol 
            en formato datetime.datetime, excepto "duracion_dia" que 
            tiene formato datetime.timdelta. 
    
    Excepciones:
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
        TypeError si los tipos de argumentos no son correctos.
    """
    if local or fecha is None:
        datos_api = timezonedb_get((latitud, longitud))

    if fecha is None:
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
        if local:
            zona_horaria = tz.timezone(datos_api["zona_horaria"])
            fechahoras_eventos_sol[evento] = zona_horaria.fromutc(fechahora)
        else:
            fechahoras_eventos_sol[evento] = tz.UTC.localize(fechahora)

    return fechahoras_eventos_sol



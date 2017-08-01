#/usr/bin/env python3
#!coding=utf-8

"""
Módulo con utilidades generales.
"""

import requests
from collections import Sequence
from numbers import Number
from claves import MAP_API_KEY

# API's
SOL_API_URL = "https://api.sunrise-sunset.org/json"
MAP_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def obtener_coordenadas(direccion, region = None):
    """
    Obtener las coordenadas (latitud, longitud) de una dirección.
    
    Argumentos:
        direccion: direccion a obtener sus coordenadas.
        region: código de región donde está la dirección solicitada.

    Retorno:
        Tupla con el par (latitud, longitud)
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
    """
    parametros_url = {"address": direccion, "key": MAP_API_KEY, 
                      "language": "es"}
    if region is not None:
        parametros_url["region"] = region

    res = requests.get(MAP_API_URL, parametros_url)
    if res["status"] == "OK":
        return (res["results"][0]["geometry"]["location"]["lat"],
                res["results"][0]["geometry"]["location"]["lng"])

    raise RuntimeError("Error al acceder a la API de Google: {}"
                       .format(res["results"]))


def obtener_direccion(latitud, longitud):
    """
    Obtener direccion a partir de unas coordenadas (latitud, longitud).
    
    Argumentos:
        latitud: latitud de la coordenada.
        longitud: longitud de la coordenada.

    Retorno:
        Cadena con la dirección de la coordenada.
        RuntimeError en caso de no obtener resultado de la API. Contiene
            el tipo de error devuelto por la API.
    
    Mejoras:
        Tener en cuenta los parámetros result_type y location_type de
            la API.
    """
    latlng = "{}, {}".format(latitud, longitud)
    res = requests.get(MAP_API_URL, {"latlng": latlng, "key": MAP_API_KEY,
                                     "language": "es"})
    if res["status"] == "OK":
        return res["results"][0]["formatted_address"]

    raise RuntimeError("Error al acceder a la API de Google: {}"
                       .format(res["results"]))


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


#/usr/bin/env python3
#!coding=utf-8

"""
Módulo con utilidades generales.
"""

# imports
import datetime as dt
from collections import Sequence
from numbers import Number
from ast import literal_eval


# Rango permitido de coordenadas.
RANGO_LAT = {"max": 90,  "min": -90}
RANGO_LNG = {"max": 180, "min": -180}



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

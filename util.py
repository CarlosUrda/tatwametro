#/usr/bin/env python3
#!coding=utf-8

"""
Módulo con utilidades para los ejercicios del libro.
"""

from collections import Sequence
from numbers import Number


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


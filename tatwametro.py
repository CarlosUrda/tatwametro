#!/usr/bin/env python3
#coding=utf-8

"""
Programa para calcular tatwas

- Coordenadas por IP
- Horario de Tatwas.
- Hora más próxima de tatwa.
- Horario de un tatwa en concreto.
- Solucionar fecha de sol para día de hoy.
- Hacer interfaz.
- Gestión correcta de excepciones.
- Pylint
- Mejorar documentación.
- Separar util.py en util y api
- Crear paquete a partir de util.py
"""

import util as ut
import tatwa as tw
import datetime as dt
from ast import literal_eval


def evaluar_coordenadas(entrada):
    try:
        coordenadas = literal_eval(entrada)
    except ValueError:
        raise ValueError("ERROR: Coordenadas en formato incorrecto.")

    try:
        return ut.convertir_coordenadas(*coordenadas)
    except TypeError:

def main():
    """
    Función principal
    """
    ancho_pantalla = 79
    print("*" * ancho_pantalla,
          "  T A T W Á M E T R O  ".center(ancho_pantalla, "*"),
          "*" * ancho_pantalla, sep = "\n")

    entorno_tatwas = tw.EntornoTatwas()

    coordenadas = ut.obtener_dato("Introduce coordenadas (latitud, longitud): ",
                                  evaluar_coordenadas)
    entorno_tatwas.fijar_coordenadas(*coordenadas)
    print("Coordenadas fijadas: {} => {}"
          .format(entorno_tatwas.coordenadas, entorno_tatwas.direccion))
    print("\nObteniendo las horas de salida del sol de hoy....\n")
    entorno_tatwas.actualizar_fechahoras_eventos_sol()
    print("Hora de salida del sol ({}): {}"
          .format(entorno_tatwas._fecha_sol_usada.strftime("%d-%m-%Y"), 
                  entorno_tatwas._fechahoras_eventos_sol["salida"].time()))
    print("\nCalculando los tatwas....\n")
    entorno_tatwas.calcular_tatwas()
    print("(Tatwa calculado a las {} después de la salida del sol)"
          .format(entorno_tatwas._hora_tw_usada.strftime("%H:%M:%S"))
          .center(ancho_pantalla))
    print(" INFORMACIÓN DEL TATWA CALCULADO ".center(ancho_pantalla, "·"))
    print("Nombre:", entorno_tatwas._tatwas["salida"]["tatwa"])
    print("Hora inicio:", 
        entorno_tatwas._tatwas["salida"]["fechahora_inicio"].time())
    print("Hora fin:", 
        entorno_tatwas._tatwas["salida"]["fechahora_fin"].time())
    segundos_restantes = entorno_tatwas._tatwas["salida"]["segundos_restantes"]
    print("Tiempo restante:", 
        (dt.datetime.min + segundos_restantes).strftime("%M:%S")) 

if __name__ in ("__main__", "__console__"):
    main()

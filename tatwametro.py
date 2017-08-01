#!/usr/bin/env python3
#coding=utf-8

"""
Programa para calcular tatwas
"""

import util
from ast import literal_eval
import time



def inicializar_parametros():
    """
    Inicializar los parámetros usados para obtener la hora de salida del sol.
    """
    global hora_tatwa, direccion, coordenadas, hora_salida_sol
    
    hora_local = time.localtime()
    hora_tatwa["hora"] = hora_local.tm_hour
    hora_tatwa["min"] = hora_local.tm_min
    
    direccion = "Madrid"

    res = requests.get(MAP_API_URL, \
                       {"address": direccion, "key", MAP_API_KEY, 
                        "language": "es"}).json()
    if res["status"] not in ("OK", "ZERO_RESULTS"):
        raise 



def main():
    """
    Función principal
    """
    ancho_pantalla = 79
    print("*" * ancho_pantalla,
          "  T A T W Ó M E T R O  ".center(ancho_pantalla, "*"),
          "*" * ancho_pantalla, sep = "\n")

    inicializar_parametros()

    mostrar_parametros()

    util.obtener_dato()



if __name__ in ("__main__", "__console__"):
    main()

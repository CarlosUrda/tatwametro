#!/usr/bin/env python3
#coding=utf-8

"""
Programa para calcular tatwas

- Archivo de configuración con el nombre del log. Todo proyecto tendrá
este archivo y los módulos que contengan el proyecto usarán ese archivo
común para escribir logs.
- Coordenadas por IP
- Tabla de Horario de Tatwas.
- Hora más próxima de ocurrir un tatwa.
- Horario de un tatwa en concreto.
- Solucionar fecha de sol para día de hoy.
- Hacer interfaz.
- Gestión correcta de excepciones.
- Pylint
- Mejorar documentación.
- Separar util.py en util y api
- Crear paquete api a partir de util.py
"""

import util as ut
import tatwa as tw
import datetime as dt
from ast import literal_eval


def evaluar_coordenadas(entrada):
    try:
        return ut.convertir_coordenadas(*literal_eval(entrada))
    except (ValueError, SyntaxError, TypeError) as err:
        #print(err) Log
        raise ValueError("Introduce solo dos valores (latitud, longitud)"
                         " separadas por coma.")


def evaluar_fecha(entrada, formato="%d-%m-%Y").):
    """
    Evaluar una cadena de entrada para convertirla en datetime.date
    usando un formato determinado.

    Argumentos:
        entrada: cadena a evaluar.
        formato: formato usado para evaluar la cadena.

    Retorno:
        Valor datetime.time creado a partir de la cadena de entrada.

    Excepciones:
        ValueError si la cadena de entrada no está en el formato
            especificado por argumento.
    """
    try:
        return dt.datetime.strptime(entrada, formato).date()
    except (ValueError, TypeError) as err:
        #print(err) Log
        raise ValueError("Introduce la fecha en formato {}".format(formato))
        


def evaluar_hora(entrada, formato="%H-%M-%S"):
    """
    Evaluar una cadena de entrada para convertirla en datetime.time
    usando un formato determinado.

    Argumentos:
        entrada: cadena a evaluar.
        formato: formato usado para evaluar la cadena.

    Retorno:
        Valor datetime.time creado a partir de la cadena de entrada.

    Excepciones:
        ValueError si la cadena de entrada no está en el formato
            especificado por argumento.
    """
    try:
        return dt.datetime.strptime(entrada, formato).time()
    except (ValueError, TypeError) as err:
        #print(err) Log
        raise ValueError("Introduce la fecha en formato HH:MM:SS.")
        


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

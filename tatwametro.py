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
- No se puede acceder al resultado de los tatwas mediante _tatwas.
- Guardar zona horaria como tz.timezone en lugar de como cadena.
- Mirar el argumento final de localize.
"""

import util as ut
import tatwa as tw
import datetime as dt



def main():
    """
    Función principal
    """
    ancho_pantalla = 79
    print("*" * ancho_pantalla,
          "  T A T W Á M E T R O  ".center(ancho_pantalla, "*"),
          "*" * ancho_pantalla, "\n", sep = "\n")

    entorno_tw = tw.EntornoTatwas()

    coordenadas = ut.obtener_dato("Introduce coordenadas (latitud, longitud): ",
                                  ut.evaluar_coordenadas)
    entorno_tw.fijar_coordenadas(*coordenadas)
    print("Coordenadas fijadas: {} => {}\n"
          .format(entorno_tw.coordenadas, entorno_tw.direccion))

    entorno_tw.fecha_sol = \
        ut.obtener_dato("Introduce fecha salida del sol [DD-MM-YYYY] (fecha"
                        " última salida por defecto): ",
                        lambda x: ut.evaluar_fechahora(x, "%d-%m-%Y"), fin="")

    print("\nObteniendo las horas de salida del sol....\n")
    entorno_tw.actualizar_fechahoras_eventos_sol()
    fechahora_salida_sol = entorno_tw._fechahoras_eventos_sol["salida"]
    print("Fecha de salida del sol: {}\n"
          .format(fechahora_salida_sol.strftime("%H:%M:%S | %d/%m/%Y")))
    
    entorno_tw.hora_tw = \
        ut.obtener_dato("Introduce la hora a calcular tatwa [HH:MM:SS] (hora"
                        " actual por defecto): ",
                        lambda x: ut.evaluar_fechahora(x, "%H:%M:%S").time(), 
                        fin="")
    entorno_tw.fecha_tw = \
        ut.obtener_dato("Introduce fecha a calcular tatwa [DD-MM-YYYY] (fecha"
                        " actual por defecto): ",
                        lambda x: ut.evaluar_fechahora(x, "%d-%m-%Y").date(), 
                        fin="")

    print("\nCalculando los tatwas....\n")
    entorno_tw.calcular_tatwas()
    
    print(" INFORMACIÓN DEL TATWA CALCULADO ({}) "
          .format(entorno_tw._fechahora_tw.strftime("%H:%M:%S %d/%m/%Y"))
          .center(ancho_pantalla, "·"))
    if entorno_tw._tatwas["salida"] is None:
        print("El tatwa no puede ser calculado: fechas incoherentes")
    else:
        print("Nombre:", entorno_tw._tatwas["salida"]["tatwa"])
        print("Posición/Ciclo: {} / {}"
              .format(entorno_tw._tatwas["salida"]["tatwa"].posicion,
                      entorno_tw._tatwas["salida"]["tatwa"].ciclo))
        print("Hora inicio:", 
              entorno_tw._tatwas["salida"]["fechahora_inicio"].time())
        print("Hora fin:", 
              entorno_tw._tatwas["salida"]["fechahora_fin"].time())
        segundos_restantes = entorno_tw._tatwas["salida"]["segundos_restantes"]
        print("Tiempo restante:", 
            (dt.datetime.min + segundos_restantes).strftime("%M:%S")) 



if __name__ in ("__main__", "__console__"):
    main()

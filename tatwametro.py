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
import api


def main():
    """
    Función principal
    """
    ancho_pantalla = 79
    print("", "*" * ancho_pantalla,
          "  T A T W Á M E T R O  ".center(ancho_pantalla, "*"),
          "*" * ancho_pantalla, "", sep = "\n")

    entorno_tw = tw.EntornoTatwas()

    coordenadas = ut.obtener_dato("Introduce coordenadas (latitud, longitud): ",
                                  ut.evaluar_coordenadas)
    entorno_tw.fijar_coordenadas(*coordenadas)
    print("\nCoordenadas fijadas (gracias a https://timezonedb.com/api):\n"
          "\t{} => {}\n".format(entorno_tw.coordenadas, entorno_tw.direccion))

    entorno_tw.fecha_sol = \
        ut.obtener_dato("Introduce fecha salida del sol [DD-MM-YYYY] (fecha"
                        " última salida por defecto): ",
                        lambda x: ut.evaluar_fechahora(x, "%d-%m-%Y"), fin="")

    print("\nObteniendo horas de salida del sol (gracias a"
          " https://sunrise-sunset.org/api)....\n")
    entorno_tw.actualizar_fechahoras_eventos_sol()
    for ev, fechahora_evento_sol in entorno_tw._fechahoras_eventos_sol.items():
        print("Fecha {} {}"
              .format(api.EVENTOS_SOL_DESCRIPCION[ev].ljust(35, '.'), 
                      fechahora_evento_sol.strftime("%H:%M:%S | %d/%m/%Y")))
    
    entorno_tw.hora_tw = \
        ut.obtener_dato("\nIntroduce la hora a calcular tatwa [HH:MM:SS] (hora"
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
    
    print(" INFORMACIÓN DE LOS TATWAS CALCULADOS ({}) "
          .format(entorno_tw._fechahora_tw.strftime("%H:%M:%S | %d/%m/%Y"))
          .center(ancho_pantalla, "·"), "\n")
    for ev, tatwa in entorno_tw._tatwas.items():
        print("*", api.EVENTOS_SOL_DESCRIPCION[ev].capitalize())
        if tatwa is None:
            print("El tatwa de no puede ser calculado: fechas incoherentes")
        else:
            ancho = 20
            print("\tNombre".ljust(ancho, '.'), tatwa["tatwa"])
            print("\tPosición / Ciclo".ljust(ancho, '.'),  
                  "{} / {}".format(tatwa["tatwa"].posicion, 
                                   tatwa["tatwa"].ciclo))
            print("\tHora inicio".ljust(ancho, '.'), 
                  tatwa["fechahora_inicio"].time())
            print("\tHora fin".ljust(ancho, '.'), 
                  tatwa["fechahora_fin"].time())
            print("\tTiempo restante".ljust(ancho, '.'), (dt.datetime.min 
                              + tatwa["segundos_restantes"]).strftime("%M:%S")) 
        print("")


if __name__ in ("__main__", "__console__"):
    main()

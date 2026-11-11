"""
Módulo: sesion_spark.py
Descripción: Crea y configura la sesión de Spark
Autor/a: Josefina Mercado
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""

import os
import sys

from pyspark.sql import SparkSession

def crear_sesion(nombre_app):
    """
    Crea la sesion de spark y la retorna.
    indica a Spark que use el mismo Python que ejecuta el programa par us procesos

    Parametros
    nombre_app (str) nombre de la aplicacion en spark 

    Retorna:
    Spark session
    """
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    sesion = (
        SparkSession.builder
        .appName(nombre_app)                    # nombre de la aplicacion
        .master("local[*]")                     # le dice a spark que corra localmente y que use los nucleos del procesador como executors
        .config("spark.ui.showConsoleProgress", "false") # oculta las barras de progreso
        .getOrCreate()
                         
                                  # crear u obtiene la sesion de spark, si ya hay una sesion abierta la reutiliza, sino crea una nueva
    )                                           # dentro del parentesis = una sola instruccion / syntax error
    sesion.sparkContext.setLogLevel("ERROR")    # setea el nivel de log a ERROR para no mostrar INFO y WARN
    return sesion
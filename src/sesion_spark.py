"""
Módulo: sesion_spark.py
Descripción: Crea y configura la sesión de Spark
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""

from pyspark.sql import SparkSession
from src.config import NOMBRE_APP

def crear_sesion(nombre_app):
    """
    Crea la sesion de spark y la retorna
    """
    sesion = (
        SparkSession.builder
        .appName(nombre_app)                    # nombre de la aplicacion
        .master("local[*]")                     # le dice a spark que corra localmente y que use los nucleos del procesador como executors
        .config("spark.ui.showConsoleProgress", "false")
        .getOrCreate()
                         
                                  # crear u obtiene la sesion de spark, si ya hay una sesion abierta la reutiliza, sino crea una nueva
    )                                           # dentro del parentesis = una sola instruccion / syntax error
    sesion.sparkContext.setLogLevel("ERROR")    # setea el nivel de log a ERROR para no mostrar INFO y WARN
    return sesion
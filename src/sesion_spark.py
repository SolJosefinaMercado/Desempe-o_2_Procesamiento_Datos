'''
Responsabilidad de este modulo:
- Crear la sesion de spark y entregarla a los demas modulos
- Cuando se cree la sesion de spark, el Driver se conecta con el motor de Spark, arranca el
Spark Context y pide recursos al cluster Manager. 
'''
from pyspark.sql import SparkSession

def crear_sesion(nombre_app):
    """
    Crea la sesion de spark y la retorna
    """
    sesion = (
        SparkSession.builder
        .appName(nombre_app)                    # nombre de la aplicacion
        .master("local[*]")                     # le dice a spark que corra localmente y que use los nucleos del procesador como executors
        .getOrCreate()                          # crear u obtiene la sesion de spark, si ya hay una sesion abierta la reutiliza, sino crea una nueva
    )                                           # dentro del parentesis = una sola instruccion / syntax error
    sesion.sparkContext.setLogLevel("ERROR")    # setea el nivel de log a ERROR para no mostrar INFO y WARN
    return sesion

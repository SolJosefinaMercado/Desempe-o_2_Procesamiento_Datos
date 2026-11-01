'''
Resposabilidad del modulo Main:
Coordinar la ejecución del programa, llamar a los otros modulos en el orden correcto
'''
from src.sesion_spark import crear_sesion


if __name__ == "__main__":
    from src.sesion_spark import crear_sesion
    from src import config
    from src.carga_datos import descargar_dataset, leer_dataset, validar_columnas

    spark = crear_sesion(config.NOMBRE_APP)

    ruta = descargar_dataset(config.DATASET_URL, config.RUTA_TAXI_RAW)
    df = leer_dataset(spark, ruta)

    print('*'*50)
    df.show(5)
    print('*'*50)
    print("Filas:", df.count())
    print('*'*50)
    df.describe().show()

    spark.stop()
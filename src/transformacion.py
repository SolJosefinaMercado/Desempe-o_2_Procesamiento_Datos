"""
Módulo: transformacion.py
Descripción: Crea las variables derivadas, filtra viajes absurdos y guarda la tabla lista para el análisis.
Autor/a: Josefina Mercado 
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: DataFrame limpio de viajes (salida de limpieza) y DataFrame de zonas
Salida: DataFrame final y archivo Parquet en data/processed
"""
from pyspark.sql import functions as F
from pyspark.sql.functions import col

from src.config import (ZONAS_AEROPUERTO, DURACION_MIN, DURACION_MAX, VELOCIDAD_MAX,
                        COLUMNAS_FINALES, RUTA_PROCESSED)

def agregar_variables_tiempo(df):
    """
    Agrega variables de calendario a partir de la hora de subida.
    Se usa la subida porque es el momento en que se pide el viaje.

    Parámetros:
    df (DataFrame): DataFrame de Spark.

    Retorna:
    DataFrame: Con las columnas hora (0-23), dia_semana (1=domingo ... 7=sábado) y es_fin_de_semana (0/1).
    """
    # "hora" es columna nueva, F.hour extrae la hora de "tpep_pickup_datetime" en formato 24h (0-23) valor entero
    df = df.withColumn("hora", F.hour("tpep_pickup_datetime"))

    # "dia_semana" es columna nueva, F.dayofweek devuelve un valor entero (1=domingo, 2=lunes, ..., 7=sábado)
    df = df.withColumn("dia_semana", F.dayofweek("tpep_pickup_datetime"))

    # "es_fin_de_semana" es columna nueva, 1 si es sábado o domingo, 0 si es lunes a viernes
    df = df.withColumn("es_fin_de_semana", F.when(F.dayofweek("tpep_pickup_datetime").isin([1, 7]), 1).otherwise(0))
    return df
# ------------------------------------------------------------------------------------------------------------
def agregar_variables_velocidad(df):
    """
    Calcula la duracion del viaje en minutos y la velocidad en millas por hora
    La velocidad solo se calcula si la duracion es mayor a cero, sino es nula.
    El filtro de viajes absurdos elimina las filas con posible division por cero.

    Parametros:
    df (DataFrame) Spark

    Retorna:
    DataFrame con las columnas 'duracion_min' y 'velocidad_mph
    """
    df = df.withColumn(
        "duracion_min",
        (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60
    )
    df = df.withColumn(
        "velocidad_mph",
        F.when(col("duracion_min") > 0, col("trip_distance") / (col("duracion_min") / 60))
    )
    return df                  
# ------------------------------------------------------------------------------------------------------------
def agregar_es_aeropuerto(df, zonas_aeropuerto):
    """ 
    Marca los viajes de aeropuerto
    1 si la subida o bajada es en zona de aeropuerto 
    0 si no.
    
    Parametros:
    df spark 
    zonas_aeropuerto (lista) ID zona

    Retorna
    DataFrame con la columna binaria es_aeropuerto
    """
    df = df.withColumn(
        "es_aeropuerto",
        (col("PULocationID").isin(zonas_aeropuerto)     # condicionales OR
         | col("DOLocationID").isin(zonas_aeropuerto)
         | col("RatecodeID").isin(2, 3)).cast("int")
    )
    return df
# ------------------------------------------------------------------------------------------------------------
def agregar_distritos(df, zonas):
    """ 
    Agrega el distrito (Borough) de subida y de bajada con dos joins contra la tabla de zonas.
    Se usa broadcast porque la tabla de zonas es chica (265 filas): Spark envía una copia
    a cada executor y evita redistribuir los millones de viajes por la red.
    Se usa left join para no perder viajes cuya zona no figure en la tabla.

    Broadcast join. La tabla de zonas tiene solo 265 filas. En vez de mover los 3 millones de viajes, 
    Spark manda una copia completa de la tabla chica a cada executor. Cada executor ya tiene sus viajes, 
    recibe la tabla de zonas entera y hace el join en el lugar, sin mover ningún viaje.
    Así se evita el shuffle, que es redistribuir los casi 3 millones de viajes por la red.

    Parámetros:
    df (DataFrame): DataFrame de viajes.
    zonas (DataFrame): Tabla de zonas (LocationID, Borough, ...).

    Retorna:
    DataFrame: Con las columnas distrito_subida y distrito_bajada.
    """
    zonas_sub = zonas.select(col("LocationID").alias("PU_id"), col("Borough").alias("distrito_subida"))
    df = df.join(F.broadcast(zonas_sub), df.PULocationID == zonas_sub.PU_id, "left").drop("PU_id")

    zonas_baj = zonas.select(col("LocationID").alias("DO_id"), col("Borough").alias("distrito_bajada"))
    df = df.join(F.broadcast(zonas_baj), df.DOLocationID == zonas_baj.DO_id, "left").drop("DO_id")
    return df
# ------------------------------------------------------------------------------------------------------------
def filtrar_viajes_absurdos(df):
    """
    Elimina viajes con duración o velocidad imposibles, que solo pueden detectarse
    una vez calculadas esas columnas: duración fuera de DURACION_MIN a DURACION_MAX minutos,
    o velocidad nula, 0 o mayor a VELOCIDAD_MAX mph.

    Parámetros:
    df (DataFrame): DataFrame con duracion_min y velocidad_mph.

    Retorna:
    DataFrame: Sin los viajes absurdos.
    """
    df = df.filter(
        col("duracion_min").between(DURACION_MIN, DURACION_MAX)
        & (col("velocidad_mph") > 0)
        & (col("velocidad_mph") < VELOCIDAD_MAX)
    )
    print("- Viajes con duración o velocidad absurdas eliminados")
    return df
# ------------------------------------------------------------------------------------------------------------
def seleccionar_columnas(df, columnas):
    """
    Deja solo las columnas útiles para el análisis y el modelo.

    Parámetros:
    df (DataFrame): DataFrame de Spark.
    columnas (list): Columnas a conservar.

    Retorna:
    DataFrame: Solo con las columnas indicadas.
    """
    print("- Columnas antes:", len(df.columns))
    df = df.select(columnas)
    print("- Columnas después:", len(df.columns))
    return df
# ------------------------------------------------------------------------------------------------------------
def guardar_procesado(df, ruta_destino):
    """
    Guarda el DataFrame en formato Parquet. Es la tabla que usan el EDA y el modelo.
    Spark escribe una carpeta con varios archivos (uno por partición).
    mode("overwrite") reemplaza el resultado anterior si ya existe.

    Parámetros:
    df (DataFrame): DataFrame a guardar.
    ruta_destino (str): Carpeta de destino.

    Retorna:
    None.
    """
    # coalesce(4) junta las particiones en 4 sin redistribuir los datos por la red: menos archivos chicos
    df.coalesce(4).write.mode("overwrite").parquet(ruta_destino)
    print(f"- Datos procesados guardados en {ruta_destino}")
# ------------------------------------------------------------------------------------------------------------
def transformar_datos(df, zonas):
    """
    Coordina la transformación: variables nuevas, filtro de viajes absurdos,
    selección de columnas y guardado.

    Parámetros:
    df (DataFrame): DataFrame limpio de viajes.
    zonas (DataFrame): Tabla de zonas.

    Retorna:
    DataFrame: La tabla final, también guardada en RUTA_PROCESADO.
    """
    df = agregar_variables_tiempo(df)
    df = agregar_variables_velocidad(df)
    df = agregar_es_aeropuerto(df, ZONAS_AEROPUERTO)
    df = agregar_distritos(df, zonas)
    df = filtrar_viajes_absurdos(df)
    df = seleccionar_columnas(df, COLUMNAS_FINALES)
    guardar_procesado(df, RUTA_PROCESSED)
    return df
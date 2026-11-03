""" 
Modulo: persistencia_sql.py
Descripcion: Guarda en Sqlite los resultados agreagdos del EDA y del modelo
y permite consultarlos con SQL

Autor/a: <nombre> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: DataFrames chicos de Spark (resultados del EDA y del modelo)
Salida: base SQLite en data/resultados.db y DataFrames de pandas con el resultado de las consultas
"""

import os 
import sqlite3
import pandas as pd

def spark_a_pandas(df_spark):
    """
    Convierte un dataframe de spark a pandas
    Solo debe usarse con tablas agregadas o muestras: toPandas()
    Trae todos los datos a la memoria de una sola maquina

    Parametros:
    df_spark: tabla chica a convertir
    Retorna:
    Dataframe de pandas 
    """
    return df_spark.toPandas 

def guardar_tabla(df_pandas, nombre_tabla, ruta_db):
    """
    Guarda un DataFrame de pandas como tabla en la base SQLite.
    si la tabla ya existe, la reemplaza, para que correr el pipeline
    nuevamente no duplique los datos.

    Parametros:
    df_pandas (DataFrame de pandas): datos a guardar
    nombre_tabla (srt): nombre de la tabla en la base
    ruta_db (str): ruta del archivo .db

    no retorna nada
    """
    os.makedirs(os.path.dirname(ruta_db), exist_ok=True)
    # abre la conexión con la base y la cierra sola al terminar.
    with sqlite3.connect(ruta_db) as conexion:
        df_pandas.to_sql(nombre_tabla, conexion, if_exists="replace", index=False)
    print(f"Tabla {nombre_tabla} guardada, ({len(df_pandas)} filas)")
# ------------------------------------------------------------------------------------------------------------
def guardar_resultados(resultados, ruta_db):
    """
    Guarda varios resultados de Spark de una sola vez

    Prametros
    resultados (dict) nombre de la tabla -> DataFrame de Spark
    ruta_db (str)

    No retorna nada
    """
    for nombre, df_spark in resultados.items():
        guardar_tabla(spark_a_pandas(df_spark), nombre, ruta_db)
# ------------------------------------------------------------------------------------------------------------
def consultar(sql, ruta_db):
    """
    Ejecuta una consulta SQL sobre la base y devuelve el resultado

    Parametros_
    sql (str) consulta SQL
    ruta_db del archivo .db

    Retorna:
    Data]Frame de pandas con el resultado
    """
    with sqlite3.connect(ruta_db) as conexion:
        return pd.read_sql(sql, conexion)
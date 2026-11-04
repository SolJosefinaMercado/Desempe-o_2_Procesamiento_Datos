"""
Módulo: carga_datos.py
Descripción: carga el dataset desde la URL y lo carga en spark 
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""
import os
import requests
from src.config import DATASET_URL, RUTA_TAXI_RAW, ZONAS_URL, RUTA_ZONAS_RAW, COLUMNAS_REQUERIDAS


def descargar_dataset(url, ruta_destino): # ruta_destino = RUTA_RAW
    """
    Descarga un archivo desde la URL y lo guarda en disco.
    como Spark solo lee archivos locales, primero se descarga el dataset y luego se lee desde la ruta local.
    si el archivo ya existe, no se descarga nuevamente y se retorna la ruta del archivo existente.

    Parámetros:
    url (str): La URL del dataset a descargar.
    ruta_destino (str): La ruta donde se guardará el archivo descargado.

    Retorna:
    str: La ruta del archivo descargado o existente.
    """
    if os.path.exists(ruta_destino):
        print(f"El archivo ya existe en la ruta: {ruta_destino}. No se descargará nuevamente.")
        return ruta_destino  
    
    # Creo la carpeta donde va a quedar el archivo
    os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)

    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status() # Lanza una excepción si la descarga falla
                                          
        with open(ruta_destino, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024): # Descarga en bloques de 1 MB
                file.write(chunk)
    print(f'Archivo descargado desde {url} y guardado en {ruta_destino}.')
    return ruta_destino  
# ------------------------------------------------------------------------------------------------------------
def leer_dataset(spark, ruta_archivo): # ruta_archivo = RUTA_RAW
    """
    Lee el archivo Parquet de viajes en taxi.
    Parquet guarda los nombres y tipos de las columnas.
    
    Parámetros:
    spark (SparkSession): La sesión de Spark.
    ruta_archivo (str): La ruta del archivo Parquet a leer.
    
    Retorna:
    DataFrame: Un DataFrame de Spark con los datos leídos del archivo Parquet.
    """
    df = spark.read.parquet(ruta_archivo)  # Lee el archivo parquet
    return df
# ------------------------------------------------------------------------------------------------------------
def leer_zonas(spark, ruta_archivo):
    """
    Lee el CSV de zonas de taxi de la TLC.

    Parámetros:
    spark (SparkSession): La sesión de Spark.
    ruta_archivo (str): La ruta del archivo CSV.

    Retorna:
    DataFrame: Tabla de zonas (LocationID, Borough, Zone, service_zone).
    """
    # header=True: la primera fila tiene los nombres de columna
    # inferSchema=True: Spark deduce el tipo de cada columna (en un CSV todo es texto)
    zonas = spark.read.csv(ruta_archivo, header=True, inferSchema=True)
    return zonas
# ------------------------------------------------------------------------------------------------------------
def validar_columnas(dataframe, columnas_requeridas): # columnas_requeridas = COLUMNAS_REQUERIDAS
    """
    Verifica que el DataFrame tenga todas las columnas requeridas. No modifica el DataFrame.

    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark a validar.
    columnas_requeridas (list): Nombres de las columnas que deben estar presentes.

    Retorna:
    None. Lanza ValueError si falta alguna columna.
    """
    faltantes = [c for c in columnas_requeridas if c not in dataframe.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {faltantes}")
    print(f"Validación correcta: las {len(columnas_requeridas)} columnas requeridas están presentes.")

# ------------------------------------------------------------------------------------------------------------
def cargar_datos(spark):
    """
    Coordina el flujo de carga de los viajes: descarga, lectura y validacion.
    Recibe la sesion como parametro en lugar de crearla: la sesion (y el Driver) se crea una sola vez en main.py
    
    Prametros:
    spark (SparkSession): La sesión de Spark.
    Retorna:
    DataFrame: Los viaje crudos, ya validados.
    """
    ruta = descargar_dataset(DATASET_URL, RUTA_TAXI_RAW)
    df = leer_dataset(spark, ruta)
    validar_columnas(df, COLUMNAS_REQUERIDAS)
    return df
# ------------------------------------------------------------------------------------------------------------
def cargar_zonas(spark):
    """
    Coordina la carga de la tabla de zonas: descarga y lectura.

    Parámetros:
    spark (SparkSession): La sesión de Spark.

    Retorna:
    DataFrame: Tabla de zonas.
    """
    ruta = descargar_dataset(ZONAS_URL, RUTA_ZONAS_RAW)
    return leer_zonas(spark, ruta)

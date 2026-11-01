"""
Módulo: carga_datos.py
Descripción: carga el dataset desde la URL y lo carga en spark 
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""
from importlib.resources import path
import os
import requests
from src.config import DATASET_URL

def descargar_dataset(url, ruta_destino): # ruta_destino = RUTA_RAW
    """
    Parámetros:
    url (str): La URL del dataset a descargar.
    ruta_destino (str): La ruta donde se guardará el archivo descargado.
    como spark solo lee archivos locales, primero se descarga el dataset y luego se lee desde la ruta local.
    """
    if os.path.exists(ruta_destino):
        print(f"El archivo ya existe en la ruta: {ruta_destino}. No se descargará nuevamente.")
        return ruta_destino  # Retorna la ruta del archivo existente
    
    # Creo la carpeta donde va a quedar el archivo
    os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)

    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()  # Lanza una excepción si la descarga falla
        with open(ruta_destino, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024): # Descarga en bloques de 1 MB
                file.write(chunk)
    print("Descarga completada. Archivo guardado en:", ruta_destino)
    return ruta_destino  


def leer_dataset(spark, ruta_archivo): # ruta_archivo = RUTA_RAW
    df = spark.read.parquet(ruta_archivo)  # Lee el archivo parquet
    return df

def validar_columnas(dataframe, columnas_requeridas): # columnas_requeridas = COLUMNAS_REQUERIDAS
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a validar.
    columnas_requeridas (list): Una lista de nombres de columnas que se esperan en el DataFrame.
    
    Retorna:
    bool: True si todas las columnas requeridas están presentes, False en caso contrario.
    """
    # Implementación de la función para validar las columnas del DataFrame
    pass  # Reemplazar con la lógica de validación

def cargar_datos(spark):
  
    # recibe la sesión como parámetro en lugar de crearla: la sesión (y el Driver) se crea una sola vez en main.py
    # Carga los datos desde un archivo parquet y los devuelve en un dataframe de spark
    
    df = spark.read.parquet(path, header=True, inferSchema=True) 
    
    # header = True indica que la primera fila del archivo parquet contiene los nombres de las columnas
    # inferSchema = True indica que spark debe inferir el tipo de dato de cada columna             
    return df

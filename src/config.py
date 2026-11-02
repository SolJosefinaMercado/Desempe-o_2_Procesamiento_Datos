"""
Módulo: config.py
Descripción: Guarda las configuraciones del proyecto y las rutas de los archivos de entrada y salida.
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""
from pathlib import Path 

NOMBRE_APP = "NYC_Taxi_Data"  # Nombre de la spark session
DATASET_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet" 
RUTA_RAW = "./data/raw"  # Ruta del archivo raw
RUTA_TAXI_RAW = "./data/raw/yellow_tripdata_2024-01.parquet"
RUTA_PROCESSED = "./data/processed/taxi_limpio"  # Ruta del archivo procesado
RUTA_DB = "./data/nyc_taxi.db"  # Ruta de la base SQLite
SEMILLA = 42  # Semilla para la generación de números aleatorios
COLUMNAS_REQUERIDAS = ['tpep_pickup_datetime', 'passenger_count', 'trip_distance', 
                       'PULocationID', 'DOLocationID', 'RatecodeID', 
                       'payment_type', 'fare_amount', 'tip_amount', 
                       'tolls_amount', 'total_amount']
# Lista de columnas que el dataset debe contener para ser considerado válido.
COLUMNAS_IMPUTAR = ['passenger_count', 'RatecodeID'] 
FECHA_INICIO = "2024-01-01"  # Fecha de inicio para filtrar los datos
FECHA_FIN = "2024-02-01"  # Fecha de fin para filtrar los datos
DISTANCIA_MAX_MILLAS = 100  # Distancia máxima en millas para filtrar los datos

DICT_TIPOS = {"passenger_count": "int", "RatecodeID": "int", "payment_type": "int"}
ZONAS_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
RUTA_ZONAS_RAW = "./data/raw/taxi_zone_lookup.csv"
ZONAS_AEROPUERTO = [1, 132, 138]  # Lista de LocationID de los aeropuertos (JFK, LGA, EWR)
DURACION_MIN, DURACION_MAX = 1, 180 # MIN y MAX duración de viaje en minutos
VELOCIDAD_MAX = 80 

COLUMNAS_FINALES = [
    "tpep_pickup_datetime", "trip_distance", "RatecodeID", "PULocationID", "DOLocationID",
    "passenger_count", "payment_type", "fare_amount", "tip_amount", "tolls_amount", "total_amount",
    "duracion_min", "velocidad_mph", "hora", "dia_semana", "es_fin_de_semana", "es_aeropuerto",
    "distrito_subida", "distrito_bajada", "nulos_imputados",
]
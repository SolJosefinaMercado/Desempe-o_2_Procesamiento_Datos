"""
Módulo: config.py
Descripción: Guarda las configuraciones del proyecto y las rutas de los archivos de entrada y salida.
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""

NOMBRE_APP = "NYC_Taxi_Data"  # Nombre de la spark session
DATASET_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet" 
RUTA_RAW = "./data/raw"  # Ruta del archivo raw
RUTA_TAXI_RAW = "./data/raw/yellow_tripdata_2024-01.parquet"
RUTA_PROCESSED = "./data/processed"  # Ruta del archivo procesado
RUTA_DB = "./data/nyc_taxi.db"  # Ruta de la base SQLite
SEMILLA = 42  # Semilla para la generación de números aleatorios
COLUMNAS_REQUERIDAS = ["VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count", "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID", "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount", "tolls_amount", "improvement_surcharge", "total_amount"]  # Lista de columnas que el dataset debe contener para ser considerado válido.

DICT_TIPOS = {"passenger_count": "int", "RatecodeID": "int", "payment_type": "int"}
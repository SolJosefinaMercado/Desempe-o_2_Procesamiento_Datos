"""
Módulo: config.py
Descripción: Guarda las configuraciones del proyecto y las rutas de los archivos de entrada y salida.
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""
from pathlib import Path 

RAIZ = Path(__file__).resolve().parent.parent   # config.py está en src/, la raíz es la carpeta de arriba
NOMBRE_APP = "NYC_Taxi_Data"  # Nombre de la spark session
DATASET_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet" 
RUTA_RAW = "./data/raw"  # Ruta del archivo raw
RUTA_TAXI_RAW = str(RAIZ / "data" / "raw" / "yellow_tripdata_2024-01.parquet")
RUTA_PROCESSED = str(RAIZ / "data" / "processed" / "taxi_limpio")
RUTA_DB = str(RAIZ / "data" / "nyc_taxi.db")
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
RUTA_ZONAS_RAW = str(RAIZ / "data" / "raw" / "taxi_zone_lookup.csv")
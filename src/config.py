"""
Módulo: config.py
Descripción: Constantes del proyecto: URLs, rutas, listas de columnas y umbrales de los filtros.
Autor/a: Josefina Mercado 
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: ninguna
Salida: constantes usadas por el resto de los módulos
"""
from pathlib import Path

# --- Rutas (se arman desde la raíz del proyecto para que funcionen se ejecute desde donde se ejecute) ---
RAIZ = Path(__file__).resolve().parent.parent      # config.py está en src/, la raíz es la carpeta de arriba
RUTA_TAXI_RAW = str(RAIZ / "data" / "raw" / "yellow_tripdata_2024-01.parquet")
RUTA_ZONAS_RAW = str(RAIZ / "data" / "raw" / "taxi_zone_lookup.csv")
RUTA_PROCESSED = str(RAIZ / "data" / "processed" / "taxi_limpio")
RUTA_DB = str(RAIZ / "data" / "nyc_taxi.db")       # base SQLite con los resultados del EDA y del modelo

# --- Spark ---
NOMBRE_APP = "NYC_Taxi_Data"
SEMILLA = 42                                       # para muestras y splits reproducibles

# --- Fuentes de datos ---
DATASET_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
ZONAS_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

# --- Carga: columnas que el archivo original tiene que traer ---
COLUMNAS_REQUERIDAS = [
    "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count", "trip_distance",
    "RatecodeID", "PULocationID", "DOLocationID", "payment_type",
    "fare_amount", "tip_amount", "tolls_amount", "total_amount",
]

# --- Limpieza ---
DICT_TIPOS = {"passenger_count": "int", "RatecodeID": "int", "payment_type": "int"}
COLUMNAS_IMPUTAR = ["passenger_count", "RatecodeID"]
FECHA_INICIO = "2024-01-01"                        # inclusive
FECHA_FIN = "2024-02-01"                           # exclusivo
DISTANCIA_MAX_MILLAS = 100

# --- Transformación ---
ZONAS_AEROPUERTO = [1, 132, 138]                   # Newark (EWR), JFK, LaGuardia
DURACION_MIN, DURACION_MAX = 1, 180                # minutos
VELOCIDAD_MAX = 80                                 # millas por hora
COLUMNAS_FINALES = [
    "tpep_pickup_datetime", "trip_distance", "RatecodeID", "PULocationID", "DOLocationID",
    "passenger_count", "payment_type", "fare_amount", "tip_amount", "tolls_amount", "total_amount",
    "duracion_min", "velocidad_mph", "hora", "dia_semana", "es_fin_de_semana", "es_aeropuerto",
    "distrito_subida", "distrito_bajada", "nulos_imputados",
]
# --- Modelo (variables elegidas en el EDA, sección 9) ---
COLUMNA_OBJETIVO = "fare_amount"
VARIABLES_NUMERICAS = ["trip_distance", "es_aeropuerto"]
VARIABLES_CATEGORICAS = ["distrito_subida", "hora", "dia_semana"]
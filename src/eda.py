"""
Módulo: eda.py
Descripción: Análisis exploratorio con Spark. Cada función devuelve una tabla agregada.
Autor/a: Lucía Pellegrini (análisis) — Legajo <número> / Josefina Mercado (integración) — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: DataFrame final de viajes (Parquet) y tabla de zonas
Salida: diccionario {nombre_de_tabla: DataFrame agregado} para guardar en SQLite
"""
from pyspark.sql import functions as F
from pyspark.sql.functions import col


def viajes_por_hora(df):
    """Viajes y tarifa mediana por hora de subida (Hallazgos 1 y 6)."""
    return (df.groupBy("hora")
              .agg(F.count("*").alias("viajes"),
                   F.percentile_approx("fare_amount", 0.5).alias("tarifa_mediana"))
              .orderBy("hora"))
# ------------------------------------------------------------------------------------------------------------
def viajes_dia_hora(df):
    """Viajes por día de la semana (1 = domingo ... 7 = sábado) y hora (Hallazgo 1.1)."""
    return (df.groupBy("dia_semana", "hora")
              .agg(F.count("*").alias("viajes"))
              .orderBy("dia_semana", "hora"))
# ------------------------------------------------------------------------------------------------------------
def propina_por_pago(df):
    """Propina promedio y porcentaje de viajes sin propina según la forma de pago (Hallazgo 2)."""
    return (df.groupBy("payment_type")
              .agg(F.count("*").alias("viajes"),
                   F.round(F.avg("tip_amount"), 4).alias("propina_promedio"),
                   F.round(100 * F.avg(F.when(col("tip_amount") == 0, 1).otherwise(0)), 2)
                    .alias("pct_sin_propina"))
              .orderBy("payment_type"))
# ------------------------------------------------------------------------------------------------------------
def tarifa_por_distancia(df):
    """Tarifa mediana y tarifa por milla según rangos de distancia (Hallazgo 4)."""
    rango = (F.when(col("trip_distance") < 1, "0-1")
              .when(col("trip_distance") < 2, "1-2")
              .when(col("trip_distance") < 5, "2-5")
              .when(col("trip_distance") < 10, "5-10")
              .when(col("trip_distance") < 20, "10-20")
              .otherwise("20+"))
    orden = (F.when(col("trip_distance") < 1, 1).when(col("trip_distance") < 2, 2)
              .when(col("trip_distance") < 5, 3).when(col("trip_distance") < 10, 4)
              .when(col("trip_distance") < 20, 5).otherwise(6))
    return (df.withColumn("rango_distancia", rango)
              .withColumn("orden", orden)
              .withColumn("tarifa_por_milla", col("fare_amount") / col("trip_distance"))
              .groupBy("orden", "rango_distancia")
              .agg(F.count("*").alias("viajes"),
                   F.percentile_approx("fare_amount", 0.5).alias("tarifa_mediana"),
                   F.percentile_approx("tarifa_por_milla", 0.5).alias("tarifa_milla_mediana"))
              .orderBy("orden")
              .drop("orden"))
# ------------------------------------------------------------------------------------------------------------
def tarifa_por_distrito(df):
    """Viajes, tarifa y distancia medianas por distrito de subida (Hallazgo 5)."""
    return (df.groupBy("distrito_subida")
              .agg(F.count("*").alias("viajes"),
                   F.percentile_approx("fare_amount", 0.5).alias("tarifa_mediana"),
                   F.percentile_approx("trip_distance", 0.5).alias("distancia_mediana"))
              .orderBy(F.col("viajes").desc()))
# ------------------------------------------------------------------------------------------------------------
def top_zonas_subida(df, zonas):
    """Las 10 zonas de subida con más viajes y su tarifa mediana."""
    nombres = zonas.select(col("LocationID"), col("Zone").alias("zona"))
    return (df.join(F.broadcast(nombres), df.PULocationID == nombres.LocationID, "left")
              .groupBy("zona")
              .agg(F.count("*").alias("viajes"),
                   F.percentile_approx("fare_amount", 0.5).alias("tarifa_mediana"))
              .orderBy(F.col("viajes").desc())
              .limit(10))
# ------------------------------------------------------------------------------------------------------------
def correlaciones(df):
    """Correlación de Pearson de cada variable con la tarifa (sección 7 del EDA)."""
    variables = ["trip_distance", "passenger_count", "tolls_amount"]
    filas = [(v, float(df.stat.corr(v, "fare_amount"))) for v in variables]
    return df.sparkSession.createDataFrame(filas, ["variable", "correlacion"])
# ------------------------------------------------------------------------------------------------------------
def calcular_resultados_eda(df, zonas):
    """
    Calcula todas las tablas del EDA.

    Retorna:
    dict: nombre de tabla -> DataFrame de Spark agregado.
    """
    return {
        "viajes_por_hora": viajes_por_hora(df),
        "viajes_dia_hora": viajes_dia_hora(df),
        "propina_por_pago": propina_por_pago(df),
        "tarifa_por_distancia": tarifa_por_distancia(df),
        "tarifa_por_distrito": tarifa_por_distrito(df),
        "top_zonas_subida": top_zonas_subida(df, zonas),
        "correlaciones": correlaciones(df),
    }
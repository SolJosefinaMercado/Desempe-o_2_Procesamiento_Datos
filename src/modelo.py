"""
Módulo: modelo.py
Descripción: Modelo de regresión lineal con MLlib que predice la tarifa y la compara con dos referencias.
Autor/a: Santiago Mustillo — Legajo <número> / Josefina Mercado (integración)
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: DataFrame final de viajes
Salida: tabla de métricas (MAE por modelo) y muestra de predicciones, para guardar en SQLite
"""

from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import functions as F
from src.config import SEMILLA, COLUMNA_OBJETIVO, VARIABLES_NUMERICAS, VARIABLES_CATEGORICAS


def entrenar_modelo(viajes):
    """
    Entrena y evalúa tres modelos sobre el mismo conjunto de prueba (80/20):
    1. Tarifa fija: predice siempre la tarifa promedio del entrenamiento (referencia).
    2. Solo distancia: regresión lineal con trip_distance.
    3. Modelo ampliado: Pipeline de MLlib con las variables elegidas en el EDA.
    Las variables categóricas se indexan (StringIndexer) y codifican (OneHotEncoder)
    porque son códigos, no cantidades.

    Parámetros:
    df (DataFrame): DataFrame final de viajes.

    Retorna:
    tuple: (metricas, predicciones_muestra), dos DataFrames de Spark chicos.
    """
    datos_modelo = viajes.select(*VARIABLES_CATEGORICAS, *VARIABLES_NUMERICAS, COLUMNA_OBJETIVO)
    entrenamiento, prueba = datos_modelo.randomSplit([0.8, 0.2], seed=SEMILLA)
    armador_distancia = VectorAssembler(
        inputCols=["trip_distance"],
        outputCol="features",
    )
    regresion_distancia = LinearRegression(
        featuresCol="features",
        labelCol="fare_amount",
    )
    modelo_distancia = regresion_distancia.fit(
        armador_distancia.transform(entrenamiento)
    )
    predicciones_distancia = modelo_distancia.transform(
        armador_distancia.transform(prueba)
    )

    categorias = ["distrito_subida", "hora", "dia_semana"]
    columnas_indice = [f"{columna}_indice" for columna in categorias]
    columnas_codificadas = [f"{columna}_codificada" for columna in categorias]

    indexador = StringIndexer(
        inputCols=categorias,
        outputCols=columnas_indice,
        handleInvalid="keep",
    ).fit(entrenamiento)

    entrenamiento = indexador.transform(entrenamiento)
    prueba = indexador.transform(prueba)

    codificador = OneHotEncoder(
        inputCols=columnas_indice,
        outputCols=columnas_codificadas,
    ).fit(entrenamiento)

    entrenamiento = codificador.transform(entrenamiento)
    prueba = codificador.transform(prueba)

    armador = VectorAssembler(
        inputCols=["trip_distance", "es_aeropuerto"] + columnas_codificadas,
        outputCol="features",
    )
    entrenamiento_preparado = armador.transform(entrenamiento)
    prueba_preparada = armador.transform(prueba)

    regresion = LinearRegression(
        featuresCol="features",
        labelCol="fare_amount",
    )
    modelo = regresion.fit(entrenamiento_preparado)
    predicciones = modelo.transform(prueba_preparada)

    evaluador = RegressionEvaluator(
        labelCol="fare_amount",
        predictionCol="prediction",
        metricName="mae",
    )
    mae = evaluador.evaluate(predicciones)

    mae_distancia = evaluador.evaluate(predicciones_distancia)
    print(f"MAE solo distancia (misma prueba): USD {mae_distancia:.2f}")

    tarifa_promedio = entrenamiento.agg(F.avg("fare_amount")).first()[0]
    predicciones_base = prueba.withColumn("prediction", F.lit(tarifa_promedio))
    mae_base = evaluador.evaluate(predicciones_base)

    # Integración: resultados como tablas, para guardarlos en SQLite
    metricas = viajes.sparkSession.createDataFrame(
        [("Tarifa fija", float(mae_base)),
         ("Solo distancia", float(mae_distancia)),
         ("Modelo ampliado", float(mae))],
        ["modelo", "mae"],
    )
    predicciones_muestra = (predicciones
                            .select("fare_amount", "prediction", "distrito_subida")
                            .sample(fraction=0.01, seed=42))
    return metricas, predicciones_muestra


from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import functions as F


def entrenar_modelo(viajes):
    datos_modelo = viajes.select(
        "trip_distance",
        "es_aeropuerto",
        "distrito_subida",
        "hora",
        "dia_semana",
        "fare_amount",
    )
    entrenamiento, prueba = datos_modelo.randomSplit([0.8, 0.2], seed=42)

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

    return predicciones, mae, mae_base


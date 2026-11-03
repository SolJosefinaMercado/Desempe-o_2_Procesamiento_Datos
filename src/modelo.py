from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import functions as F


def entrenar_modelo(viajes):
    datos_modelo = viajes.select("trip_distance", "fare_amount")
    entrenamiento, prueba = datos_modelo.randomSplit([0.8, 0.2], seed=42)

    armador = VectorAssembler(
        inputCols=["trip_distance"],
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

    tarifa_promedio = entrenamiento.agg(F.avg("fare_amount")).first()[0]
    predicciones_base = prueba.withColumn("prediction", F.lit(tarifa_promedio))
    mae_base = evaluador.evaluate(predicciones_base)

    return predicciones, mae, mae_base


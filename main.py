'''
Resposabilidad del modulo Main:
Coordinar la ejecución del programa, llamar a los otros modulos en el orden correcto
'''
from src.sesion_spark import crear_sesion
from src import config
from src.carga_datos import descargar_dataset, leer_dataset, validar_columnas, cargar_datos
from pyspark.sql.functions import col, count, when
from src.config import DICT_TIPOS, NOMBRE_APP
from src.limpieza import limpiar_dataset
from src.carga_datos import cargar_datos, cargar_zonas
from src.transformacion import transformar_datos
from src.modelo import entrenar_modelo

if __name__ == "__main__":
    print("\n========== 1. CARGA ==========")
    spark = crear_sesion(NOMBRE_APP)
    df = cargar_datos(spark)

    print("\n========== 2. LIMPIEZA ==========")
    df = limpiar_dataset(df)

    print("\n========== 3. TRANSFORMACIÓN ==========")
    zonas = cargar_zonas(spark)
    df = transformar_datos(df, zonas)

    print("\n========== 4. ENTRENAMIENTO DEL MODELO ==========")
    predicciones, mae, mae_base = entrenar_modelo(df)
    print(f"MAE con distancia: USD {mae:.2f}")
    print(f"MAE tarifa fija:   USD {mae_base:.2f}")

    print("\n========== PIPELINE TERMINADO ==========")
    print(f"Filas finales: {df.count():,}")
    spark.stop()

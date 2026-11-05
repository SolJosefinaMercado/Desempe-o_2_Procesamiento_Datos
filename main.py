"""
Módulo: main.py
Descripción: Coordina el pipeline completo, llamando a los módulos en orden.
Autor/a: Equipo
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)
"""
import time

from src import config
from src.sesion_spark import crear_sesion
from src.carga_datos import cargar_datos, cargar_zonas
from src.limpieza import limpiar_dataset
from src.transformacion import transformar_datos
from src.eda import calcular_resultados_eda
from src.modelo import entrenar_modelo
from src.persistencia_sql import guardar_resultados

def segundos_desde(inicio):
    """Devuelve el tiempo transcurrido desde 'inicio', en segundos, como texto."""
    return f"{time.perf_counter() - inicio:.1f} s"


if __name__ == "__main__":

    spark = crear_sesion(config.NOMBRE_APP)

    print("\n========== 1. CARGA ==========")
    df = cargar_datos(spark)
    zonas = cargar_zonas(spark)

    print("\n========== 2. LIMPIEZA ==========")
    df = limpiar_dataset(df)

    print("\n========== 3. TRANSFORMACIÓN ==========")
    df = transformar_datos(df, zonas)

    print("\n========== 4. EDA ==========")
    print("calculando resultados")
    resultados = calcular_resultados_eda(df, zonas)

    print("\n========== 5. MODELO ==========")
    metricas, predicciones_muestra = entrenar_modelo(df)
    metricas.show()
    resultados["metricas_modelo"] = metricas
    resultados["predicciones_muestra"] = predicciones_muestra

    print("\n========== 6. PERSISTENCIA EN SQL ==========")
    guardar_resultados(resultados, config.RUTA_DB)

    print("\n========== PIPELINE TERMINADO ==========")
    print(f"Filas finales: {df.count():,}")
    print("Tiempo total:", segundos_desde(inicio_total))
    spark.stop()

    # DASHBOARD python -m streamlit run app/dashboard.py --server.headless true
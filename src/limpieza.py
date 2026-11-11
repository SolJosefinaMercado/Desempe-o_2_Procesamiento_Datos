"""
Módulo: limpieza.py
Descripción: Corrige tipos, trata nulos y elimina duplicados y registros con valores imposibles.
Autor/a: Josefina Mercado 
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: DataFrame crudo de viajes (salida de carga_datos.cargar_datos)
Salida: DataFrame limpio, listo para transformación
"""
from pyspark.sql.functions import col

from src.config import (DICT_TIPOS, COLUMNAS_IMPUTAR, FECHA_INICIO, FECHA_FIN,
                        DISTANCIA_MAX_MILLAS)

def corregir_tipos(df, tipos): 
    """
    Convierte las columnas indicadas al tipo de destino.
    Al leerse desde Parquet el esquema ya está tipado correctamente. 
    Solo se convierten tres columnas de códigos de bigint a int, 
    por consistencia y menor uso de memoria.
    * (ningún valor supera el máximo de int, 2.147.483.647).
    Las fechas se mantuvieron como timestamp_ntz para preservar la hora local de Nueva York.

    Parámetros: 
    df (DataFrame de Spark)  
    tipos (dict) columna : tipo destino.
    
    Retorna: 
    el DataFrame con los tipos corregidos.
    """
    for columna, tipo in tipos.items():
        df = df.withColumn(columna, col(columna).cast(tipo))
    print("- Tipos de datos corregidos:", tipos)
    return df
# ------------------------------------------------------------------------------------------------------------
def eliminar_duplicados(df): 
    """
    Elimina las filas duplicadas de todas las columnas del DataFrame
    
    Parámetros:
    df (DataFrame de Spark): El DataFrame del que se eliminarán los duplicados
    
    Retorna:
    DataFrame: El DataFrame sin duplicados
    """
    df = df.dropDuplicates()
    print("- Duplicados eliminados")
    return df
# ------------------------------------------------------------------------------------------------------------
def tratar_nulos(df, columnas):
    """
    Imputa los nulos de las columnas indicadas con la moda (valor más frecuente).
    Se usa la moda porque son columnas de conteo o de código, donde el promedio no tiene sentido.
    Antes de imputar, marca las filas afectadas en la columna 'nulos_imputados'.
    
    Parámetros:
    df (DataFrame): DataFrame de Spark.
    columnas (list): columnas a imputar.

    Retorna:
    DataFrame: DataFrame sin nulos en esas columnas, con la columna 'nulos_imputados'.
    """
    # 1. Marcar las filas que tienen algún nulo en esas columnas (antes de rellenar)
    condicion = None
    for c in columnas:
        condicion = col(c).isNull() if condicion is None else (condicion | col(c).isNull())
    
    df = df.withColumn("nulos_imputados", condicion)

    # 2. Calcular la moda de cada columna, ignorando los nulos
    print("- Tratamiento de nulos con la moda para las columnas:", columnas)
    modas = {}
    for c in columnas:
        modas[c] = (df.filter(col(c).isNotNull())
                      .groupBy(c).count()
                      .orderBy("count", ascending=False)
                      .first()[0])
        print(f"Moda de {c}: {modas[c]}")

    # 3. Rellenar los nulos con la moda de cada columna
    df = df.fillna(modas)
    print("- Valores nulos tratados")
    return df
# ------------------------------------------------------------------------------------------------------------
def filtrar_invalidos(df):
    """
    Elimina los registros con valores imposibles detectados en el análisis descriptivo:
    - montos de tarifa o total menores o iguales a 0 (reembolsos y anulaciones);
    - distancia igual a 0 o mayor a DISTANCIA_MAX_MILLAS (máximo observado: 312.722 millas);
    - cantidad de pasajeros fuera del rango 1 a 6;
    - RatecodeID fuera de los códigos válidos 1 a 6 (99 = desconocido);
    - viajes con subida fuera del mes analizado;
    - viajes cuya bajada no es posterior a la subida.

    Parámetros:
    df (DataFrame): DataFrame de Spark.

    Retorna:
    DataFrame: El DataFrame solo con registros válidos.
    """
    df = df.filter(
        (col("fare_amount") > 0)
        & (col("total_amount") > 0)
        & (col("trip_distance") > 0)                        # valores mayores a cero
        & (col("trip_distance") <= DISTANCIA_MAX_MILLAS)    # valores menores a DISTANCIA_MAX_MILLAS
        & (col("passenger_count").between(1, 6))
        & (col("RatecodeID").between(1, 6))
        & (col("tpep_pickup_datetime") >= FECHA_INICIO)
        & (col("tpep_pickup_datetime") < FECHA_FIN)         # filtro temporal: solo viajes del mes analizado
        & (col("tpep_dropoff_datetime") > col("tpep_pickup_datetime"))
    )
    print("- Registros inválidos eliminados")
    return df
# ------------------------------------------------------------------------------------------------------------
def limpiar_dataset(df): 
    """
    Coordina la limpieza: tipos, nulos, duplicados y valores inválidos.
    Muestra cuántas filas se eliminaron en total.

    Parámetros:
    df (DataFrame): DataFrame crudo de viajes.

    Retorna:
    DataFrame: DataFrame de Spark limpio y listo para transformar.
    """
    filas_iniciales = df.count()

    df = corregir_tipos(df, DICT_TIPOS)
    df = tratar_nulos(df, COLUMNAS_IMPUTAR)
    df = eliminar_duplicados(df)
    df = filtrar_invalidos(df)

    df = df.cache()  # cachear el df limpio para acelerar las siguientes operaciones
    filas_finales = df.count()
    eliminadas = filas_iniciales - filas_finales
    print(f"- Filas antes: {filas_iniciales:,} | después: {filas_finales:,} | "
          f"eliminadas: {eliminadas:,} ({eliminadas / filas_iniciales:.1%})")
    return df
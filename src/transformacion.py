"""
Módulo: transformacion.py
Descripción: Crea las variables derivadas y deja la tabla lista para el análisis
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""

def agregar_variables_derivadas(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a transformar.
  
    Retorna:
    DataFrame: Un DataFrame de Spark con las variables derivadas agregadas.
    """
    # Implementación de la función para agregar variables derivadas al DataFrame
    pass  # Reemplazar con la lógica de transformación

def seleccionar_columnas_relevantes(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a transformar.
    columnas_relevantes (list): Una lista de nombres de columnas que se desean mantener en el DataFrame.
  
    Retorna:
    DataFrame: Un DataFrame de Spark con solo las columnas relevantes seleccionadas.
    """
    # Implementación de la función para seleccionar solo las columnas relevantes del DataFrame
    pass  # Reemplazar con la lógica de selección

def guardar_procesado(dataframe, ruta_destino):     # guardado en parquet
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a guardar.
    ruta_destino (str): La ruta donde se guardará el archivo procesado.
  
    Retorna:
    None: Guarda el DataFrame procesado en la ruta especificada.
    """
    # Implementación de la función para guardar el DataFrame procesado en un archivo
    pass  # Reemplazar con la lógica de guardado

def transformar_datos(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a transformar.
    ruta_destino (str): La ruta donde se guardará el archivo procesado.
  
    Retorna:
    DataFrame: Un DataFrame de Spark con las transformaciones aplicadas y guardado en la ruta especificada.
    """
    # Implementación de la función para aplicar todas las transformaciones y guardar el resultado
    pass  # Reemplazar con la lógica completa de transformación
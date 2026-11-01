"""
Módulo: limpieza.py
Descripción: quita los datos erronesos y los nulos del dataset
Autor/a: <Josefina Mercado> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)

Entrada: <qué recibe el módulo>
Salida: <qué devuelve o qué archivo genera>
"""

def corregir_tipos(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a limpiar.
  
    Retorna:
    DataFrame: Un DataFrame de Spark con los tipos de datos corregidos.
    """
    # Implementación de la función para corregir los tipos de datos en el DataFrame
    pass  # Reemplazar con la lógica de corrección

def eliminar_duplicados(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a limpiar.
  
    Retorna:
    DataFrame: Un DataFrame de Spark sin filas duplicadas.
    """
    # Implementación de la función para eliminar filas duplicadas del DataFrame
    pass  # Reemplazar con la lógica de eliminación

def tratar_nulos(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a limpiar.
  
    Retorna:
    DataFrame: Un DataFrame de Spark sin valores nulos.
    """
    # Implementación de la función para tratar los valores nulos en el DataFrame
    pass  # Reemplazar con la lógica de tratamiento de nulos

def filtrar_invalidos(df):
    """
    Parámetros:
    df (DataFrame): El DataFrame de Spark que se va a limpiar.
  
    Retorna:
    DataFrame: Un DataFrame de Spark sin filas con datos inválidos.
    """
    # Implementación de la función para filtrar filas con datos inválidos
    pass  # Reemplazar con la lógica de filtrado

def resumen_limpieza(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a limpiar.
  
    Retorna:
    dict: Un diccionario con un resumen de la limpieza realizada, incluyendo el número de filas eliminadas y el número de valores nulos tratados.
    """
    # Implementación de la función para generar un resumen de la limpieza
    pass  # Reemplazar con la lógica de resumen

def limpiar_dataset(dataframe): 
    """
    Parámetros:
    dataframe (DataFrame): El DataFrame de Spark que se va a limpiar.
  
    Retorna:
    DataFrame: Un DataFrame de Spark limpio y listo para procesar.
    """
    # Implementación de la función para limpiar el dataset completo
    pass  # Reemplazar con la lógica completa de limpieza
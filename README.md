# Viajes en taxi de Nueva York — Pipeline con PySpark

**2° Desempeño — Procesamiento de Datos (ISSD)**

| Integrante | Legajo | Responsabilidad |
|---|---|---|
| Josefina Mercado | <legajo> | Carga, limpieza, transformación, e integración |
| Lucía Pellegrini | <legajo> | Análisis exploratorio con Spark |
| Santiago Mustillo | <legajo> | Modelo de MLlib y dashboard |
Grupo | persistencia en SQL
## Objetivo

[Escribir en dos o tres líneas qué responde el proyecto y qué predice el modelo.]

## Estructura del proyecto

```
main.py                  → ejecuta el pipeline completo
src/
  config.py              → rutas, URLs y parámetros
  sesion_spark.py        → crea la sesión de Spark
  carga_datos.py         → descarga y lectura de los datos
  limpieza.py            → tipos, nulos, duplicados y valores inválidos
  transformacion.py      → variables nuevas, distritos y guardado en Parquet
  eda.py                 → tablas del análisis exploratorio
  modelo.py              → modelo de regresión con MLlib
  persistencia_sql.py    → guardado y consultas en SQLite
app/dashboard.py         → dashboard en Streamlit
notebooks/eda_pellegrini.ipynb → análisis exploratorio comentado
```


**Fuente de datos:** [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), viajes en taxi amarillo de enero de 2024, más la tabla de zonas `taxi_zone_lookup.csv`.

## Requisitos

* **Python 3.12 o superior** (desarrollado con Python 3.14.6)
* **Java 17 o superior** (se usó Temurin 21). PySpark necesita Java para funcionar.
* **PySpark 4.3.0** y demás dependencias (se instalan con `requirements.txt`)

## Ejecución

### En VS Code (Windows)

1. Comprobar Java: `java -version` (17 o superior).
2. Crear y activar el entorno virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
   Si aparece "la ejecución de scripts está deshabilitada": `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
3. Instalar dependencias: `python -m pip install -r requirements.txt`
4. **Solo Windows:** para escribir archivos, Spark necesita `winutils.exe` y `hadoop.dll` en `C:\hadoop\bin`, la variable `HADOOP_HOME=C:\hadoop` y `C:\hadoop\bin` en el `Path`.
5. Ejecutar el pipeline completo desde la raíz del proyecto:
   ```powershell
   python main.py
   ```
   Genera `data/processed/taxi_limpio` (Parquet) y `data/nyc_taxi.db` (SQLite con los resultados del EDA y del modelo).
6. Abrir el dashboard (desde la terminal, no desde un notebook):
   ```powershell
   python -m streamlit run app/dashboard.py
   ```
7. El análisis exploratorio comentado está en `notebooks/eda_pellegrini.ipynb`.

### En Google Colab

Abrir `notebooks/eda_pellegrini.ipynb` con el botón "Open in Colab" y ejecutar todas las celdas. La primera celda de código clona el repositorio, instala las dependencias y ejecuta `main.py`, que descarga los datos y genera todos los resultados.
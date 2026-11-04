## Requisitos

* **Python 3.12 o superior** (desarrollado con Python 3.14.6)
* **Java 17 o superior** (se usó Temurin 21). PySpark necesita Java para funcionar.
* **PySpark 4.2.1** y demás dependencias (se instalan con `requirements.txt`)

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
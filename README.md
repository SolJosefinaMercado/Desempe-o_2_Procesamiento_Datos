## Requisitos

* **Python 3.12 o superior** (desarrollado con Python 3.14.6)
* **Java 17 o superior** (se usó Temurin 21). PySpark necesita Java para funcionar.
* **PySpark 4.2.1** y demás dependencias (se instalan con `requirements.txt`)

## Ejecución

### Opción A — Google Colab (recomendada para la corrección)

No requiere instalar nada: Colab ya incluye Python y Java.

1. Abrir `main.ipynb` en Google Colab.
2. Ejecutar todas las celdas (*Entorno de ejecución → Ejecutar todas*).

La primera celda instala las dependencias y descarga el dataset automáticamente.

### Opción B — Local (Windows / PowerShell)

**0. Desactivar Anaconda** (solo si está instalado):

```powershell
conda deactivate
```

**1. Comprobar que Java está instalado:**

```powershell
java -version
```

Debe mostrar la versión 17 o superior. Si el comando no se reconoce, Java no está instalado o falta configurar la variable de entorno `JAVA_HOME`.

**2. Crear el entorno virtual:**

```powershell
python -m venv .venv
```

> Si aparece *"no se encontró Python"*, usar el lanzador de Python para Windows:
> ```powershell
> py -m venv .venv
> ```
> Si `py` tampoco funciona, instalar Python desde [python.org](https://www.python.org/downloads/) tildando **"Add python.exe to PATH"**.

**3. Activar el entorno:**

```powershell
.\.venv\Scripts\activate
```

> Si aparece un error de *"la ejecución de scripts está deshabilitada"*, ejecutar una sola vez
**3. Instala requirements:**
python -m pip install -r requirements.txt

## Cómo ejecutar el dashboard

### 1. Generar la base de datos en Colab

Con el repositorio clonado y las dependencias instaladas, ejecutá esta celda en Colab:

```python
%cd /content/Desempe-o_2_Procesamiento_Datos
!python main.py
```

El programa genera los datos procesados en `data/processed/taxi_limpio`. Cuando termine, ejecutá esta segunda celda para contar los viajes por hora y guardar el resultado en SQLite:

```python
from pyspark.sql import SparkSession
from src import config
from src.persistencia_sql import guardar_tabla

spark = SparkSession.builder.getOrCreate()
viajes = spark.read.parquet("data/processed/taxi_limpio")

viajes_por_hora = (
    viajes.groupBy("hora")
    .count()
    .withColumnRenamed("count", "viajes")
)

guardar_tabla(viajes_por_hora.toPandas(), "viajes_por_hora", config.RUTA_DB)
```

Para enero de 2024, el mensaje esperado es `Tabla viajes_por_hora guardada, (24 filas)`.

### 2. Descargar la base de datos

En otra celda de Colab, ejecutá:

```python
from google.colab import files

files.download(str(config.RUTA_DB))
```

Colocá el archivo descargado `nyc_taxi.db` dentro de la carpeta `data` del proyecto en tu computadora. La ruta debe quedar así: `data/nyc_taxi.db`.

### 3. Abrir el dashboard

En la terminal de VS Code, desde la carpeta del proyecto y con el entorno virtual activo, ejecutá:

```powershell
python -m streamlit run app/dashboard.py
```

Abrí [http://localhost:8501/](http://localhost:8501/) en el navegador. El dashboard muestra la cantidad de viajes por hora, con un filtro de horarios, y la comparación del error de los modelos de tarifa.
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
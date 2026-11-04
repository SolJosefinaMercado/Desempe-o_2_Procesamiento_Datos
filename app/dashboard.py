"""
Módulo: dashboard.py
Descripción: Dashboard en Streamlit con la demanda por hora y la comparación de modelos de tarifa.
Autor/a: <Santiago Mustillo> — Legajo <número>
Proyecto: 2° Desempeño — Procesamiento de Datos (ISSD)
Ejecutar desde la raíz del proyecto: python -m streamlit run app/dashboard.py
"""

from pathlib import Path
import streamlit as st
from src.persistencia_sql import consultar

ruta_db = Path(__file__).resolve().parents[1] / "data" / "nyc_taxi.db"

st.title("Taxis amarillos de Nueva York")
st.subheader("Cantidad de viajes por hora de subida")

if not ruta_db.is_file():
    st.error("Falta el archivo data/nyc_taxi.db.")
    st.stop()

viajes_por_hora = consultar(
    "SELECT hora, viajes FROM viajes_por_hora ORDER BY hora",
    str(ruta_db),
)

viajes_por_hora["Hora de subida"] = viajes_por_hora["hora"].map(
    lambda hora: f"{int(hora):02d}:00"
)
desde, hasta = st.slider("Filtrar por hora de subida", 0, 23, (0, 23))

viajes_filtrados = viajes_por_hora[
    viajes_por_hora["hora"].between(desde, hasta)
]

st.bar_chart(viajes_filtrados, x="Hora de subida", y="viajes")

st.subheader("Comparación de modelos de tarifa")
st.caption("Error absoluto medio (MAE) en los mismos viajes de prueba. Menor es mejor.")

# Integración: los MAE se leen de la tabla que guarda main.py, en vez de estar escritos a mano
metricas = consultar("SELECT modelo, ROUND(mae, 2) AS mae FROM metricas_modelo", str(ruta_db))
st.table(metricas)

# Integración: la mejora se calcula con los valores de la tabla
mae = dict(zip(metricas["modelo"], metricas["mae"]))
mejora = mae["Solo distancia"] - mae["Modelo ampliado"]
st.write(f"Al sumar las nuevas variables, el MAE bajó USD {mejora:.2f} por viaje "
         f"(aprox. {mejora / mae['Solo distancia']:.1%}).")


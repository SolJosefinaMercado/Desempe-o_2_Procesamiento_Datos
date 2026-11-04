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

st.table([
    {"Modelo": "Tarifa fija", "MAE (USD)": "10,90"},
    {"Modelo": "Solo distancia", "MAE (USD)": "2,58"},
    {"Modelo": "Modelo ampliado", "MAE (USD)": "2,42"},
])

st.write("Al sumar las nuevas variables, el MAE bajó USD 0,16 por viaje (aprox. 6,2 %).")
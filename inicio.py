import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.graph_objects as go
import base64
from pathlib import Path
import os

# Establecer la configuración de la pantalla
st.set_page_config(
    page_title="Dashboard Defensa",
    layout="wide"
)

# Configuración global de métricas para evitar el truncado (...)
st.markdown("""
    <style>
    /* Permite que el texto salte de línea y no se corte */
    [data-testid="stMetricLabel"] > div {
        white-space: normal !important;
        line-height: 1.2 !important;
        overflow-wrap: break-word !important;
    }
    /* Opcional: Ajusta el contenedor para que las métricas tengan aire entre ellas */
    [data-testid="stMetric"] {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)





# Ruta de la imagen relativa al archivo actual
image_path = Path(__file__).parent / "img" / "Escudo.png"

# Codificar la imagen en base64
with open(image_path, "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode()

# Mostrar imagen fija abajo del sidebar con HTML

st.logo(f"data:image/png;base64,{encoded_image}", size="large", icon_image=f"data:image/png;base64,{encoded_image}")


# Data

ruta_base = os.path.dirname(__file__)
ruta_metadata = os.path.join(ruta_base, '.', 'data', 'base_info_jugadores.csv')
metadata = pd.read_csv(ruta_metadata, encoding='utf-8')


st.title("Dashboard Defensa")

passes = pd.read_csv("data/passes.csv",encoding="utf-8")


# Selector de jugador
jugadores = sorted(passes["player_name"].unique())
jugador = st.selectbox("Seleccioná un jugador", jugadores, index=None,placeholder="Selecciona una opción...")
st.session_state.jugador = jugador

if not jugador:
    st.info("Por favor, selecciona un jugador en el buscador para ver su perfil.")
    st.stop()

id_jugador = metadata[metadata["player_short_name"] == jugador]["player_id"].iloc[0]
st.session_state.id_jugador = id_jugador

try:

    df_metadata_jugador_tmp = metadata[metadata["player_short_name"] == jugador]
    max_season = df_metadata_jugador_tmp["season_name"].max()
    df_max_season = df_metadata_jugador_tmp[df_metadata_jugador_tmp["season_name"] == max_season]

    df_metadata_jugador = df_max_season.groupby(['player_name', 'season_name', 'player_birthdate', 'age', 'team_name', 'position_group']).agg({
        'competition_name': lambda x: ' / '.join(x.unique()),
        'minutes_full_all': 'mean',
        'count_match': 'sum',
        'count_match_failed': 'sum'
    }).reset_index().iloc[0]

    # 4. Interfaz de Usuario estilo Biografía
    st.title(f"Perfil de Jugador: {jugador}")
    st.divider()

    # Layout en columnas para la "Ficha Biográfica"

    st.subheader("Datos Personales")
    st.markdown(f"""
    **📅 Fecha de Nacimiento:** {df_metadata_jugador['player_birthdate']}

    **🎂 Edad:** {df_metadata_jugador['age']} años

    **📍 Posición:** {df_metadata_jugador['position_group']}
    """)

    st.write("")

    st.subheader("Información de Temporada")
    st.markdown(f"""
    **⚽ Equipo:** {df_metadata_jugador['team_name']}

    **🏆 Competición:** {df_metadata_jugador['competition_name']}

    **📅 Temporada:** {max_season}
    """)

    st.divider()

    # KPIs de Desempeño
    st.subheader("📊 Estadísticas Partidos")
    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(label="Minutos Totales", value=f"{df_metadata_jugador['minutes_full_all']:.2f}")
    kpi2.metric(label="Partidos Jugados", value=int(df_metadata_jugador['count_match']))
    kpi3.metric(label="Partidos Fallidos", value=int(df_metadata_jugador['count_match_failed']))

except Exception as e:
    st.info("El jugador seleccionado no tiene información asociada")
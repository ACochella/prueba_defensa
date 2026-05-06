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
import plotly.express as px

# Ruta de la imagen relativa al archivo actual
image_path = Path(__file__).parent.parent / "img" / "Escudo.png"

# Codificar la imagen en base64
with open(image_path, "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode()

#configuracion_sidebar(encoded_image)
st.logo(f"data:image/png;base64,{encoded_image}", size="large", icon_image=f"data:image/png;base64,{encoded_image}")



st.title(f"Rendimiento Físico - {st.session_state.jugador}")
st.markdown("__________")



ruta_base = os.path.dirname(__file__)
ruta_fisico = os.path.join(ruta_base, '..', 'data', 'base_fisica_jugadores.csv')
base_fisica = pd.read_csv(ruta_fisico, encoding='utf-8')


st.session_state.base_fisica = base_fisica



df_fisico_jugador = base_fisica[base_fisica["player_id"] == st.session_state.id_jugador]


col1, col2, col3, col4 = st.columns(4)

with col1:

    cols_excluidas = ['player_name', 'player_id', 'team_name', 'team_id', 'competition_name', 'competition_id', 'season_name', 'season_id']
    metricas_disponibles = [col for col in base_fisica.columns if col not in cols_excluidas]

    metricas_seleccionadas = st.sidebar.multiselect(
        "Selecciona hasta 5 métricas:",
        options=metricas_disponibles,
        max_selections=5,
        default=[])
    
with col2:

    ligas_disponibles = base_fisica['competition_name'].dropna().unique().tolist()
    default_liga = "ARG - Primera Division - 1st Phase"

    index_default = ligas_disponibles.index(default_liga) if default_liga in ligas_disponibles else 0

    liga_seleccionada = st.sidebar.selectbox(
        "Selecciona la Liga para Comparar:",
        options=ligas_disponibles,
        index=index_default
    )

with col3:

    temporadas_unicas = base_fisica[base_fisica['competition_name'] == liga_seleccionada]['season_name'].dropna().unique()
    temporadas_ordenadas = sorted(temporadas_unicas, reverse=True)

    temporada_seleccionada = st.sidebar.selectbox(
        "Selecciona la Temporada:",
        options=temporadas_ordenadas
    )

with col4:

    positions = base_fisica['position_group'].dropna().unique().tolist()

    posicion_seleccionada = st.sidebar.multiselect(
        "Selecciona la Posicion:",
        options=positions,
        max_selections=5,
        default=[])
    
# 2. Filtrar por Liga
base_fisica_comparacion = base_fisica[base_fisica['competition_name'] == liga_seleccionada]

# 3. Filtrar por Temporada
base_fisica_comparacion = base_fisica_comparacion[base_fisica_comparacion['season_name'] == temporada_seleccionada]

# 4. Filtrar por Posiciones
if posicion_seleccionada:
    base_fisica_comparacion = base_fisica_comparacion[base_fisica_comparacion['position_group'].isin(posicion_seleccionada)]

# 5. Selección de Columnas (Métricas + Info básica)
columnas_identificacion = ['player_name', 'team_name', 'position_group', 'player_id']
columnas_finales = columnas_identificacion + metricas_seleccionadas

# Solo filtramos columnas si el usuario eligió al menos una métrica
if metricas_seleccionadas:
    base_fisica_comparacion = base_fisica_comparacion[base_fisica_comparacion['player_id'] != st.session_state.id_jugador][columnas_finales]
    df_fisico_jugador = df_fisico_jugador[df_fisico_jugador["season_name"] ==df_fisico_jugador["season_name"].max()][columnas_finales]
else:
    base_fisica_comparacion = base_fisica_comparacion[base_fisica_comparacion['player_id'] != st.session_state.id_jugador][columnas_identificacion]
    df_fisico_jugador = df_fisico_jugador[df_fisico_jugador["season_name"] ==df_fisico_jugador["season_name"].max()][columnas_identificacion]





# 1. Concatenación y preparación
comparacion_con_jugador = pd.concat([base_fisica_comparacion, df_fisico_jugador])

# --- 1. Configuración de columnas dinámica ---
num_metricas = len(metricas_seleccionadas)

if num_metricas > 0:
    # Definimos la estructura de filas según tu pedido
    if num_metricas <= 2:
        filas = [num_metricas] # Una fila con 1 o 2 columnas
    elif num_metricas == 3:
        filas = [3]            # Una fila con 3 columnas
    elif num_metricas == 4:
        filas = [2, 2]         # Dos filas de 2 columnas
    elif num_metricas == 5:
        filas = [3, 2]         # Una fila de 3 y otra de 2

    # --- 2. Generación de Gráficos ---
    idx_metrica = 0
    for n_cols in filas:
        cols = st.columns(n_cols)
        for i in range(n_cols):
            if idx_metrica < num_metricas:
                metrica = metricas_seleccionadas[idx_metrica]
                
                with cols[i]:
                    # --- LÓGICA DEL GRÁFICO (Adaptada de los pasos anteriores) ---
                    
                    
                    # Identificar extremos para esta métrica
                    n_extremos = 5
                    df_sorted = comparacion_con_jugador.sort_values(metrica)
                    extremos_ids = pd.concat([df_sorted.head(n_extremos), df_sorted.tail(n_extremos)])['player_id'].unique()

                    # Grupos y Labels
                    comparacion_con_jugador['Grupo'] = comparacion_con_jugador.apply(
                        lambda x: 'Seleccionado' if x['player_id'] == st.session_state.id_jugador 
                        else ('Extremos' if x['player_id'] in extremos_ids else 'Resto'), axis=1
                    )
                    
                    comparacion_con_jugador['label'] = comparacion_con_jugador.apply(
                        lambda x: x['player_name'] if x['Grupo'] in ['Seleccionado', 'Extremos'] else "", axis=1
                    )

                    # Jitter
                    np.random.seed(42)
                    comparacion_con_jugador['y_jitter'] = np.random.uniform(-0.1, 0.1, size=len(comparacion_con_jugador))

                    # Crear Figura
                    fig = px.scatter(
                        comparacion_con_jugador, x=metrica, y="y_jitter",
                        color="Grupo", hover_name="player_name", text="label",
                        color_discrete_map={'Seleccionado': '#008000', 'Extremos': '#90EE90', 'Resto': '#D3D3D3'},
                        title=f"Distribución de {metrica}"
                    )

                    fig.update_traces(marker=dict(size=8), textposition='top center', textfont=dict(size=7))
                    fig.update_layout(
                        height=350, showlegend=False,
                        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, title=""),
                        margin=dict(l=20, r=20, t=40, b=20)
                    )

                    st.plotly_chart(fig, use_container_width=True)
                
                idx_metrica += 1
else:
    st.info("Selecciona al menos una métrica en la barra lateral")

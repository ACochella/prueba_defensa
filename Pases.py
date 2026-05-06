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

# Ruta de la imagen relativa al archivo actual
image_path = Path(__file__).parent.parent / "img" / "Escudo.png"

# Codificar la imagen en base64
with open(image_path, "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode()

#configuracion_sidebar(encoded_image)
st.logo(f"data:image/png;base64,{encoded_image}", size="large", icon_image=f"data:image/png;base64,{encoded_image}")


### Creación de cancha para gráficos ###

def dibujar_cancha(ax):
    # Límites
    ax.set_xlim(-55, 55)
    ax.set_ylim(-38, 38)

    # Bordes
    ax.plot([-55, 55], [-38, -38], color="black")
    ax.plot([-55, 55], [38, 38], color="black")
    ax.plot([-55, -55], [-38, 38], color="black")
    ax.plot([55, 55], [-38, 38], color="black")

    # Línea mitad
    ax.plot([0, 0], [-38, 38], color="black")

    # Círculo central
    centro = plt.Circle((0, 0), 9.15, color="black", fill=False)
    ax.add_patch(centro)

    # Áreas grandes
    ax.plot([-55, -55 + 16.5], [-20.16, -20.16], color="black")
    ax.plot([-55, -55 + 16.5], [20.16, 20.16], color="black")
    ax.plot([-55 + 16.5, -55 + 16.5], [-20.16, 20.16], color="black")

    ax.plot([55, 55 - 16.5], [-20.16, -20.16], color="black")
    ax.plot([55, 55 - 16.5], [20.16, 20.16], color="black")
    ax.plot([55 - 16.5, 55 - 16.5], [-20.16, 20.16], color="black")

    # Quitar ejes
    ax.axis("off")


st.title(f"Pases - {st.session_state.jugador}")
st.markdown("__________")



ruta_base = os.path.dirname(__file__)
ruta_pases = os.path.join(ruta_base, '..', 'data', 'passes.csv')
pases = pd.read_csv(ruta_pases, encoding='utf-8')

ruta_pases = os.path.join(ruta_base, '..', 'data', 'passing_option.csv')
passing_option = pd.read_csv(ruta_pases, encoding='utf-8')


st.session_state.pases = pases

st.session_state.passing_option = passing_option



# Selector de jugador
jugadores = sorted(pases["player_name"].unique())

# Filtrar jugador
df_pases_jugador = pases[pases["player_name"] == st.session_state.jugador]




# Métricas pases
total_pases = len(df_pases_jugador)
pases_completos = df_pases_jugador["pase_completado"].sum()
pases_primera = df_pases_jugador["pase_primera"][df_pases_jugador["pase_completado"]>0].sum()
pases_adelante = df_pases_jugador["pase_adelante"][df_pases_jugador["pase_completado"]>0].sum()
pase_atras_lados = df_pases_jugador["pase_atras"][df_pases_jugador["pase_completado"]>0].sum() + df_pases_jugador["pase_lados"][df_pases_jugador["pase_completado"]>0].sum()
pase_dificil = df_pases_jugador["pase_dificil"][df_pases_jugador["pase_completado"]>0].sum()
xt_pase_dificil_completado = round(df_pases_jugador["player_targeted_xthreat"][(df_pases_jugador["pase_dificil"]>0) & (df_pases_jugador["pase_completado"]>0)].mean(),3)
xt_pase_dificil_total = round(df_pases_jugador["player_targeted_xthreat"][df_pases_jugador["player_targeted_xpass_completion"] < 0.65].mean(),3)
prob_exito_pase_dificil = df_pases_jugador["player_targeted_xpass_completion"][df_pases_jugador["player_targeted_xpass_completion"] < 0.65].mean()*100
pase_peligroso = df_pases_jugador["pase_peligroso"][df_pases_jugador["pase_completado"]>0].sum()
xt_pase_peligroso_completado = round(df_pases_jugador["player_targeted_xthreat"][(df_pases_jugador["pase_peligroso"]>0) & (df_pases_jugador["pase_completado"]>0)].mean(),3)
xt_pase_peligroso_total = round(df_pases_jugador["player_targeted_xthreat"][df_pases_jugador["player_targeted_xthreat"] > 0.02].mean(),3)
prob_exito_pase_peligroso = df_pases_jugador["player_targeted_xpass_completion"][df_pases_jugador["player_targeted_xthreat"] > 0.02].mean()*100


if total_pases > 0:
    porcentaje = (pases_completos / total_pases) * 100
else:
    porcentaje = 0



st.subheader("📊 Métricas Generales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Pases Totales", total_pases)

with col2:
    st.metric("Completados", pases_completos)

with col3:
    st.metric("% Completados", f"{porcentaje:.2f}%")

with col4:
    st.metric("Pases de Primera", pases_primera)


# 🔹 DIRECCIÓN
st.subheader("🧭 Dirección de pases")

col1, col2 = st.columns(2)

with col1:
    st.metric("Hacia adelante", pases_adelante)

with col2:
    st.metric("Lado / Atrás", pase_atras_lados)


# 🔹 DIFÍCILES
st.subheader("⚡ Pases Difíciles")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Completados", pase_dificil)

with col2:
    st.metric("xT Completados", xt_pase_dificil_completado)

with col3:
    st.metric("xT Total", xt_pase_dificil_total)

with col4:
    st.metric("xPass prom.", f"{prob_exito_pase_dificil:.2f}%")


# 🔹 PELIGROSOS
st.subheader("🔥 Pases Peligrosos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Completados", pase_peligroso)

with col2:
    st.metric("xT Completados", xt_pase_peligroso_completado)

with col3:
    st.metric("xT Total", xt_pase_peligroso_total)

with col4:
    st.metric("xPass Prom.", f"{prob_exito_pase_peligroso:.2f}%")

st.divider()

st.subheader("Mapa de pases")

col1, col2 = st.columns(2)

with col1:

    fig1, ax1 = plt.subplots(figsize=(8, 6))

    dibujar_cancha(ax1)


    for _, row in df_pases_jugador.iterrows():

        # Color del pase
        color = "green" if row["pase_completado"] else "red"

        # Dibujar flecha
        ax1.annotate(
            '',
            xy=(row["x_end"], row["y_end"]),
            xytext=(row["x_start"], row["y_start"]),
            arrowprops=dict(
                arrowstyle="->",
                color=color,
                lw=1.5,
                alpha=0.8
            )
        )

    # 2. Dibujar ICONOS con Scatter (evita problemas de fuentes/emojis)
        if row["pase_peligroso"]:
            ax1.scatter(
                row["x_end"], row["y_end"] + 1.5, 
                marker='*', color='gold', s=120, edgecolors='black', zorder=5
            )

        if row["pase_dificil"]:
            # Círculo rojo con un signo '!' encima
            ax1.scatter(
                row["x_end"], row["y_end"] + 1.5, 
                marker='o', color='red', s=100, edgecolors='white', zorder=5
            )
            ax1.text(
                row["x_end"], row["y_end"] + 1.5, "!", 
                color='white', fontsize=8, ha='center', va='center', fontweight='bold', zorder=6
            )

    # --- TÍTULO Y LEYENDA MEJORADA ---

    #ax1.set_title(f"Análisis de Pases: {jugador}", fontsize=16, pad=40)

    # Creamos "objetos proxy" para la leyenda (estos no se dibujan en el mapa, solo en la leyenda)
    legend_elements = [
        Line2D([0], [0], marker='*', color='w', label='Pase Peligroso',
            markerfacecolor='gold', markersize=12, markeredgecolor='black', linestyle='None'),
        Line2D([0], [0], marker='o', color='w', label='Pase Difícil',
            markerfacecolor='red', markersize=10, markeredgecolor='white', linestyle='None'),
        Line2D([0], [0], color='green', lw=2, label='Completado'),
        Line2D([0], [0], color='red', lw=2, label='Fallido')
    ]

    # Ubicamos la leyenda fuera del gráfico
    ax1.legend(
        handles=legend_elements, 
        loc='upper center', 
        bbox_to_anchor=(0.5, 1.08),
        ncol=4,                     
        frameon=False, 
        fontsize=10
    )

    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    # Lógica de Heatmap
    x_min, x_max, y_min, y_max = -55, 55, -38, 38
    filas_y, columnas_x = 4, 5
    conteo = df_pases_jugador['start_zone'].value_counts().reindex(range(1, 21), fill_value=0)
    
    # Tu orden vertical solicitado (F order)
    heatmap_data = conteo.values.reshape((columnas_x, filas_y), order='F')

    # Dibujar Heatmap de fondo
    im = ax2.imshow(heatmap_data, extent=[x_min, x_max, y_min, y_max], cmap='YlGn', alpha=0.5, aspect='auto', zorder=0)
    
    # Dibujar líneas de cancha sobre el heatmap
    dibujar_cancha(ax2)
    
    # Cuadrícula de zonas opcional
    for x in np.linspace(x_min, x_max, columnas_x + 1):
        ax2.plot([x, x], [y_min, y_max], color="black", linestyle="--", alpha=0.1, lw=1)
    for y in np.linspace(y_min, y_max, filas_y + 1):
        ax2.plot([x_min, x_max], [y, y], color="black", linestyle="--", alpha=0.1, lw=1)

    plt.colorbar(im, ax=ax2, fraction=0.03, pad=0.04)
    ax2.set_title("Zonas de Inicio", fontsize=12, pad=10)
    
    st.pyplot(fig2)
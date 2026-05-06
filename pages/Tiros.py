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


def dibujar_media_cancha_vertical(ax):
    # Límites (vertical)
    ax.set_xlim(-38, 38)
    ax.set_ylim(0, 50)

    # Bordes
    ax.plot([-38, 38], [0, 0], color="black")
    ax.plot([-38, 38], [50, 50], color="black")
    ax.plot([-38, -38], [0, 50], color="black")
    ax.plot([38, 38], [0, 50], color="black")

    # Línea mitad
    ax.plot([-38, 38], [0, 0], color="black")

    # Círculo central (mitad)
    centro = plt.Circle((0, 0), 9.15, color="black", fill=False)
    ax.add_patch(centro)

    # Área grande
    ax.plot([-20.16, -20.16], [50, 50 - 16.5], color="black")
    ax.plot([20.16, 20.16], [50, 50 - 16.5], color="black")
    ax.plot([-20.16, 20.16], [50 - 16.5, 50 - 16.5], color="black")
        # -------------------------
    # ÁREA CHICA (5.5m)
    # -------------------------
    ax.plot([-9.16, -9.16], [50, 50 - 5.5], color="black")
    ax.plot([9.16, 9.16], [50, 50 - 5.5], color="black")
    ax.plot([-9.16, 9.16], [50 - 5.5, 50 - 5.5], color="black")

    # -------------------------
    # ARCO (portería)
    # -------------------------
    # ancho arco = 7.32 → mitad = 3.66
    ax.plot([-3.66, 3.66], [50, 50], color="black")
    # profundidad del arco
    ax.plot([-3.66, -3.66], [50, 50 + 1.5], color="black")
    ax.plot([3.66, 3.66], [50, 50 + 1.5], color="black")
    ax.plot([-3.66, 3.66], [50 + 1.5, 50 + 1.5], color="black")


    ax.axis("off")


st.title(f"Tiros - {st.session_state.jugador}")
st.markdown("__________")



ruta_base = os.path.dirname(__file__)
ruta_shots = os.path.join(ruta_base, '..', 'data', 'shots.csv')
tiros = pd.read_csv(ruta_shots, encoding='utf-8')


st.session_state.tiros = tiros



df_tiros_jugador = tiros[tiros["player_name"] == st.session_state.jugador]

total_tiros = len(df_tiros_jugador)
tiros_primera = df_tiros_jugador["tiro_primera"][df_tiros_jugador["tiro_cabeza"] == 0].sum()
tiros_cabeza = df_tiros_jugador["tiro_cabeza"].sum()
tiros_dentro_area = df_tiros_jugador["tiro_dentro_area"].sum()
goles = df_tiros_jugador["gol"].sum()


st.subheader("⚽ Tiros")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Totales", total_tiros)

with col2:
    st.metric("De Primera", tiros_primera)

with col3:
    st.metric("De Cabeza", tiros_cabeza)

with col4:
    st.metric("Dentro del Área", tiros_dentro_area)

with col5:
    st.metric("Goles", goles)


def tipo_tiro(row):
    if row["gol"] == 1:
        return "Gol"
    elif row["tiro_cabeza"] == 1:
        return "Cabeza"
    elif (row["tiro_primera"] == 1) & (row["tiro_cabeza"] == 0):
        return "Primera"
    else:
        return "Otro"

df_tiros_jugador["tipo"] = df_tiros_jugador.apply(tipo_tiro, axis=1)


# --- FIGURA ---
fig, ax = plt.subplots()
ax.set_aspect('equal')

dibujar_media_cancha_vertical(ax)

ax.set_ylim(15, 55)

# --- COLORES ---
def get_color(row):
    if row["gol"] == 1:
        return "#00ff9f"
    elif row["tiro_cabeza"] == 1:
        return "#3b82f6"
    elif row["tiro_primera"] == 1:
        return "#f59e0b"
    else:
        return "#9ca3af"


# --- DIBUJAR TIROS ---
for _, row in df_tiros_jugador.iterrows():

    color = get_color(row)

    # ROTAR coordenadas (clave para vertical)
    x = row["y_end"]
    y = row["x_end"]

    # Glow
    ax.scatter(
        x, y,
        color=color,
        s=30,
        alpha=0.08,
        zorder=2
    )

    # Punto principal
    ax.scatter(
        x, y,
        color=color,
        s=15,
        alpha=0.95,
        edgecolors='white' if row["gol"] == 1 else 'black',
        linewidth=0.8 if row["gol"] == 1 else 0.2,
        zorder=3
    )


# --- LEYENDA ---
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Gol',
           markerfacecolor='#00ff9f', markersize=8, markeredgecolor='white'),
    Line2D([0], [0], marker='o', color='w', label='Cabeza',
           markerfacecolor='#3b82f6', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Primera',
           markerfacecolor='#f59e0b', markersize=8),
    Line2D([0], [0], marker='o', color='w', label='Otro',
           markerfacecolor='#9ca3af', markersize=8),
]

ax.legend(
    handles=legend_elements,
    loc='center left',
    bbox_to_anchor=(1.02, 0.5),
    frameon=False,
    fontsize=6
)

plt.tight_layout()

# --- STREAMLIT ---
st.pyplot(fig)
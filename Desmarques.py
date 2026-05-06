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


st.title(f"Desmarques - {st.session_state.jugador}")
st.markdown("__________")



ruta_base = os.path.dirname(__file__)
ruta_desmarques = os.path.join(ruta_base, '..', 'data', 'desmarques.csv')
desmarques = pd.read_csv(ruta_desmarques, encoding='utf-8')

ruta_pases = os.path.join(ruta_base, '..', 'data', 'passing_option.csv')
passing_option = pd.read_csv(ruta_pases, encoding='utf-8')



st.session_state.desmarques = desmarques

st.session_state.passing_option = passing_option



df_desmarques_jugador = desmarques[desmarques["player_name"] == st.session_state.jugador]
df_opcion_pase_jugador = passing_option[passing_option["player_name"] == st.session_state.jugador]


ruptura_sin_opcion = df_desmarques_jugador["ruptura_sin_opcion"][df_desmarques_jugador["ruptura_sin_opcion"] == 1].sum()
ruptura_con_opcion = df_opcion_pase_jugador["desmarque_ruptura_con_opcion_pase"][df_opcion_pase_jugador["desmarque_ruptura_con_opcion_pase"] == 1].sum()
dentro_fuera = df_desmarques_jugador["desmarque_dentro_fuera"][df_desmarques_jugador["desmarque_dentro_fuera"] == 1].sum()
fuera_dentro = df_desmarques_jugador["desmarque_fuera_dentro"][df_desmarques_jugador["desmarque_fuera_dentro"] == 1].sum()
intento_pared = df_desmarques_jugador["intento_pared"][df_desmarques_jugador["intento_pared"] == 1].sum()
delante = df_desmarques_jugador["desmarque_por_delante"][df_desmarques_jugador["desmarque_por_delante"] == 1].sum()

profundidad_intentado = df_desmarques_jugador["desmarque_profundidad"][df_desmarques_jugador["desmarque_profundidad"] == 1].sum()
profundidad_completado = df_desmarques_jugador["desmarque_profundidad_completado"][df_desmarques_jugador["desmarque_profundidad_completado"] == 1].sum()
profundidad_centro_intentado = df_desmarques_jugador["desmarque_profundidad_centro"][df_desmarques_jugador["desmarque_profundidad_centro"] == 1].sum()
profundidad_centro_completado = df_desmarques_jugador["desmarque_profundidad_centro_completado"][df_desmarques_jugador["desmarque_profundidad_centro_completado"] == 1].sum()
profundidad_fuera_intentado = df_desmarques_jugador["desmarque_profundidad_fuera"][df_desmarques_jugador["desmarque_profundidad_fuera"] == 1].sum()
profundidad_fuera_completado = df_desmarques_jugador["desmarque_profundidad_fuera_completado"][df_desmarques_jugador["desmarque_profundidad_fuera_completado"] == 1].sum()

col1, col2, col3, col4,col5,col6 = st.columns(6)

with col1:
    st.metric("Desmarques Ruptura sin Opción de Pase", ruptura_sin_opcion)

with col2:
    st.metric("Desmarques Ruptura con Opción de Pase", ruptura_con_opcion)

with col3:
    st.metric("Desde dentro hacía fuera", dentro_fuera)

with col4:
    st.metric("Desde fuera hacía dentro", fuera_dentro)

with col5:
    st.metric("Intento Pared", intento_pared)

with col6:
    st.metric("Desmarques por Delante de la Pelota", delante)


col1, col2, col3, col4,col5,col6 = st.columns(6)

with col1:
    st.metric("Desmarques Profundidad Intentados", profundidad_intentado)

with col2:
    if profundidad_intentado > 0:
        porcentaje_profundidad = (profundidad_completado / profundidad_intentado)*100
    else:
        porcentaje_profundidad = 0.0
    st.metric("Desmarques Profundidad Completados", f"{porcentaje_profundidad:.2f}%")

with col3:
    st.metric("Desmarques Profundidad Centrales Intentados", profundidad_centro_intentado)

with col4:
    if profundidad_centro_intentado > 0:
        porcentaje_profundidad_centro = (profundidad_centro_completado / profundidad_centro_intentado)*100
    else:
        porcentaje_profundidad_centro = 0.0
    st.metric("Desmarques Profundidad Centrales Intentados", f"{porcentaje_profundidad_centro:.2f}%")

with col5:
    st.metric("Desmarques Profundidad Laterales Intentados", profundidad_fuera_intentado)

with col6:
    if profundidad_fuera_intentado > 0:
        porcentaje_profundidad_fuera = (profundidad_fuera_completado / profundidad_fuera_intentado) * 100
    else:
        porcentaje_profundidad_fuera = 0.0
    st.metric("Desmarques Profundidad Laterales Intentados", f"{porcentaje_profundidad_fuera:.2f}%")

st.subheader("Opción de Pase")


col1, col2 = st.columns(2)

with col1:

    tipos_desmarques = ["ruptura_sin_opcion","desmarque_ruptura_con_opcion_pase","intento_pared","desmarque_dentro_fuera","desmarque_fuera_dentro","desmarque_por_delante","desmarque_profundidad","desmarque_profundidad_completado","desmarque_profundidad_centro","desmarque_profundidad_centro_completado","desmarque_profundidad_fuera","desmarque_profundidad_fuera_completado"]

    desmarques_seleccionados = st.multiselect(
        "Seleccione Tipo de Desmarque",
        options=tipos_desmarques,
        default=[],
        format_func=lambda x: x.replace("_", " ").capitalize(),
        placeholder="Seleccione una o más opciones..."
    )

    if not desmarques_seleccionados:
        st.warning("Por favor, seleccione al menos un tipo de desmarque para visualizar.")
        st.stop()

    cols = ["x_start","x_end","y_start","y_end"] + desmarques_seleccionados

    # --- FILTRADO ---
    df_plot =pd.concat([df_desmarques_jugador, df_opcion_pase_jugador], ignore_index=True).fillna(0)[cols]

    colores_desmarques = {
        "ruptura_sin_opcion": "#3b82f6", "desmarque_ruptura_con_opcion_pase": "#10b981",               
        "intento_pared": "#f59e0b", "desmarque_dentro_fuera": "#ef4444",               
        "desmarque_fuera_dentro": "#6b7280", "desmarque_por_delante": "#8b5cf6",           
        "desmarque_profundidad": "#06b6d4", "desmarque_profundidad_completado": "#06b6d4", 
        "desmarque_profundidad_centro": "#ec4899", "desmarque_profundidad_centro_completado": "#ec4899",     
        "desmarque_profundidad_fuera": "#83f755", "desmarque_profundidad_fuera_completado": "#83f755"                 
    }

    tipos_punteados = ["desmarque_profundidad", "desmarque_profundidad_centro", "desmarque_profundidad_fuera"]

    fig1, ax1 = plt.subplots(figsize=(8, 6))
    dibujar_cancha(ax1) # Asegúrate de que esta función esté definida en tu código
    # --- DIBUJAR FLECHAS ---
    for _, row in df_plot.iterrows():
        color = None
        estilo_linea = "solid" # Para annotate se usa nombre de estilo
        orden_capa = 2  # Valor base para zorder (como se ven en el gráfico)
        
        for tipo in desmarques_seleccionados:
            if row[tipo] == 1:
                color = colores_desmarques.get(tipo, "gray")
                if tipo in tipos_punteados:
                    estilo_linea = "dotted"
                    orden_capa = 2  # Las punteadas se quedan abajo
                else:
                    estilo_linea = "solid"
                    orden_capa = 5  # Las sólidas saltan al frente y superponen a las punteadas cuando coinciden
                break
        
        if color:
            ax1.annotate(
                "",
                xy=(row["x_end"], row["y_end"]),      # Punta de la flecha
                xytext=(row["x_start"], row["y_start"]), # Inicio de la línea
                zorder=orden_capa, # Para que se superpongan
                arrowprops=dict(
                    arrowstyle="->",                 # Estilo de punta simple
                    color=color,
                    lw=2.0,
                    linestyle=estilo_linea,
                    alpha=0.9,
                    shrinkA=0,                       # No encoger al inicio
                    shrinkB=2                        # Pequeño margen al final para ver bien la punta
                )
            )

    # --- LEYENDA ARRIBA ---
    legend_elements = []
    for tipo in desmarques_seleccionados:
        color_leg = colores_desmarques.get(tipo, "gray")
        estilo_leg = ":" if tipo in tipos_punteados else "-"
        label_limpio = tipo.replace("_", " ").capitalize()
        
        legend_elements.append(
            Line2D([0], [0], color=color_leg, lw=2, linestyle=estilo_leg, label=label_limpio)
        )

    # Ajustamos la leyenda para que se distribuya en varias columnas arriba
    ax1.legend(
        handles=legend_elements,
        loc='lower center',
        bbox_to_anchor=(0.5, 1.02), # Justo encima del gráfico
        ncol=3,                     # Número de columnas para que no sea una lista infinita
        frameon=False,
        fontsize=9
    )

    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    
    # Lógica de Heatmap
    x_min, x_max, y_min, y_max = -55, 55, -38, 38
    filas_y, columnas_x = 4, 5
    conteo = df_opcion_pase_jugador['end_zone'].value_counts().reindex(range(1, 21), fill_value=0)
    
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
    ax2.set_title("Zonas de Asociación", fontsize=12, pad=10)
    
    st.pyplot(fig2)
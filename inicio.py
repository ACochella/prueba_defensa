import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import plotly.graph_objects as go

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
#image_path = Path(__file__).parent / "img" / "sports.png"

# Data




# Establecer la configuración de la pantalla
st.set_page_config(
    page_title="Comienzo",
    layout="wide"
)

# Codificar la imagen en base64
#with open(image_path, "rb") as img_file:
#    encoded_image = base64.b64encode(img_file.read()).decode()

# Mostrar imagen fija abajo del sidebar con HTML
#st.sidebar.markdown(
#    f"""
#    <style>
#        .sidebar-bottom {{
#            position: fixed;
#            bottom: 20px;
#            left: 20px;
#        }}
#    </style>
#    <div class="sidebar-bottom">
#        <img src="data:image/png;base64,{encoded_image}" width="100"/>
#    </div>
#    """,
#    unsafe_allow_html=True
#)

st.title("Dashboard Defensa")

# Carga de datos

metadata_jugadores = pd.read_csv("data/base_info_jugadores.csv",encoding="utf-8")
asistencias = pd.read_csv("data/asistencias.csv",encoding="utf-8")
desmarques = pd.read_csv("data/desmarques.csv",encoding="utf-8")
duelos = pd.read_csv("data/duelos_presiones.csv",encoding="utf-8")
intercepciones = pd.read_csv("data/intercepciones.csv",encoding="utf-8")
passes = pd.read_csv("data/passes.csv",encoding="utf-8")
passing_option = pd.read_csv("data/passing_option.csv",encoding="utf-8")
shots = pd.read_csv("data/shots.csv",encoding="utf-8")


# Selector de jugador
jugadores = sorted(passes["player_name"].unique())
jugador = st.selectbox("Seleccioná un jugador", jugadores)

# Filtrar jugador
df_pases_jugador = passes[passes["player_name"] == jugador]




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



# Métricas Tiros

df_tiros_jugador = shots[shots["player_name"] == jugador]

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


st.subheader("❌⚽ Sin pelota")

df_desmarques_jugador = desmarques[desmarques["player_name"] == jugador]
df_opcion_pase_jugador = passing_option[passing_option["player_name"] == jugador]


st.subheader("Desmarques")

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
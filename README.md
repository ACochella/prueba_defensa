# Recomendador de Jugadores ⚽

Aplicación diseñada para **directores técnicos, analistas y scouts** que buscan incorporar futbolistas o analizar perfiles de jugadores de forma detallada.  
Permite filtrar, evaluar y comparar jugadores en base a métricas específicas de su posición y rol.

🌐 **Acceso a la aplicación:** [Recomendador de Jugadores](https://recomendador-jugadores.streamlit.app/)

---

## 📌 Características principales

- **Filtros avanzados**: posición, rol, valor de mercado, edad.
- **Estadísticas específicas** según posición y rol, con percentiles y métricas destacadas.
- **Estadísticas generales** para comparaciones personalizadas.
- **Diccionario de roles y métricas** integrado.
- **Visualizaciones interactivas**: box plots, comparaciones de métricas, históricos de roles.

---

## 🚀 Guía rápida de uso

### 1. Inicio
Seleccioná:
- **Posición**: Arquero, Defensor, Mediocampista o Delantero.
- **Rol**: Según el puesto elegido.
- **Valor de mercado**: Valor del jugador informado por TransferMarkt.
- **Edad**: Rango de edad de los jugadores.

---

### 2. Estadísticas Específicas
- Visualizá métricas clave para el puesto y rol del jugador.
- Identificá en qué métricas el jugador supera el percentil 80.
- Análisis detallado mediante **box plots**:
  - Mínimo, Q1, Mediana, Q3, Máximo, Outliers.

---

### 3. Estadísticas Generales
- Compará jugadores de forma personalizada.
- Selección libre de métricas ofensivas, defensivas o de efectividad (según el puesto).
- Histórico de roles asignados a cada jugador a lo largo del tiempo.

---

## 📖 Diccionario de Roles

### Arqueros
- Arquero Equilibrado
- Arquero Trabajador
- Arquero Playmaker
- Arquero Sufridor
- Arquero Muralla

### Defensores
- Defensor Equilibrado
- Defensor Temerario
- Defensor Caudillo
- Defensor Atacante
- Defensor Regular

### Mediocampistas
- Mediocampista con Gol
- Mediocampista con Lectura de Juego
- Mediocampista Box to Box
- Mediocampista Recuperador
- Mediocampista Pasador
- Mediocampista Enganche

### Delanteros
- Delantero Killer
- Delantero Mediapunta
- Delantero Generador de Peligro
- Delantero Faro del Área
- Delantero Extremo

Para el detalle completo, consultar la sección **Diccionario de Roles** en la Guía de Uso.

---

## 📊 Diccionario de Métricas

La aplicación incluye métricas por 90 minutos (`_90s`), métricas porcentuales (`perc_`) y métricas acumulativas.  
Ejemplos:
- **Ofensivas**: `goals_90s`, `xG_90s`, `assists_90s`, `key_passes_90s`.
- **Defensivas**: `tackles_won_90s`, `interceptions_90s`, `blocks_90s`.
- **Arqueros**: `saves_90s`, `clean_sheets`, `passes_over_45m_completed_90s`.

Para el detalle completo, consultar la sección **Diccionario de Métricas** en la Guía de Uso.

---

## 📂 Fuente de datos

- [FBref](https://fbref.com/)
- [Transfermarkt](https://www.transfermarkt.com/)

Ligas: Alemania, España, Francia, Inglaterra, Italia.
import streamlit as st
import pandas as pd
from visualizaciones import render_visualizaciones
from mapa import render_mapa
from animaciones import render_animaciones
from stats_jugador import render_stats_jugador
from stats_por_anio import render_stats_anuales
from stats import render_stats
from rankings import render_rankings

# CONFIGURACIÓN DE LA PÁGINA 
st.set_page_config(
    page_title="Dashboard de Fútbol - Proyecto Final", 
    layout="wide",
)

# DEFINICIÓN DE LA PALETA DE COLORES
custom_colors = ['#faeba7', '#95e0cf', '#3a787c', '#0f202a']
bg_color = custom_colors[0]       
accent_light = custom_colors[1]   
accent_dark = custom_colors[2]    
text_color = custom_colors[3]     

# ESTILOS CSS GLOBALES
st.markdown(f"""
    <style>
    /* Header */
    .stAppHeader {{
        background-color: {text_color};
        color: {bg_color};
    }}
    
    .stAppHeader a span {{
        color: {bg_color};
    }}
    
    .stAppHeader a span div p {{
        color: {bg_color};
        font-size: 14px;
    }}
    
    div[data-testid="stMarkdownContainer"] p {{
        color: {text_color};
    }}

    </style>
    """, unsafe_allow_html=True)


     

# CARGA DE DATASETS 
@st.cache_data
def cargar_datos():
    df_stats = pd.read_parquet("Datasets/top5_players_stats.parquet")
    df_valuations = pd.read_parquet("Datasets/top5_valuations.parquet")
    df_transfers = pd.read_parquet("Datasets/top5_transfers.parquet")
    
    return df_stats, df_valuations, df_transfers

df_stats, df_valuations, df_transfers = cargar_datos()

posiciones = {
    'Goalkeeper': 'Portero',
    'Defender': 'Defensa',
    'Midfield': 'Mediocampista',
    'Attack': 'Atacante',
}

roles = {
    'Offense': 'Ataque',
    'Defense': 'Defensa'
}

df_stats['main_position'] = df_stats['main_position'].replace(posiciones)
df_stats['role'] = df_stats['role'].replace(roles)


minutos_minimos = st.slider(
    "Filtro: Minutos mínimos jugados", 
    min_value=0, 
    max_value=3600, 
    value=900, 
    step=100,
    help="Filtra a los jugadores para evitar promedios engañosos de aquellos con pocos minutos.",
    key='filtro_visualizaciones'
) 

df_filtrado = df_stats[df_stats['Playing Time_Min'] >= minutos_minimos]

def inicio():
    st.title("Análisis Integrado del Mercado y Rendimiento Futbolístico")
    st.markdown(f"### *Proyecto Final — Herramientas Enfocadas a la Ciencia de Datos*")
    
    st.markdown(f"""
    **Autor:** Samuel Iván Sánchez Salazar   
    """)
        
    st.header("Introducción al Proyecto")
    st.write("""
    El fútbol moderno ha evolucionado profundamente: la llegada del **Big Data** y las estadísticas avanzadas 
    ha transformado por completo la manera en la que analizamos, comparamos y valoramos a los jugadores en la actualidad.

    Este proyecto fue diseñado para explorar la fascinante intersección entre el rendimiento de los futbolistas dentro 
    del campo y las cifras millonarias que mueven en el mercado de transferencias. A lo largo de este dashboard, 
    comparamos el panorama de las **5 grandes ligas de Europa** (Premier League, LaLiga, Serie A, Bundesliga y Ligue 1) 
    a través de distintas temporadas.

    Por medio de **gráficas interactivas y filtros dinámicos**, buscamos descubrir qué jugadores sobresalen en diferentes 
    aspectos del juego, observar cómo las métricas avanzadas se relacionan con los cambios en sus valuaciones 
    económicas y, sobre todo, visualizar cómo el análisis de datos está cambiando las reglas para entender este deporte.
    """)
    
    st.header("Fuentes de Datos")
    st.write("Para cumplir con los requerimientos de pluralidad de fuentes, se integraron los siguientes repositorios reales:")
    
    col_source1, col_source2 = st.columns(2)
    with col_source1:
        st.markdown("#### 1. Rendimiento Táctico Avanzado")
        st.write("Estadísticas detalladas recolectadas vía _FBref_ (goles esperados, toques, pases progresivos y conducciones).")
        st.link_button("Ver Fuente en Kaggle", "https://www.kaggle.com/datasets/emrey3lmaz/top-5-league-football-player-stats-2017-2025")
        
    with col_source2:
        st.markdown("#### 2. Valores Históricos de Mercado")
        st.write("Historial detallado de cotizaciones, tasaciones económicas y transferencias oficiales europeas de los jugadores, según datos de _Transfermakt_.")
        st.link_button("Ver Fuente en Kaggle", "https://www.kaggle.com/datasets/davidcariboo/player-scores")


def metodologia():
    st.title("Metodología y Arquitectura de Datos")
    st.write("El proceso de Extracción, Transformación y Carga (ETL) fue documentado y ajustado meticulosamente para garantizar la calidad y coherencia del análisis.")
    
    st.header("Pipeline de Limpieza y Unión de Tablas")
    st.write("La preparación de la información estructurada se dividió en cuatro fases críticas de ingeniería de datos:")
    
    paso1, paso2, paso3, paso4 = st.columns(4)
    
    with paso1:
        st.write("""
                1. **Reducción y Estandarización Inicial:**
                    - El dataset de rendimiento táctico (FBref) fue filtrado para conservar únicamente las **62 columnas** más representativas.
                    - Se creó una columna `main_position` tomando solo la primera posición registrada en FBref.
                    - **Normalización de Texto:** Para asegurar cruces exactos, los nombres de los jugadores (`player` en FBref y `name` en Transfermarkt) se transformaron a minúsculas, eliminando caracteres especiales y acentos.
                    - Del lado de Transfermarkt, se extrajo específicamente el **año de nacimiento** del jugador.
                """)
        
    with paso2: 
        st.write(""" 
                2. **Unión Base (Merge con Llave Compuesta):**
                    - Se realizó la unión de los datasets utilizando una llave lógica de tres variables: **nombre estandarizado, año de nacimiento y posición**. 
                    - Una vez hecho el merge, se extrajeron atributos clave de Transfermarkt: el `player_id`, la nacionalidad (`country_of_citizenship`) y la estatura (`height_in_cm`).
                    - Se descartaron los registros donde el `player_id` resultó nulo para evitar inconsistencias cruzadas.
                """)
        
    with paso3:
        st.write("""
                3. **Integración Económica Temporal:**
                    - Los datasets auxiliares de finanzas (`valuations` y `transfers`) fueron acotados temporalmente al marco de **2017 a 2025**.
                    - Usando el `player_id` recuperado en el paso anterior, se cruzó la información para añadir dos métricas vitales por temporada: el **valor de mercado promedio** y el **valor de mercado máximo**.
                """)
    with paso4:
        st.write("""
                4. **Persistencia Optimizada (Parquet):**
                    - Para mantener estrictamente el tipado de los datos y evitar corrupciones de lectura típicas de los archivos `.csv`, todas las transformaciones fueron guardadas y exportadas en formato **Parquet**.
                """)
    
    st.header("Código Fuente y Repositorio")
    st.write("Revisa el histórico del proyecto, archivos Parquet de muestra y requerimientos. Puedes ver el cuaderno de trabajo con las operaciones vectorizadas y expresiones regulares de limpieza aquí:")
    st.link_button("Ir a GitHub", "https://github.com/SamuelSanchez03/Top5FootballLeaguesDashboard.git")

def analisis_visual():
    render_visualizaciones(df_filtrado, df_valuations, df_transfers)
    
def rankings():
    render_rankings(df_filtrado)
    
def stats_jugador():
    render_stats_jugador(df_filtrado)
    
def stats_por_anio():
    render_stats_anuales(df_filtrado)
    
def stats():
    render_stats(df_filtrado)

def animaciones():
    render_animaciones()
    
def mapa():
    render_mapa(df_filtrado)

def conclusiones():
    st.title("Conclusiones del Proyecto")
    st.header("Hallazgos Principales")
    st.write("""
    Tras analizar la intersección entre el rendimiento en la cancha y el impacto financiero, podemos destacar las siguientes conclusiones clave:

    * **El mito de la métrica única:** No existe una sola estadística (ni siquiera los goles o las asistencias) que dicte por sí sola el valor de mercado de un jugador. Las valuaciones son multifactoriales.
    * **La trinidad del valor en el mercado:** Lo que parece influir de manera más determinante en el precio de un futbolista es la combinación de **Liga, Edad y Posición**. El perfil más cotizado en la actualidad corresponde a jugadores jóvenes en posiciones de ataque que militan en la Premier League (siempre y cuando mantengan un nivel estadístico sólido que aporte al equipo).
    * **La hegemonía de la Premier League:** Si bien es la liga con las valuaciones más altas e infladas, los datos demuestran que esta superioridad económica está respaldada por el rendimiento; en general, sus jugadores suelen registrar mejores estadísticas globales que el promedio del resto de las 5 grandes ligas.
    * **El "Impuesto del Atacante":** Los delanteros y extremos siguen siendo los activos más caros del fútbol. Esto se justifica en que sus aportaciones estadísticas (goles, xG, asistencias) son las que contribuyen de manera más directa a la obtención de puntos para sus equipos.
    * **El peso del Big Data y las métricas avanzadas:** Se hace evidente una evolución en el análisis deportivo. Gracias a las estadísticas avanzadas, hoy es posible identificar "jugadores invisibles" o perfiles con roles específicos (creación, progresión, recuperación) que contribuyen de formas complejas al estilo táctico y a los resultados, sin necesidad de figurar en la tabla de goleadores.
    """)

    st.header("Valor Agregado de la Unión de Datos")
    st.write("""
    El verdadero impacto de este proyecto radica en el esfuerzo técnico y analítico de realizar el *merge* de dos universos de datos masivos que normalmente se estudian por separado: **el rendimiento deportivo profundo (FBref) y la economía del fútbol (Transfermarkt)**. 

    Al limpiar, estandarizar y unir estos conjuntos de datos, logramos transformar números aislados en **inteligencia deportiva y financiera**. Esto nos permitió pasar de preguntas descriptivas simples ("¿quién es el máximo goleador?") a resolver preguntas de negocio complejas, tales como evaluar si el rendimiento real de un jugador justifica los millones que cuesta o entender qué ligas pagan mejor ciertas habilidades específicas. 
    """)

    st.header("Reflexión Final")
    st.info("""
    A pesar del inmenso poder de las estadísticas avanzadas para identificar talento y evaluar el rendimiento, el fútbol conserva su factor humano y caótico. Existen variables intangibles —como la química del vestuario, la fortaleza mental, la capacidad de adaptación o incluso la suerte— que nos demuestran que **el deporte no puede explicarse ni predecirse con un 100% de certeza matemática**. Los datos son la mejor brújula para mitigar el riesgo en la toma de decisiones, pero el fútbol seguirá siendo, en esencia, impredecible.
    """)
    
pages = [
    st.Page(inicio, title="Inicio", icon=":material/home:"),
    st.Page(metodologia, title="Metodología", icon=":material/engineering:"),
    st.Page(analisis_visual, title="Análisis Visual", icon=":material/analytics:"),
    st.Page(rankings, title="Rankings", icon=":material/leaderboard:"),
    st.Page(stats_jugador, title="Stats Jugador", icon=":material/shoe_cleats:"),
    st.Page(stats_por_anio, title="Stats Por Año", icon=":material/calendar_month:"),
    st.Page(stats, title="Stats de Desempeño", icon=":material/show_chart:"),
    st.Page(mapa, title="Mapa", icon=":material/map:"),
    st.Page(animaciones, title="Bar Races", icon=":material/play_circle:"),
    st.Page(conclusiones, title="Conclusiones", icon=":material/inventory:")
]

# 3. Handle navigation and force it to the top bar
current_page = st.navigation(pages, position="top")

# 4. Execute the chosen page
current_page.run()
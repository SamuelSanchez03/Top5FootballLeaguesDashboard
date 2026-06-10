import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- PALETA DE COLORES ---
custom_colors = ['#faeba7', '#95e0cf', '#3a787c', '#0f202a']
bg_color = custom_colors[0]    
secondary_color = custom_colors[1] 
primary_color = custom_colors[2]   
text_color = custom_colors[3]      

plt.rcParams.update({
    'figure.facecolor': bg_color,
    'axes.facecolor': bg_color,
    'text.color': text_color,
    'axes.labelcolor': text_color,
    'xtick.color': text_color,
    'ytick.color': text_color,
    'axes.edgecolor': text_color,
    'grid.color': primary_color,
    'grid.alpha': 0.1
})

line_colors = [custom_colors[2], custom_colors[1], custom_colors[3]]
sns.set_palette(sns.color_palette(line_colors))

def render_stats_anuales(df_filtrado):
    st.title("Evolución de Estadísticas por Año")
    
    nombres_espanol = {
        'league': 'Liga',
        'main_position': 'Posición Principal',
        'year': 'Año',
        'age_': 'Edad',
        'Playing Time_Min': 'Minutos Jugados',
        'Playing Time_90s': 'Partidos Completos (90s)',
        'Performance_Gls': 'Goles',
        'Performance_Ast': 'Asistencias',
        'Performance_G+A': 'Goles y Asistencias',
        'Performance_PK': 'Goles de Penal',
        'Performance_Fld': 'Faltas Recibidas',
        'Performance_Fls': 'Faltas Cometidas',
        'Performance_Int': 'Intercepciones',
        'Performance_Off': 'Fueras de Juego',
        'Performance_Recov': 'Recuperaciones',
        'Performance_TklW': 'Entradas Ganadas',
        'Tackles_Att 3rd': 'Entradas (Último Tercio)',
        'Expected_xG': 'Goles Esperados (xG)',
        'Expected_npxG': 'Goles Esperados sin Penales (npxG)',
        'Expected_xAG': 'Asistencias Esperadas (xAG)',
        'Expected_xA': 'Asistencias Esperadas Tradicionales (xA)',
        'Expected_G-xG': 'Diferencia Goles - xG',
        'Progression_PrgC': 'Conducciones Progresivas',
        'Progression_PrgP': 'Pases Progresivos',
        'Progression_PrgR': 'Pases Progresivos Recibidos',
        'Per 90 Minutes_Gls': 'Goles por 90 min',
        'Per 90 Minutes_Ast': 'Asistencias por 90 min',
        'Per 90 Minutes_G+A': 'Goles y Asistencias por 90 min',
        'Per 90 Minutes_xG': 'xG por 90 min',
        'Per 90 Minutes_xAG': 'xAG por 90 min',
        'Per 90 Minutes_npxG': 'npxG por 90 min',
        'Standard_SoT%': '% Tiros a Puerta',
        'Standard_Sh/90': 'Tiros por 90 min',
        'Standard_G/Sh': 'Goles por Tiro',
        'KP_': 'Pases Clave',
        'PrgP_': 'Pases Progresivos Totales',
        '1/3_': 'Pases al Último Tercio',
        'Pass Types_Tage_B': 'Pases Filtrados',
        'Total_Att': 'Pases Intentados',
        'Total_Cmp%': '% Pases Completados',
        'Long_Cmp%': '% Pases Largos Completados',
        'Medium_Cmp%': '% Pases Medios Completados',
        'Short_Cmp%': '% Pases Cortos Completados',
        'SCA_SCA90': 'Acciones de Creación de Tiro por 90 min',
        'GCA_GCA90': 'Acciones de Creación de Gol por 90 min',
        'Err_': 'Errores que llevan a Tiro',
        'Blocks_Blocks': 'Bloqueos',
        'Take-Ons_Att': 'Regates Intentados',
        'Take-Ons_Succ%': '% Regates Exitosos',
        'Carries_Carries': 'Conducciones',
        'Carries_PrgC': 'Conducciones Progresivas Totales',
        'Carries_Dis': 'Desposesiones',
        'Touches_Touches': 'Toques',
        'Touches_Att Pen': 'Toques en Área Penal Rival',
        'Aerial Duels_Won': 'Duelos Aéreos Ganados',
        'Aerial Duels_Won%': '% Duelos Aéreos Ganados',
        'Team Success_PPM': 'Puntos por Partido (PPM)',
        'Team Success_+/-90': 'Diferencia de Goles por 90 min',
        'height_in_cm': 'Estatura (cm)',
        'mean_market_value_in_eur': 'Valor de Mercado Promedio (M€)',
        'max_market_value_in_eur': 'Valor de Mercado Máximo (M€)'
    }

    # Aplicar el cambio al dataframe
    df_filtrado.rename(columns=nombres_espanol, inplace=True)
    df_filtrado['Valor de Mercado Promedio (M€)'] = df_filtrado['Valor de Mercado Promedio (M€)'] / 1_000_000
    df_filtrado['Valor de Mercado Máximo (M€)'] = df_filtrado['Valor de Mercado Máximo (M€)'] / 1_000_000

    # Filtrar solo las columnas numéricas para las estadísticas (excluyendo identificadores y años)
    columnas_excluidas = ['Liga', 'season', 'team', 'player', 'Posición Principal', 'role', 
                        'player_id', 'country_of_citizenship', 'Año', 'image_url']
    columnas_estadisticas = [col for col in df_filtrado.columns if col not in columnas_excluidas]


    col_grafico_1, col_grafico_2 = st.columns(2)

    with col_grafico_1:
        stat_seleccionada = st.selectbox("Selecciona la estadística a analizar:", columnas_estadisticas)

    with col_grafico_2:
        agrupacion = st.selectbox("Agrupar por:", ["Liga", "Posición Principal"])

    # Calcular el promedio agrupado por año y la variable seleccionada
    df_agrupado = df_filtrado.groupby(['Año', agrupacion])[stat_seleccionada].mean().reset_index()

    # Crear el gráfico con Seaborn
    fig, ax = plt.subplots(figsize=(12, 10), dpi=1000)
    sns.lineplot(data=df_agrupado, x='Año', y=stat_seleccionada, hue=agrupacion, marker='o', ax=ax)

    ax.set_title(f"Evolución de {stat_seleccionada} por {agrupacion}", fontsize=14)
    ax.set_xlabel("Año")
    ax.set_ylabel(f"Promedio de {stat_seleccionada}")
    ax.grid(True, linestyle='--', alpha=0.7)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig, width='content')
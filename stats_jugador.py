import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

def render_stats_jugador(df_stats):
    st.title("Perfil del Jugador por Temporada")

    col_jug_1, col_jug_2 = st.columns(2)

    with col_jug_1:
        # Filtrar jugadores por id
        # Ordenar los jugadores alfabéticamente para facilitar la búsqueda
        ids = df_stats.drop_duplicates(subset=['player_id'])[['player_id', 'player']]
        ids = ids.sort_values('player')
        nombres_dict = ids.set_index('player_id')['player'].to_dict()

        jugador_id_seleccionado = st.selectbox(
            "Selecciona un jugador:",
            options=nombres_dict.keys(), 
            format_func=lambda x: f"{nombres_dict[x]} ({int(x)})" 
        )
                
    with col_jug_2:
        # Filtrar las temporadas disponibles solo para el jugador seleccionado
        temporadas_disponibles = df_stats[df_stats['player_id'] == jugador_id_seleccionado]['season'].unique()
        temporadas_ordenadas = sorted(temporadas_disponibles, reverse=True)
        temporadas_ordenadas = [str(t)[:2]+ "/" + str(t)[2:] for t in temporadas_ordenadas]
        temporada_seleccionada = st.selectbox("Selecciona una Temporada:", temporadas_ordenadas)

    # Filtrar los datos para el jugador y temporada seleccionados
    df_jugador = df_stats[(df_stats['player_id'] == jugador_id_seleccionado) & 
                            (df_stats['season'] == int(temporada_seleccionada.replace('/', '')))]

    if not df_jugador.empty:
        datos_jugador = df_jugador.iloc[0]
        
        st.header(f"Estadísticas de {df_stats[df_stats['player_id'] == jugador_id_seleccionado]['player'].unique()[0]} ({temporada_seleccionada})")
        
        col_foto, col_texto = st.columns([1, 8])
        
        with col_foto:
            if pd.notna(datos_jugador['image_url']):
                st.image(datos_jugador['image_url'], width=130)
            else:
                # Imagen por defecto en caso de que no tenga foto disponible
                st.image("https://via.placeholder.com/120x150?text=Sin+Foto", width=130)
                
        with col_texto:
            st.write("") 
            st.write(f"**Equipo:** {datos_jugador['team']}")
            st.write(f"**Liga:** {datos_jugador['league']}")
            st.write(f"**Posición:** {datos_jugador['main_position']} | **Rol:** {datos_jugador['role']}")
            st.write(f"**Edad:** {datos_jugador['age_'].astype(int)} años | **Estatura:** {datos_jugador['height_in_cm'].astype(int)} cm")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Minutos Jugados", f"{datos_jugador['Playing Time_Min']:,.0f}")
        m2.metric("Goles", datos_jugador['Performance_Gls'])
        m3.metric("Asistencias", datos_jugador['Performance_Ast'])
        m4.metric("Goles + Asistencias", datos_jugador['Performance_G+A'])
        
        m5, m6, m7, m8 = st.columns(4)
        m5.metric("Goles Esperados (xG)", round(datos_jugador['Expected_xG'], 2))
        m6.metric("Asistencias Esperadas (xAG)", round(datos_jugador['Expected_xAG'], 2))
        m7.metric("Disparos / 90min", round(datos_jugador['Standard_Sh/90'], 2))
        if pd.notna(datos_jugador['mean_market_value_in_eur']):
            m8.metric("Valor Mercado Promedio", f"€{datos_jugador['mean_market_value_in_eur']:,.0f}")
        else:
            m8.metric("Valor Mercado Promedio", "N/A")
            
        m9, m10, m11, m12 = st.columns(4)
        m9.metric("Porcentaje de Pases Completados", f"{datos_jugador['Total_Cmp%']:,.0f}%")
        m10.metric("Puntos por Partido", datos_jugador['Team Success_PPM'])
        m11.metric("Recuperaciones", datos_jugador['Performance_Recov'].astype(int))
        m12.metric("Conducciones Progresivas", datos_jugador['Progression_PrgC'])
            
    else:
        st.warning("No se encontraron datos para este jugador en la temporada seleccionada.")
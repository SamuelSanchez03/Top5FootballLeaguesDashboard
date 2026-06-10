import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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

def id_a_nombre(ids, df, stat):
    # Convertir la Serie a DataFrame y resetear el índice
    df_id = ids.reset_index()
    df_id.columns = ['player_id', stat]

    # Seleccionamos solo el 'player_id' y el nombre de df_players
    df_resultado = pd.merge(df_id, df[['player_id', 'player']], on='player_id', how='inner')

    df_sin_duplicados = df_resultado.drop_duplicates(subset=['player_id'], keep='first')

    # Extraer ÚNICAMENTE la columna de los nombres
    return df_sin_duplicados['player'] 

def reemplazar_id_por_nombre(ids, df):
    mapa_nombres = df.drop_duplicates(subset=['player_id']).set_index('player_id')['player'].to_dict()
    
    # Renombrar los valores 'player_id' del índice
    serie_resultado = ids.rename(index=mapa_nombres, level='player_id')
    
    # Actualizar los nombres de los niveles del MultiIndex para reflejar el cambio
    serie_resultado.index.names = ['player', 'season']
    
    return serie_resultado

def render_rankings(df_filtrado):
    st.title("Rankings Destacados (Top 10)")
    col5, col6 = st.columns(2)

    # Ranking Goles + Asistencias
    with col5:
        top_10_ga = df_filtrado[['player_id', 'player', 'Performance_G+A']].groupby('player_id')['Performance_G+A'].sum().nlargest(10).sort_values(ascending=True)
    
        nombres_ordenados = id_a_nombre(top_10_ga, df_filtrado, 'Goles_Asistencias')

        fig5, ax5 = plt.subplots(figsize=(8, 6))
        ax5.barh(nombres_ordenados, np.array(top_10_ga.values, dtype=np.int64), color=primary_color)
        ax5.set_title('Top 10 Histórico: Goles + Asistencias')
        ax5.set_xlabel('Total G+A')
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        
        st.pyplot(fig5)

    # Ranking Minutos Veteranos (Jugadores > 33 años, sin porteros)
    with col6:
        df_campo = df_filtrado[(df_filtrado['main_position'] != 'Goalkeeper') & (df_filtrado['age_']> 33)].copy()

        lideres_minutos = df_campo.groupby(['player_id', 'season'])['Playing Time_Min'].max().nlargest(10).sort_values(ascending=True)

        minutos_con_nombres = reemplazar_id_por_nombre(lideres_minutos, df_campo)
        
        fig6, ax6 = plt.subplots(figsize=(8, 6))
        ax6.barh(
            [f"{idx[0]} ({str(idx[1])[:2]}/{str(idx[1])[2:]})" for idx in minutos_con_nombres.index], 
            lideres_minutos.values, 
            color=primary_color, 
            edgecolor=bg_color
        )
        
        ax6.set_title('Top 10 Jugadores con más Minutos (>30 años y Excl. Porteros)')
        ax6.set_xlabel('Minutos Jugados')
        ax6.spines['top'].set_visible(False)
        ax6.spines['right'].set_visible(False)
        st.pyplot(fig6)

    col7, col8 = st.columns(2)

    # Ranking de Jugadores con "Suerte" (Goles Reales vs Goles Esperados)
    with col7:
        
        lideres_suerte = df_filtrado.groupby(['player_id', 'season'])['Expected_G-xG'].max().nlargest(10).sort_values(ascending=True)

        suerte_con_nombres = reemplazar_id_por_nombre(lideres_suerte, df_filtrado)
        
        fig7, ax7 = plt.subplots(figsize=(8, 6))
        ax7.barh(
            [f"{idx[0]} ({str(idx[1])[:2]}/{str(idx[1])[2:]})" for idx in suerte_con_nombres.index], 
            lideres_suerte.values, 
            color=primary_color, 
            edgecolor=bg_color
        )       
        ax7.set_title("Top 10: Mayor Efectividad / Suerte (G - xG)")
        ax7.set_xlabel("Diferencia Goles vs xG")
        ax7.spines['top'].set_visible(False)
        ax7.spines['right'].set_visible(False)
        st.pyplot(fig7)

    # Ranking Mejor % Pases (Filtro: mínimo 500 pases intentados y 100 pases progresivos)
    with col8:
        # Filtro de pases para no incluir jugadores con 1 pase y 100% efectividad
        min_pases = 500
        min_pases_prog = 200
        filtro_pases = df_filtrado[(df_filtrado['Total_Att'] >= min_pases) & (df_filtrado['PrgP_'] >= min_pases_prog)]
        
        lideres_pases = filtro_pases.groupby(['player_id', 'season'])['Total_Cmp%'].max().nlargest(10).sort_values(ascending=True)

        pases_con_nombres = reemplazar_id_por_nombre(lideres_pases, filtro_pases)
        
        fig8, ax8 = plt.subplots(figsize=(8, 6))
        ax8.barh(
            [f"{idx[0]} ({str(idx[1])[:2]}/{str(idx[1])[2:]})" for idx in pases_con_nombres.index], 
            lideres_pases.values, 
            color=primary_color, 
            edgecolor=bg_color
        )  
        ax8.set_title(f"Top 10: % Pases Completados (Min. {min_pases} int. y {min_pases_prog} pases prog.)")
        ax8.set_xlabel("Porcentaje de Completados (%)")
        ax8.set_xlim(min(lideres_pases.values)-5, 100) # Ajustar el zoom del eje X
        ax8.spines['top'].set_visible(False)
        ax8.spines['right'].set_visible(False)
        st.pyplot(fig8)
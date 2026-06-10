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

def render_visualizaciones(df_filtrado, df_valuations, df_transfers):
    st.title("Datos Generales")

    st.header("Métricas Clave")
    total_jugadores = df_filtrado['player_id'].nunique()
    
    valor_promedio = df_filtrado['mean_market_value_in_eur'].mean()
    edad_promedio = df_filtrado['age_'].mean()
    total_equipos = df_filtrado['team'].nunique()
    total_nacionalidades = df_filtrado['country_of_citizenship'].nunique()
    total_temporadas = df_filtrado['season'].nunique()

    met1, met2, met3 = st.columns(3)
    
    with met1:
        st.metric(label="Jugadores Únicos", value=f"{total_jugadores:,}")
        st.metric(label="Número de Temporadas", value=f"{total_temporadas} temporadas")
        
    with met2:
        st.metric(label="Valor Mercado Promedio", value=f"€{valor_promedio/1e6:.1f}M")
        st.metric(label="Número de Nacionalidades", value=f"{total_nacionalidades} países")
        
    with met3:
        st.metric(label="Edad Promedio", value=f"{edad_promedio:.1f} años")
        st.metric(label="Número de Equipos", value=f"{total_equipos} equipos")
    
    st.header("Distribuciones")
    col1, col2 = st.columns(2)
    
    # Distribución de Edades
    with col1:        
        fig1, ax1 = plt.subplots(figsize=(12, 8))
        ax1.hist(df_filtrado['age_'].dropna(), bins=range(14, 44), color=primary_color, edgecolor=bg_color, align='left')

        ax1.set_title('Distribución de Edades')
        ax1.set_xlabel('Edad')
        ax1.set_ylabel('Cantidad de Jugadores')

        ax1.set_xticks(range(14, 43)) 
        ax1.set_xlim(13, 43)
        st.pyplot(fig1)


    # Distribución de Posiciones
    with col2:
        pos_counts = df_filtrado['main_position'].value_counts()
    
        pie_colors = [primary_color, secondary_color, '#6e9b9d', '#b5d5c5', '#1a3c40']
        
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        ax2.pie(
            pos_counts.values, 
            labels=pos_counts.index, 
            colors=pie_colors, 
            autopct='%1.1f%%', # Muestra el porcentaje
            startangle=90, 
            textprops={'color': text_color, 'fontsize': 10},
            wedgeprops={'edgecolor': bg_color, 'linewidth': 1.5}
        )
        ax2.set_title('Distribución de Jugadores por Posición')
        
        st.pyplot(fig2, width='content')

    col3, col4 = st.columns(2)
    
    # Distribución de Valor de Mercado
    with col3:
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.hist(df_filtrado['mean_market_value_in_eur'], bins=20, range=(0, 100_000_000), 
                 color=primary_color, edgecolor=bg_color)
        ax3.set_title("Distribución Valor de Mercado")
        ax3.set_xlabel("Valor en Euros")
        ax3.set_ylabel("Cantidad de Jugadores")
        ax3.set_xlim(0, 100_000_000)
        ax3.set_xticks(range(0, 101_000_000, 10_000_000)) 
        ax3.set_yticks(range(0, 4501, 500)) 
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x/1000}k'))
        ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'€{x/1e6:.0f}M'))
        st.pyplot(fig3)

    # Distribución de Valor de Mercado por Edad
    with col4:
        fig4, ax4 = plt.subplots(figsize=(12, 8))
        val_edad = df_filtrado.groupby('age_')['mean_market_value_in_eur'].mean().reset_index()
        ax4.bar(val_edad['age_'], val_edad['mean_market_value_in_eur'], color=primary_color)
        ax4.set_title("Valor de Mercado Promedio por Edad")
        ax4.set_xlabel("Edad")
        ax4.set_ylabel("Valor Promedio (Euros)")
        ax4.set_xticks(range(14, 43)) 
        ax4.set_xlim(13, 43)
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'€{x/1e6:.0f}M'))
        
        
        st.pyplot(fig4)
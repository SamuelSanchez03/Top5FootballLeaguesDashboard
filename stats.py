import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from adjustText import adjust_text

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
    'grid.alpha': 0.1,
    'figure.autolayout': True 
})

def get_jugadores_interesantes(df, x_col, y_col, criterio, n=5):
    df_clean = df[[x_col, y_col, 'player', 'player_id', 'season']].dropna().copy()
    df_clean = df_clean.drop_duplicates(subset=['player', 'player_id', 'season'])

    if criterio == 'alto_y_bajo_x':
        # Normalizar ambos ejes y buscar alto Y, bajo X
        df_clean['score'] = (
            (df_clean[y_col] - df_clean[y_col].min()) / (df_clean[y_col].max() - df_clean[y_col].min()) -
            (df_clean[x_col] - df_clean[x_col].min()) / (df_clean[x_col].max() - df_clean[x_col].min())
        )
        return df_clean.nlargest(n, 'score')

    elif criterio == 'alto_xy':
        df_clean['score'] = (
            (df_clean[x_col] - df_clean[x_col].min()) / (df_clean[x_col].max() - df_clean[x_col].min()) +
            (df_clean[y_col] - df_clean[y_col].min()) / (df_clean[y_col].max() - df_clean[y_col].min())
        )
        return df_clean.nlargest(n, 'score')

    elif criterio == 'ratio_y_x':
        df_clean = df_clean[df_clean[x_col] > df_clean[x_col].quantile(0.25)]  # evitar divisiones por valores tiny
        df_clean['score'] = df_clean[y_col] / df_clean[x_col]
        return df_clean.nlargest(n, 'score')

    elif criterio == 'alto_x_bajo_y':
        df_clean['score'] = (
            (df_clean[x_col] - df_clean[x_col].min()) / (df_clean[x_col].max() - df_clean[x_col].min()) -
            (df_clean[y_col] - df_clean[y_col].min()) / (df_clean[y_col].max() - df_clean[y_col].min())
        )
        return df_clean.nlargest(n, 'score')

def render_stats(df_filtrado):
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
    
    st.title("Análisis Visual del Rendimiento")

    st.header("Distribución de Estadísticas (Box Plots)")
    
    # Filtrar solo las columnas numéricas para las estadísticas (excluyendo identificadores y años)
    columnas_excluidas = ['Liga', 'season', 'team', 'player', 'Posición Principal', 'role', 
                        'player_id', 'country_of_citizenship', 'Año', 'image_url']
    columnas_estadisticas = [col for col in df_filtrado.columns if col not in columnas_excluidas]


    col_grafico_1, col_grafico_2 = st.columns(2)

    with col_grafico_1:
        stat_seleccionada = st.selectbox("Selecciona la estadística a analizar:", columnas_estadisticas)

    with col_grafico_2:
        agrupacion = st.selectbox("Agrupar por:", ["Liga", "Posición Principal"])

    fig1, ax1 = plt.subplots(figsize=(10, 6))

    sns.boxplot(data=df_filtrado, x=agrupacion, y=stat_seleccionada, ax=ax1, color=primary_color,
                boxprops=dict(edgecolor=text_color), whiskerprops=dict(color=text_color),
                capprops=dict(color=text_color), medianprops=dict(color=secondary_color, linewidth=2))

    df_filtrado_copy = df_filtrado.copy()
    categorias = df_filtrado[agrupacion].unique()
    texts = [] 

    for i, categoria in enumerate(categorias):
        datos_cat = df_filtrado[df_filtrado[agrupacion] == categoria][stat_seleccionada].dropna()

        q1, q3 = datos_cat.quantile(0.25), datos_cat.quantile(0.75)
        iqr = q3 - q1
        limite_inf = q1 - 1.5 * iqr
        limite_sup = q3 + 1.5 * iqr

        outliers_sup = datos_cat[datos_cat > limite_sup].nlargest(3)
        outliers_inf = datos_cat[datos_cat < limite_inf].nsmallest(3)

        for valor in pd.concat([outliers_sup, outliers_inf]):
            mask = (df_filtrado_copy[agrupacion] == categoria) & (df_filtrado_copy[stat_seleccionada] == valor)
            jugador = df_filtrado_copy[mask][['player', stat_seleccionada]].iloc[0]
            df_filtrado_copy = df_filtrado.drop(df_filtrado_copy[mask].index[0])

            # Crear texto y guardarlo para adjustText
            t = ax1.text(
                i, valor, jugador['player'] + '(' + str(jugador[stat_seleccionada].astype(int)) + ')',
                fontsize=6,
                color=text_color,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.25', facecolor=bg_color, edgecolor=text_color, alpha=0.8)
            )
            texts.append((t, i, valor))

    # adjust_text mueve las etiquetas y dibuja líneas al punto original
    adjust_text(
        [t for t, _, _ in texts],
        x=[x for _, x, _ in texts],
        y=[y for _, _, y in texts],
        ax=ax1,
        expand=(1.2, 1.4),          # cuánto espacio extra dar a cada etiqueta
        arrowprops=dict(
            arrowstyle='-',
            color=text_color,
            lw=0.8
        )
    )

    ax1.set_facecolor(bg_color)
    fig1.patch.set_facecolor(bg_color)
    ax1.set_xlabel(agrupacion, fontweight='bold', color=text_color)
    ax1.set_ylabel(stat_seleccionada, fontweight='bold', color=text_color)
    ax1.tick_params(colors=text_color)
    for spine in ax1.spines.values():
        spine.set_color(text_color)

    plt.xticks(rotation=45 if agrupacion == "Posición Principal" else 0)
    plt.tight_layout()
    st.pyplot(fig1, width='content')
    
    st.header("Mapas de Correlación Temáticos")
    st.write("Explora cómo se relacionan las métricas dentro de fases del juego o su impacto directo en el mercado financiero.")
    
    fase_juego = st.radio("Selecciona el enfoque del análisis:", 
                        ["Ataque y Finalización", "Creación y Pases", "Defensa y Físico", "Impacto en Valor de Mercado"], 
                        horizontal=True)

    cmap_custom = sns.light_palette(primary_color, as_cmap=True)

    if fase_juego == "Impacto en Valor de Mercado":
        cols_corr = ['Valor de Mercado Promedio (M€)', 'Edad', 'Goles', 'Asistencias', 'Goles Esperados (xG)', 'Acciones de Creación de Gol por 90 min', 'Minutos Jugados', 'Puntos por Partido (PPM)']
        
        fig2, ax2 = plt.subplots(figsize=(5, 6))
        
        # Calculamos correlación, aislamos la columna de Valor, quitamos la fila de Valor y ordenamos
        matriz_corr = df_filtrado[cols_corr].corr()[['Valor de Mercado Promedio (M€)']].drop('Valor de Mercado Promedio (M€)')
        matriz_corr = matriz_corr.sort_values(by='Valor de Mercado Promedio (M€)', ascending=False)
        
        sns.heatmap(matriz_corr, annot=True, cmap=cmap_custom, fmt=".2f", 
                    linewidths=0.5, ax=ax2, cbar_kws={'label': 'Nivel de Correlación'},
                    vmin=-1, vmax=1,
                    yticklabels=[c for c in matriz_corr.index],
                    xticklabels=['Valor Promedio (M€)'])
        
        plt.xticks(fontweight='bold')
        plt.yticks(rotation=0)
        st.pyplot(fig2, width='content')

    else:
        if fase_juego == "Ataque y Finalización":
            cols_corr = ['Goles', 'Goles Esperados (xG)', '% Tiros a Puerta', 'Toques en Área Penal Rival', 'Tiros por 90 min']
        elif fase_juego == "Creación y Pases":
            cols_corr = ['Asistencias', 'Asistencias Esperadas (xAG)', 'Pases Progresivos', 'Pases Clave', '% Pases Completados']
        elif fase_juego == "Defensa y Físico": 
            cols_corr = ['Entradas Ganadas', 'Intercepciones', 'Bloqueos', 'Recuperaciones', '% Duelos Aéreos Ganados']
        
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        
        sns.heatmap(df_filtrado[cols_corr].corr(), annot=True, cmap=cmap_custom, fmt=".2f", 
                    linewidths=0.5, ax=ax2, cbar_kws={'label': 'Nivel de Correlación'},
                    xticklabels=[c for c in cols_corr],
                    yticklabels=[c for c in cols_corr])
        
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        st.pyplot(fig2, width='content')

    st.header("Perfiles y Estilos de Juego")
    st.write("Análisis detallado de métricas clave para identificar perfiles de jugadores, eficiencia y su valoración en el mercado.")

    hue_col = st.radio("Clasificar colores por:", ["Liga", "Posición Principal"], horizontal=True)

    N = 7  # jugadores a etiquetar por gráfica
    # Criterio específico por gráfica
    graficas_estaticas = [
        {
            "titulo": "Las 'Gemas Ocultas'",
            "x": "Valor de Mercado Promedio (M€)",
            "y": "Goles y Asistencias",
            "criterio": "alto_y_bajo_x",      # alto rendimiento, bajo valor
            "criterio_desc": "Alto G+A, bajo valor"
        },
        {
            "titulo": "Curva de Valoración",
            "x": "Edad",
            "y": "Valor de Mercado Promedio (M€)",
            "criterio": "alto_y_bajo_x",      # más valiosos siendo jóvenes
            "criterio_desc": "Más valiosos para su edad"
        },
        {
            "titulo": "Finalizadores Letales",
            "x": "Goles Esperados (xG)",
            "y": "Goles",
            "criterio": "alto_y_bajo_x",      # más goles de los esperados (sobre-rinden)
            "criterio_desc": "Superan su xG"
        },
        {
            "titulo": "El Motor del Equipo",
            "x": "Pases Progresivos",
            "y": "Conducciones Progresivas",
            "criterio": "alto_xy",            # élite en ambas dimensiones
            "criterio_desc": "Élite en progresión"
        },
        {
            "titulo": "Calidad de Disparo",
            "x": "Tiros por 90 min",
            "y": "Goles por Tiro",
            "criterio": "ratio_y_x",          # máxima eficiencia: goles/tiro
            "criterio_desc": "Mayor eficiencia disparando"
        },
        {
            "titulo": "El Imán del Área",
            "x": "Toques en Área Penal Rival",
            "y": "Goles Esperados (xG)",
            "criterio": "alto_xy",            # más peligrosos y presentes en el área
            "criterio_desc": "Más peligrosos en el área"
        },
        {
            "titulo": "Eficiencia de Regate",
            "x": "Regates Intentados",
            "y": "% Regates Exitosos",
            "criterio": "alto_xy",            # muchos regates Y alta tasa de éxito
            "criterio_desc": "Más regates y más exitosos"
        },
        {
            "titulo": "Construcción de la Jugada",
            "x": "Pases al Último Tercio",
            "y": "Pases Clave",
            "criterio": "alto_xy",            # constructores de élite
            "criterio_desc": "Mejores creadores"
        },
        {
            "titulo": "Estilos Defensivos",
            "x": "Entradas Ganadas",
            "y": "Intercepciones",
            "criterio": "alto_xy",            # defensores más activos en ambas facetas
            "criterio_desc": "Más activos defensivamente"
        },
    ]

    for i in range(0, len(graficas_estaticas), 3):
        cols = st.columns(3)

        for j, col in enumerate(cols):
            if i + j < len(graficas_estaticas):
                info = graficas_estaticas[i + j]

                fig, ax = plt.subplots(figsize=(5, 4.5))
                fig.patch.set_facecolor(bg_color)
                ax.set_facecolor(bg_color)

                sns.scatterplot(
                    data=df_filtrado,
                    x=info["x"],
                    y=info["y"],
                    hue=hue_col,
                    palette=sns.color_palette("husl", df_filtrado[hue_col].nunique()),
                    alpha=0.6,
                    edgecolor=bg_color,
                    legend=True if i == 0 and j == 1 else False,
                    ax=ax
                )

                if i == 0 and j == 1:
                    sns.move_legend(ax, loc="center right", fontsize=6, title_fontsize=8)

                # Etiquetar jugadores interesantes
                try:
                    destacados = get_jugadores_interesantes(
                        df_filtrado, info["x"], info["y"], info["criterio"], n=N
                    )

                    texts = []
                    for _, row in destacados.iterrows():
                        t = ax.text(
                            row[info["x"]], row[info["y"]],
                            row['player'] + ' (' + str(row['season'])[:2] + '/' + str(row['season'])[2:] + ')',
                            fontsize=6.5,
                            color=text_color,
                            fontweight='bold',
                            bbox=dict(
                                boxstyle='round,pad=0.2',
                                facecolor=bg_color,
                                edgecolor=text_color,
                                alpha=0.85,
                                linewidth=0.8
                            )
                        )
                        texts.append(t)

                    adjust_text(
                        texts,
                        x=destacados[info["x"]].values,
                        y=destacados[info["y"]].values,
                        ax=ax,
                        expand=(1.5, 1.8),
                        arrowprops=dict(arrowstyle='-', color=text_color, lw=0.7)
                    )
                except Exception as e:
                    st.write(e)

                ax.set_title(info["titulo"], fontweight='bold', color=primary_color, fontsize=12)
                ax.set_xlabel(info["x"], fontsize=9, color=text_color)
                ax.set_ylabel(info["y"], fontsize=9, color=text_color)
                ax.tick_params(colors=text_color)
                for spine in ax.spines.values():
                    spine.set_color(text_color)

                col.pyplot(fig)
                plt.close(fig)
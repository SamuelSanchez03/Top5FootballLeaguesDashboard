import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

def render_mapa(df_filtrado):
    st.title("Mapa de Nacionalidades")
    st.markdown("Distribución de jugadores según su país de origen. Utiliza los filtros para explorar ligas o equipos específicos.")

    # CREACIÓN DE FILTROS DINÁMICOS
    col1, col2 = st.columns(2)

    with col1:
        ligas_unicas = ['Todas'] + list(df_filtrado['league'].dropna().unique())
        liga_seleccionada = st.selectbox("Filtro por Liga:", ligas_unicas)

    with col2:
        if liga_seleccionada == 'Todas':
            equipos_unicos = ['Todos'] + list(df_filtrado['team'].dropna().unique())
        else:
            equipos_unicos = ['Todos'] + list(df_filtrado[df_filtrado['league'] == liga_seleccionada]['team'].dropna().unique())
        
        equipo_seleccionado = st.selectbox("Filtro por Equipo:", equipos_unicos)

    df_mapa = df_filtrado.copy()
    df_mapa = df_mapa.drop_duplicates(subset=['player_id'])[['player', 'country_of_citizenship', 'league', 'team']]

    if liga_seleccionada != 'Todas':
        df_mapa = df_mapa[df_mapa['league'] == liga_seleccionada]

    if equipo_seleccionado != 'Todos':
        df_mapa = df_mapa[df_mapa['team'] == equipo_seleccionado]

    mapeo_paises = {
        'England': 'United Kingdom',
        'Scotland': 'United Kingdom',
        'Wales': 'United Kingdom',
        'United States': 'United States of America',
        'Republic of Ireland': 'Ireland',
        'Korea Republic': 'South Korea',
        'Czech Republic': 'Czechia'
    }
    df_mapa['country_of_citizenship'] = df_mapa['country_of_citizenship'].replace(mapeo_paises)
    conteo_paises = df_mapa['country_of_citizenship'].value_counts().reset_index()
    conteo_paises.columns = ['pais', 'cantidad_jugadores']

    # PREPARAR GEOPANDAS Y FOLIUM
    url_mapa = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    world = gpd.read_file(url_mapa)

    # Realizamos un merge del mapa base con datos de jugadores
    mapa_data = world.merge(conteo_paises, how="left", left_on="name", right_on="pais")

    mapa_data['cantidad_jugadores'] = mapa_data['cantidad_jugadores'].fillna(0)

    # DIBUJAR EL MAPA COROPLÉTICO
    m = folium.Map(location=[48.0, 10.0], zoom_start=3, tiles="cartodbpositron")

    folium.Choropleth(
        geo_data=world,
        name="choropleth",
        data=conteo_paises,
        columns=["pais", "cantidad_jugadores"],
        key_on="feature.properties.name", 
        fill_color="YlGnBu", # Paleta: Yellow-Green-Blue 
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Cantidad de Jugadores",
        nan_fill_color="white" # Países sin datos se ven blancos
    ).add_to(m)

    style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000', 'fillOpacity': 0.1, 'weight': 0.1}
    highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity': 0.50, 'weight': 0.1}
    info = folium.features.GeoJson(
        mapa_data,
        style_function=style_function, 
        highlight_function=highlight_function, 
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'cantidad_jugadores'],
            aliases=['País:', 'Jugadores:'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
        )
    )
    m.add_child(info)

    st_folium(m, returned_objects=[], use_container_width=True)
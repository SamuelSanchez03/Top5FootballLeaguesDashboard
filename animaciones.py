import streamlit as st

def render_animaciones():
    st.title("Jugadores y su Valor a lo Largo del Tiempo")
    
    st.header("Carrera de Valuaciones de Jugadores")
    st.markdown("Evolución de las valuaciones de mercado a lo largo del tiempo.")

    valuations_bar_race_path = "Resources/bar_race_valuaciones.mp4"

    valuations_video_file = open(valuations_bar_race_path, 'rb')
    valuations_video_bytes = valuations_video_file.read()

    st.video(
        valuations_video_bytes,
        loop=True,        
        autoplay=False,     
        muted=True,
    )
        
    st.header("Carrera de los Fichajes Más Caros")
    st.markdown("Evolución de las transferencias récord a lo largo del tiempo.")
    
    transfers_bar_race_path = "Resources/bar_race_valuaciones.mp4"

    transfers_video_file = open(transfers_bar_race_path, 'rb')
    transfers_video_bytes = transfers_video_file.read()

    st.video(
        transfers_video_bytes,
        loop=True,        
        autoplay=False,     
        muted=True  
    )
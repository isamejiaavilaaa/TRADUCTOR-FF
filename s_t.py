import streamlit as st
from deep_translator import GoogleTranslator
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import tempfile
import os

# Configuración de la página
st.set_page_config(
    page_title="Traductor Multilenguaje",
    page_icon="🌎",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Título y descripción
st.title("🌎 Traductor Multilenguaje")
st.markdown("### Traduce texto o voz entre diferentes idiomas")

# Diccionario de idiomas soportados
LANGUAGES = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it",
    "Portugués": "pt",
    "Coreano": "ko",
    "Japonés": "ja",
    "Chino (Simplificado)": "zh-CN"
}

# Configuración en la barra lateral
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selección de idiomas
    source_lang = st.selectbox(
        "Idioma de origen:",
        options=list(LANGUAGES.keys()),
        index=0
    )
    
    target_lang = st.selectbox(
        "Idioma de destino:",
        options=list(LANGUAGES.keys()),
        index=1
    )
    
    st.markdown("---")
    st.markdown("### 📝 Instrucciones")
    st.markdown("""
    1. Selecciona los idiomas de origen y destino
    2. Escribe el texto o usa el micrófono
    3. Presiona el botón 'Traducir'
    """)

# Contenedor principal
main_container = st.container()

with main_container:
    # Pestañas para texto y audio
    tab1, tab2 = st.tabs(["✍️ Texto", "🎤 Voz"])
    
    with tab1:
        input_text = st.text_area(
            "Texto a traducir:",
            height=150,
            placeholder="Escribe aquí el texto que deseas traducir..."
        )
        
        if st.button("Traducir Texto", key="translate_text"):
            if input_text:
                try:
                    translator = GoogleTranslator(
                        source=LANGUAGES[source_lang],
                        target=LANGUAGES[target_lang]
                    )
                    translation = translator.translate(input_text)
                    
                    st.markdown("### Resultado:")
                    st.markdown(f'<div style="padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem;">{translation}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error en la traducción: {str(e)}")
            else:
                st.warning("Por favor, ingresa un texto para traducir.")
    
    with tab2:
        st.markdown("### Grabación de Voz")
        
        # Grabador de audio
        audio_bytes = audio_recorder(
            text="🎤 Haz clic para grabar",
            recording_color="#e74c3c",
            neutral_color="#3498db"
        )
        
        if audio_bytes:
            # Guardar el audio temporalmente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                fp.write(audio_bytes)
                temp_audio_path = fp.name
            
            try:
                # Convertir audio a texto
                recognizer = sr.Recognizer()
                with sr.AudioFile(temp_audio_path) as source:
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language=LANGUAGES[source_lang])
                    
                    st.markdown("### Texto reconocido:")
                    st.markdown(f'<div style="padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem;">{text}</div>', unsafe_allow_html=True)
                    
                    # Traducir el texto reconocido
                    translator = GoogleTranslator(
                        source=LANGUAGES[source_lang],
                        target=LANGUAGES[target_lang]
                    )
                    translation = translator.translate(text)
                    
                    st.markdown("### Traducción:")
                    st.markdown(f'<div style="padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem;">{translation}</div>', unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Error en el procesamiento de audio: {str(e)}")
            finally:
                # Limpiar archivo temporal
                os.unlink(temp_audio_path)

# Pie de página
st.markdown("---")
st.markdown("Desarrollado con ❤️ | [Código fuente](https://github.com/tuusuario/traductor)")


import streamlit as st
from googletrans import Translator
from gtts import gTTS
import os
import base64

# Función para generar y reproducir audio
def text_to_speech(text, language):
    try:
        # Crear el objeto gTTS
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Guardar temporalmente el archivo
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        
        # Leer el archivo y codificarlo en base64
        with open(audio_file, "rb") as file:
            audio_bytes = file.read()
            b64 = base64.b64encode(audio_bytes).decode()
            
        # Eliminar el archivo temporal
        os.remove(audio_file)
        
        # Crear el elemento de audio HTML
        audio_html = f'''
            <audio controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Tu navegador no soporta el elemento de audio.
            </audio>
            '''
        return audio_html
    except Exception as e:
        return str(e)

# Configuración de la página
st.set_page_config(
    page_title="Traductor con Audio",
    page_icon="🎧",
    layout="centered"
)

# Inicializar el traductor
translator = Translator()

# Título y descripción
st.title("🎧 Traductor con Audio")
st.markdown("Traduce texto y escucha la pronunciación")

# Diccionario de idiomas soportados (ajustado para gTTS)
LANGUAGES = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it",
    "Portugués": "pt",
    "Japonés": "ja",
    "Chino": "zh-CN"
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

# Área de texto para entrada
input_text = st.text_area(
    "Texto a traducir:",
    height=150,
    placeholder="Escribe aquí el texto que deseas traducir..."
)

# Botón de traducción
if st.button("Traducir y Generar Audio"):
    if input_text:
        try:
            # Realizar traducción
            translation = translator.translate(
                input_text,
                src=LANGUAGES[source_lang],
                dest=LANGUAGES[target_lang]
            )
            
            # Mostrar resultado
            st.markdown("### Traducción:")
            st.info(translation.text)
            
            # Generar y mostrar audio
            st.markdown("### Audio de la traducción:")
            audio_html = text_to_speech(translation.text, LANGUAGES[target_lang])
            st.markdown(audio_html, unsafe_allow_html=True)
            
            # Mostrar transcripción fonética (si está disponible)
            if hasattr(translation, 'pronunciation') and translation.pronunciation:
                st.markdown("### Pronunciación:")
                st.text(translation.pronunciation)
            
        except Exception as e:
            st.error(f"Error en la traducción o generación de audio. Por favor, intenta nuevamente.")
    else:
        st.warning("Por favor, ingresa un texto para traducir.")

# Pie de página
st.markdown("---")
st.markdown("Desarrollado con ❤️")

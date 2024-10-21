import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from googletrans import Translator
import tempfile
import os

# Configuración de la página
st.set_page_config(
    page_title="Traductor de Voz",
    page_icon="🎙️",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Título y descripción
st.title("🎙️ Traductor de Voz")
st.markdown("Graba tu voz y obtén la traducción en texto")

# Diccionario de idiomas soportados
LANGUAGES = {
    "Español": {"code": "es", "speech_code": "es-ES"},
    "Inglés": {"code": "en", "speech_code": "en-US"},
    "Francés": {"code": "fr", "speech_code": "fr-FR"},
    "Alemán": {"code": "de", "speech_code": "de-DE"},
    "Italiano": {"code": "it", "speech_code": "it-IT"},
    "Portugués": {"code": "pt", "speech_code": "pt-BR"}
}

# Inicializar el traductor
translator = Translator()

# Configuración en la barra lateral
with st.sidebar:
    st.header("⚙️ Configuración")
    
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

# Función para transcribir audio
def transcribe_audio(audio_bytes, language):
    try:
        # Guardar el audio temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Inicializar el reconocedor
        recognizer = sr.Recognizer()
        
        # Transcribir el audio
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source, duration=30)  # Limitar a 30 segundos
            text = recognizer.recognize_google(audio_data, language=language)
            
        # Limpiar archivo temporal
        os.remove(temp_audio_path)
        
        return text
    except sr.UnknownValueError:
        st.error("No se pudo entender el audio. Por favor, intenta nuevamente.")
        return None
    except sr.RequestError as e:
        st.error(f"Error en el servicio de reconocimiento de voz: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return None

# Contenedor principal
st.markdown("### 🎤 Grabación de voz")
st.write("Haz clic en el botón para empezar a grabar (máximo 30 segundos):")

# Grabador de audio
audio_bytes = audio_recorder(
    text="Grabar audio",
    recording_color="#e74c3c",
    neutral_color="#3498db",
    icon_name="microphone",
    pause_threshold=30  # Límite de duración en segundos
)

if audio_bytes:
    # Mostrar el audio grabado
    st.audio(audio_bytes, format="audio/wav")
    
    with st.spinner('Transcribiendo audio...'):
        # Transcribir el audio
        transcribed_text = transcribe_audio(
            audio_bytes,
            LANGUAGES[source_lang]["speech_code"]
        )
        
        if transcribed_text:
            # Mostrar texto transcrito
            st.markdown("### 📝 Texto reconocido:")
            st.success(transcribed_text)
            
            with st.spinner('Traduciendo...'):
                try:
                    # Realizar traducción
                    translation = translator.translate(
                        transcribed_text,
                        src=LANGUAGES[source_lang]["code"],
                        dest=LANGUAGES[target_lang]["code"]
                    )
                    
                    # Mostrar traducción
                    st.markdown("### 🔄 Traducción:")
                    st.info(translation.text)
                    
                except Exception as e:
                    st.error("Error en la traducción. Por favor, intenta nuevamente.")

# Instrucciones de uso
with st.expander("📋 Instrucciones de uso"):
    st.markdown("""
    1. Selecciona el idioma de origen y destino en la barra lateral.
    2. Haz clic en el botón "Grabar audio".
    3. Habla claramente en el idioma seleccionado (máximo 30 segundos).
    4. Haz clic nuevamente para detener la grabación.
    5. Espera a que se procese la traducción.
    """)

# Pie de página
st.markdown("---")
st.markdown("Desarrollado con ❤️")

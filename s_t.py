import streamlit as st
from googletrans import Translator
from gtts import gTTS
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io
import os
import base64
import tempfile

# Función para convertir texto a audio
def text_to_speech(text, language):
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        audio_file = "temp_audio.mp3"
        tts.save(audio_file)
        
        with open(audio_file, "rb") as file:
            audio_bytes = file.read()
            b64 = base64.b64encode(audio_bytes).decode()
        
        os.remove(audio_file)
        
        audio_html = f'''
            <audio controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Tu navegador no soporta el elemento de audio.
            </audio>
            '''
        return audio_html
    except Exception as e:
        return str(e)

# Función para transcribir audio
def transcribe_audio(audio_bytes, language='es-ES'):
    try:
        # Guardar el audio temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Inicializar el reconocedor
        recognizer = sr.Recognizer()
        
        # Transcribir el audio
        with sr.AudioFile(temp_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)
            
        # Limpiar archivo temporal
        os.remove(temp_audio_path)
        
        return text
    except Exception as e:
        return None

# Configuración de la página
st.set_page_config(
    page_title="Traductor con Audio",
    page_icon="🎙️",
    layout="centered"
)

# Título y descripción
st.title("🎙️ Traductor con Audio")
st.markdown("Habla o escribe texto y escucha la traducción")

# Diccionario de idiomas soportados
LANGUAGES = {
    "Español": {"code": "es", "speech_code": "es-ES"},
    "Inglés": {"code": "en", "speech_code": "en-US"},
    "Francés": {"code": "fr", "speech_code": "fr-FR"},
    "Alemán": {"code": "de", "speech_code": "de-DE"},
    "Italiano": {"code": "it", "speech_code": "it-IT"},
    "Portugués": {"code": "pt", "speech_code": "pt-BR"},
    "Japonés": {"code": "ja", "speech_code": "ja-JP"}
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

# Tabs para seleccionar método de entrada
input_method = st.radio(
    "Selecciona el método de entrada:",
    ["Texto", "Voz"]
)

input_text = ""

if input_method == "Texto":
    input_text = st.text_area(
        "Texto a traducir:",
        height=150,
        placeholder="Escribe aquí el texto que deseas traducir..."
    )
else:
    st.write("📢 Haz clic en el botón para grabar tu voz:")
    audio_bytes = audio_recorder(
        text="🎙️ Grabar",
        recording_color="#e74c3c",
        neutral_color="#3498db"
    )
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        input_text = transcribe_audio(
            audio_bytes,
            LANGUAGES[source_lang]["speech_code"]
        )
        if input_text:
            st.success(f"Texto reconocido: {input_text}")
        else:
            st.error("No se pudo reconocer el audio. Por favor, intenta nuevamente.")

# Botón de traducción
if st.button("Traducir"):
    if input_text:
        try:
            # Realizar traducción
            translation = translator.translate(
                input_text,
                src=LANGUAGES[source_lang]["code"],
                dest=LANGUAGES[target_lang]["code"]
            )
            
            # Mostrar traducción
            st.markdown("### Traducción:")
            st.info(translation.text)
            
            # Generar y mostrar audio de la traducción
            st.markdown("### Audio de la traducción:")
            audio_html = text_to_speech(
                translation.text,
                LANGUAGES[target_lang]["code"]
            )
            st.markdown(audio_html, unsafe_allow_html=True)
            
        except Exception as e:
            st.error("Error en la traducción. Por favor, intenta nuevamente.")
    else:
        st.warning("Por favor, proporciona texto para traducir.")

# Pie de página
st.markdown("---")
st.markdown("Desarrollado con ❤️")

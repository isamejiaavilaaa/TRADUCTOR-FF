# Importamos las librerías necesarias
import streamlit as st
from googletrans import Translator
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Inicializamos el traductor
translator = Translator()

# Inicializamos el reconocedor de voz
recognizer = sr.Recognizer()

# Función para reconocer el audio desde un archivo
def recognize_from_audio(file):
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='es-ES')
            return text
        except sr.UnknownValueError:
            st.error("No se pudo entender el audio.")
        except sr.RequestError:
            st.error("Error con el servicio de reconocimiento.")
    return None

# Título y descripción de la aplicación
st.title("Traductor")
st.subheader("Sube un archivo de audio para traducirlo, o ingresa el texto manualmente.")

# Descripción adicional en la barra lateral
st.sidebar.header("Traductor")
st.sidebar.write("Sube un archivo de audio, o ingresa el texto manualmente para traducirlo.")

# Mapeo de los lenguajes disponibles
input_languages = {
    "Inglés": "en", 
    "Español": "es", 
    "Alemán": "de",
    "Coreano": "ko", 
    "Esperanto": "eo", 
    "Portugués": "pt", 
    "Italiano": "it"
}

# Selección del lenguaje de entrada en la barra lateral
in_lang = st.sidebar.selectbox(
    "Selecciona el lenguaje de Entrada",
    list(input_languages.keys())
)
input_language = input_languages[in_lang]  # Código del idioma seleccionado

# Selección del lenguaje de salida en la barra lateral
out_lang = st.sidebar.selectbox(
    "Selecciona el lenguaje de salida",
    list(input_languages.keys())
)
output_language = input_languages[out_lang]  # Código del idioma seleccionado

# Opción para elegir entre texto escrito o archivo de audio
option = st.radio("¿Cómo quieres ingresar el texto?", ("Escribir", "Subir archivo de audio"))

# Área de texto o subir archivo de audio
text_to_translate = None
if option == "Escribir":
    text_to_translate = st.text_area(
        "Escribe lo que deseas traducir", 
        placeholder="Introduce tu texto aquí..."
    )
else:
    audio_file = st.file_uploader("Sube un archivo de audio", type=["wav", "mp3"])
    if audio_file is not None:
        text_to_translate = recognize_from_audio(audio_file)

# Botón para realizar la traducción
if st.button("Traducir"):
    if text_to_translate:
        # Realizamos la traducción
        try:
            translation = translator.translate(
                text_to_translate, 
                src=input_language, 
                dest=output_language
            )
            # Mostramos el resultado
            st.success("Traducción exitosa:")
            st.write(f"**{translation.text}**")
        except Exception as e:
            st.error(f"Error en la traducción: {e}")
    else:
        st.warning("Por favor, introduce un texto o sube un archivo de audio para traducir.")

# Imagen decorativa
st.image(
    "https://cdn.pixabay.com/photo/2016/12/13/14/55/robot-1900721_960_720.jpg", 
    caption="Sube un archivo de audio o ingresa el texto."
)

# Pie de página
st.write("---")
st.write("Desarrollado con ❤️ por Isabella Mejía.")






           


        
    



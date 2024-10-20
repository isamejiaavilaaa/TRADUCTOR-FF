# Importamos las librerías necesarias
import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import os

# Inicializamos el traductor y el reconocedor de voz
translator = Translator()
recognizer = sr.Recognizer()

# Título y descripción de la aplicación
st.title("Traductor de Voz (por Archivo)")
st.subheader("Sube tu archivo de audio para traducir.")

# Descripción adicional en la barra lateral
st.sidebar.header("Traductor de Voz")
st.sidebar.write(
    "Sube un archivo de audio en uno de los idiomas disponibles y selecciona el idioma al que quieres traducir."
)

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

# Subida del archivo de audio
audio_file = st.file_uploader("Sube tu archivo de audio (en formato WAV o MP3)", type=["wav", "mp3"])

# Procesamiento del archivo de audio
if audio_file is not None:
    st.write("Archivo subido correctamente.")
    
    # Guardar temporalmente el archivo de audio para procesarlo
    with open("temp_audio_file", "wb") as f:
        f.write(audio_file.getbuffer())
    
    # Convertir el archivo a un formato que speech_recognition pueda manejar
    if audio_file.name.endswith(".mp3"):
        audio = AudioSegment.from_mp3("temp_audio_file")
        audio.export("converted.wav", format="wav")
        audio_path = "converted.wav"
    else:
        audio_path = "temp_audio_file"  # El archivo ya es WAV

    # Reconocimiento de voz desde el archivo cargado
    with sr.AudioFile(audio_path) as source:
        st.write("Procesando el audio...")
        audio_data = recognizer.record(source)
        
        try:
            # Reconocimiento de voz (asegurarse de que el idioma sea soportado por Google)
            recognized_text = recognizer.recognize_google(audio_data, language=input_language)
            st.write(f"Texto reconocido: {recognized_text}")
            
            # Realizar la traducción
            translation = translator.translate(recognized_text, src=input_language, dest=output_language)
            st.success("Traducción exitosa:")
            st.write(f"**{translation.text}**")
        
        except sr.UnknownValueError:
            st.error("No se pudo entender el audio, por favor intenta con otro archivo.")
        except sr.RequestError as e:
            st.error(f"Error con el servicio de reconocimiento de voz; {e}")
    
    # Limpieza de archivos temporales
    os.remove(audio_path)
    os.remove("temp_audio_file")
else:
    st.write("Por favor sube un archivo de audio para traducir.")

# Pie de página
st.write("---")
st.write("Desarrollado con ❤️ por Isabella Mejía.")









           


        
    



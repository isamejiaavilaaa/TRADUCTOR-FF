# Importamos las librerías necesarias
import streamlit as st
import speech_recognition as sr
from googletrans import Translator

# Inicializamos el traductor y el reconocedor de voz
translator = Translator()
recognizer = sr.Recognizer()

# Título y descripción de la aplicación
st.title("Traductor de Voz")
st.subheader("Habla y traduce tu mensaje.")

# Descripción adicional en la barra lateral
st.sidebar.header("Traductor de Voz")
st.sidebar.write(
    "Presiona el botón, habla y luego selecciona el idioma al que quieres traducir."
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

# Botón para grabar voz
if st.button("Grabar voz y traducir"):
    with sr.Microphone() as source:
        st.write("Escuchando... habla ahora:")
        try:
            # Ajusta la energía de ruido ambiental y escucha
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            # Reconoce el discurso (puedes agregar 'input_language' si es compatible con speech_recognition)
            st.write("Procesando...")
            spoken_text = recognizer.recognize_google(audio, language=input_language)

            # Muestra el texto reconocido
            st.write(f"Texto reconocido: {spoken_text}")

            # Realizamos la traducción
            translation = translator.translate(spoken_text, src=input_language, dest=output_language)

            # Mostramos el resultado
            st.success("Traducción exitosa:")
            st.write(f"**{translation.text}**")
        
        except sr.UnknownValueError:
            st.error("No pude entender el audio, por favor intenta de nuevo.")
        except sr.RequestError as e:
            st.error(f"Error en el servicio de reconocimiento de voz; {e}")

# Imagen decorativa
st.image(
    "https://cdn.pixabay.com/photo/2016/12/13/14/55/robot-1900721_960_720.jpg", 
    caption="Presiona el botón y habla para traducir."
)

# Pie de página
st.write("---")
st.write("Desarrollado con ❤️ por Isabella Mejía.")








           


        
    



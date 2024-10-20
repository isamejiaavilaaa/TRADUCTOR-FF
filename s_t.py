# Importamos las librerías necesarias
import streamlit as st
from googletrans import Translator
import speech_recognition as sr

# Inicializamos el traductor
translator = Translator()

# Inicializamos el reconocedor de voz
recognizer = sr.Recognizer()

# Función para capturar la entrada de audio y convertirla en texto
def get_audio():
    with sr.Microphone() as source:
        st.write("Escuchando...")
        audio = recognizer.listen(source)
        try:
            # Usamos Google para reconocer el audio
            text = recognizer.recognize_google(audio, language='es-ES')
            st.write(f"Texto detectado: {text}")
            return text
        except sr.UnknownValueError:
            st.error("No se entendió lo que dijiste.")
        except sr.RequestError:
            st.error("Error en el servicio de reconocimiento de voz.")
        return None

# Título y descripción de la aplicación
st.title("Traductor")
st.subheader("Presiona el botón, cuando escuches la señal habla lo que quieres traducir, luego selecciona la configuración de lenguaje que necesites.")

# Descripción adicional en la barra lateral
st.sidebar.header("Traductor")
st.sidebar.write(
    "Presiona el botón, cuando escuches la señal habla lo que quieres traducir, "
    "luego selecciona la configuración de lenguaje que necesites."
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

# Opción para elegir entre texto escrito o hablado
option = st.radio("¿Cómo quieres ingresar el texto?", ("Escribir", "Hablar"))

# Área de texto o botón para capturar audio
if option == "Escribir":
    text_to_translate = st.text_area(
        "Escribe o habla lo que deseas traducir", 
        placeholder="Introduce tu texto aquí..."
    )
else:
    if st.button("Hablar ahora"):
        text_to_translate = get_audio()  # Llamamos a la función para capturar el audio

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
        st.warning("Por favor, introduce o habla un texto para traducir.")

# Imagen decorativa
st.image(
    "https://cdn.pixabay.com/photo/2016/12/13/14/55/robot-1900721_960_720.jpg", 
    caption="Presiona el Botón y habla lo que quieres traducir"
)

# Pie de página
st.write("---")
st.write("Desarrollado con ❤️ por Isabella Mejía.")





           


        
    



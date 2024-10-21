# Importamos las librerías necesarias
import streamlit as st
from googletrans import Translator
import speech_recognition as sr  # Reconocimiento de voz

# Inicializamos el traductor
translator = Translator()

# Inicializamos el reconocimiento de voz
recognizer = sr.Recognizer()

# Título y descripción de la aplicación
st.title("Traductor con Voz")
st.subheader("Presiona el botón y habla lo que deseas traducir o ingresa texto manualmente.")

# Descripción adicional en la barra lateral
st.sidebar.header("Traductor")
st.sidebar.write(
    "Presiona el botón, habla cuando escuches la señal y selecciona la configuración de lenguaje que necesites."
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

# Opción de usar reconocimiento de voz o ingresar texto manualmente
use_voice = st.checkbox("Usar reconocimiento de voz")

if use_voice:
    # Grabación de voz a través del micrófono
    st.info("Presiona el botón y habla cuando escuches la señal")
    
    if st.button("Grabar voz"):
        with sr.Microphone() as source:
            st.info("Escuchando...")
            try:
                # Ajustamos el ruido ambiental y capturamos la voz
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                st.info("Reconociendo...")
                
                # Convertimos la voz a texto
                text_to_translate = recognizer.recognize_google(audio, language=input_language)
                st.success(f"Texto reconocido: {text_to_translate}")
            except sr.UnknownValueError:
                st.error("No se pudo entender el audio. Por favor, intenta nuevamente.")
            except sr.RequestError as e:
                st.error(f"No se pudo conectar con el servicio de reconocimiento de voz; {e}")
else:
    # Área de texto para ingresar lo que se desea traducir
    text_to_translate = st.text_area(
        "Escribe lo que deseas traducir", 
        placeholder="Introduce tu texto aquí..."
    )

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
        st.warning("Por favor, introduce un texto para traducir.")

# Imagen decorativa
st.image(
    "https://cdn.pixabay.com/photo/2016/12/13/14/55/robot-1900721_960_720.jpg", 
    caption="Presiona el botón y habla lo que quieres traducir."
)

# Pie de página
st.write("---")
st.write("Desarrollado con ❤️ por Isabella Mejía.")











           


        
    



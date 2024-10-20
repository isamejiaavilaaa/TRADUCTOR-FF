# Importamos las librerías necesarias
import streamlit as st
from googletrans import Translator

# Inicializamos el traductor
translator = Translator()

# Título y descripción de la aplicación
st.title("Traductor")
st.subheader("Introduce el texto que deseas traducir.")

# Descripción adicional en la barra lateral
st.sidebar.header("Traductor")
st.sidebar.write(
    "Introduce el texto manualmente para traducirlo."
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
    caption="Introduce el texto para traducir."
)

# Pie de página
st.write("---")
st.write("Desarrollado con ❤️ por Isabella Mejía.")







           


        
    



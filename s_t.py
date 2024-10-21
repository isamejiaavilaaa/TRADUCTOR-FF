import streamlit as st
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Traductor Simple",
    page_icon="🌎",
    layout="centered"
)

# Inicializar el traductor
translator = Translator()

# Título y descripción
st.title("🌎 Traductor Simple")
st.markdown("Traduce texto entre diferentes idiomas")

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

# Área de texto para entrada
input_text = st.text_area(
    "Texto a traducir:",
    height=150,
    placeholder="Escribe aquí el texto que deseas traducir..."
)

# Botón de traducción
if st.button("Traducir"):
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
            
        except Exception as e:
            st.error("Error en la traducción. Por favor, intenta nuevamente.")
    else:
        st.warning("Por favor, ingresa un texto para traducir.")

# Pie de página
st.markdown("---")
st.markdown("Desarrollado con ❤️")

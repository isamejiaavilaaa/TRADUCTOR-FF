import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS
from googletrans import Translator

st.title("TRADUCTOR.")
st.subheader("Escucho lo que quieres traducir.")

# Cargar y mostrar la imagen
image = Image.open('OIG7.jpg')
st.image(image, width=300)

with st.sidebar:
    st.subheader("Traductor.")
    st.write(
        "Presiona el botón, cuando escuches la señal "
        "habla lo que quieres traducir, luego selecciona "
        "la configuración de lenguaje que necesites."
    )

st.write("Toca el Botón y habla lo que quieres traducir")

# Botón de escuchar
stt_button = Button(label=" Escuchar 🎤", width=300, height=50)

stt_button.js_on_event(
    "button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """)
)

result = streamlit_bokeh_events(
    stt_button, events="GET_TEXT", key="listen", 
    refresh_on_update=False, override_height=75, debounce_time=0
)

if result and "GET_TEXT" in result:
    st.write(result.get("GET_TEXT"))
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass

    st.title("Texto a Audio")
    translator = Translator()

    # Selección del lenguaje de entrada
    in_lang = st.selectbox(
        "Selecciona el lenguaje de Entrada",
        ("Inglés", "Español", "Alemán", "Coreano", 
         "Esperanto", "Portugués", "Italiano"),
    )

    # Mapeo de los lenguajes de entrada
    input_languages = {
        "Inglés": "en", "Español": "es", "Alemán": "de",
        "Coreano": "ko", "Esperanto": "eo", "Portugués": "pt",
        "Italiano": "it"
    }
    input_language = input_languages[in_lang]

    # Selección del lenguaje de salida
    out_lang = st.selectbox(
        "Selecciona el lenguaje de salida",
        ("Inglés", "Español", "Alemán", "Coreano", 
         "Esperanto", "Portugués", "Italiano"),
    )

    output_language = input_languages[out_lang]

    # Selección de acento inglés
    english_accent = st.selectbox(
        "Selecciona el acento",
        (
            "Defecto", "Español", "Reino Unido", "Estados Unidos", 
            "Canadá", "Australia", "Irlanda", "Sudáfrica",
        ),
    )

    # Mapeo de los TLD (Top Level Domain) para los acentos
    accents = {
        "Defecto": "com", "Español": "com.mx", "Reino Unido": "co.uk",
        "Estados Unidos": "com", "Canadá": "ca", "Australia": "com.au",
        "Irlanda": "ie", "Sudáfrica": "co.za"
    }
    tld = accents[english_accent]

    # Función de conversión de texto a audio
    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    display_output_text = st.checkbox("Mostrar el texto")

    if st.button("Convertir"):
        text = result.get("GET_TEXT")
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()

        st.markdown("## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("## Texto de salida:")
            st.write(output_text)

    # Función para eliminar archivos antiguos
    def remove_files(n):
        mp3_files = glob.glob("temp/*.mp3")
        if mp3_files:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted", f)

    remove_files(7)

           


        
    



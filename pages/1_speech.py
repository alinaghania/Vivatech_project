import streamlit as st
import base64
import requests
import components
import os
import dotenv

dotenv.load_dotenv()

def submit(image, api_key, voice, hd):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    base64_image = base64.b64encode(image).decode("utf-8")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "Ton objectif est de fournir une première évaluation approfondie de l'état de la voiture et des réparations nécessaires. Mentionne les dommages visibles, les pièces à changer si visible à l'œil, et tout indice pouvant indiquer la cause des dommages, et une estimation des réparations, bien sûr ce ne sont que des suppositions et tu le rappelleras dans ton rapport, j'aimerais que ta réponse soit un rapport adressé à un client",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Sois le plus précis possible sur les dégâts, l'objectif est de savoir quels sont les dégâts et comment y remédier, quelles sont les pièces à changer et comment les changer par exemple, ou le prix des réparations (une estimation), ton objectif est d'adresser un bilan complet de l'état de la voiture avec une estimation des réparations. Sois direct en fr."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                ],
            },
        ],
        "max_tokens": 2048,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        text = response.json()["choices"][0]["message"]["content"]
        st.session_state.extracted_text = text

        tts_payload = {
            "model": "tts-1-hd" if hd else "tts-1",
            "voice": voice,
            "input": text,
        }

        tts_response = requests.post("https://api.openai.com/v1/audio/speech", headers=headers, json=tts_payload)
        tts_response.raise_for_status()
        st.audio(tts_response.content, format="audio/mpeg")
        st.download_button("📥 Save Audio", data=tts_response.content, file_name=f'audio_{tts_response.headers["x-request-id"]}.mp3', mime="audio/mpeg")

        if "balloons" in st.session_state and st.session_state.balloons:
            st.balloons()
    except requests.exceptions.HTTPError as err:
        st.toast(f":red[HTTP error: {err}]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")

def run():
    st.set_page_config(page_title="GPT-4V Speech", page_icon="🗣️")

    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")

    # Move these lines to the top to have them before other components
    st.write("# 🗣️ Analyse your car to drive safe ")
    st.write("Generate audio from an image using GPT-4V + OpenAI TTS.")
    st.info("Your new garagist, but cheaper! 🤖")
    st.write("\n")

    selected_option = st.radio("Image Input", ["Camera", "Image File"], horizontal=True, label_visibility="collapsed")
    image = components.camera_uploader() if selected_option == "Camera" else components.image_uploader()

    voice = st.selectbox("AI Voice", ("echo", "alloy", "fable", "onyx", "nova", "shimmer"))
    hd = st.checkbox("HD", value=True)

    if st.button("Submit") and image and api_key:
        submit(image, api_key, voice, hd)

    if "extracted_text" in st.session_state:
        st.text_area("Extracted Text", st.session_state.extracted_text, height=400)

    components.inc_sidebar_nav_height()
    components.toggle_balloons()

if __name__ == "__main__":
    run()

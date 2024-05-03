import streamlit as st
import base64
import requests
from openai import OpenAI
import components
import os
import dotenv

dotenv.load_dotenv()

def generate_description_and_schema(image, api_key):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    base64_image = base64.b64encode(image).decode("utf-8")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": "Décris l'accident le plus précisément possible, l'aide sera très utile pour les assureurs. Mentionne les dommages visibles, les pièces à changer si visible à l'œil, et tout indice pouvant indiquer la cause des dommages, et une estimation des réparations, bien sûr, ce ne sont que des suppositions et tu le rappelleras dans ton rapport, j'aimerais que ta réponse soit un rapport adressé à un client.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Sois le plus précis possible sur l'accident pour le constat, l'objectif est de savoir ce qui a déclenché l'accident car c'est une aide indispensable pour les assureurs."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
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

        client = OpenAI(api_key=api_key)
        prompt = (
            f"Create a simple schema that shows the impact of :'{text}' "
            "Diagram should be very simple like a child's drawing. "
            "The diagram is going to help assurance to understand the accident. "
            "Don't add any detail, just use it AS-IS, no text"
        )

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        st.session_state.generated_image_url = image_url

        if "balloons" in st.session_state and st.session_state.balloons:
            st.balloons()
    except requests.exceptions.HTTPError as err:
        st.toast(f":red[HTTP error: {err}]")
    except Exception as err:
        st.toast(f":red[Error: {err}]")

    return image_url


def run():
    st.set_page_config(page_title="Create a Report of Your Accident 🚗")
    st.write("# Create a report of your accident 🚗")
    st.write("Generate an image using GPT-4V + Dall-e")
    st.info("Your new garagist, but cheaper! 🤖")
    st.write("\n")

    api_key = st.sidebar.text_input("Enter your OpenAI API key", type="password")
    if not api_key:
        st.sidebar.error("An OpenAI API key is required to proceed.")

    selected_option = st.radio(
        "Image Input",
        ["Camera", "Image File"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if selected_option == "Camera":
        image = components.camera_uploader()
        if st.button("Upload") and image:
            image_url = generate_description_and_schema(image, api_key)
            st.image(image_url, use_column_width=True)
    else:
        image = components.image_uploader()
        if st.button("Upload") and image:
            image_url = generate_description_and_schema(image, api_key)
            st.image(image_url, use_column_width=True)

    if "extracted_text" in st.session_state:
        st.text_area("Extracted Text", st.session_state.extracted_text, height=400)

if __name__ == "__main__":
    run()

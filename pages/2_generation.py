import base64
import requests
import streamlit as st
from openai import OpenAI
import components
import os




def generate_description_and_schema(image, api_key):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    base64_image = base64.b64encode(image).decode("utf-8")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "system",
                "content": " Décris l'accident montré sur la photo de manière détaillée pour déterminer les responsabilités. Mentionne la position des véhicules, les dommages visibles, et tout indice pouvant indiquer la cause de l'accident.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Soit le plus précis possible sur l'accident pour le constat, l'objectif est de savoir qu'est ce qui declenche l'accident car c'est une aide indispensable pour les assureurs."
                
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
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )
        response.raise_for_status()

        text = response.json()["choices"][0]["message"]["content"]
        st.session_state.extracted_text = text

        # Utiliser DALL-E pour générer une image à partir de la variable text
        client = OpenAI(api_key=api_key)

        context = "Based on the sequence of images provided, here is a detailed description leading up to the accident:1. The first few frames show a clear day with traffic lights visible and an intersection controlled by these lights. The camera vehicle is stopped at a red light, and a red sedan appears to be executing a right turn on red onto the cross street in front of the camera vehicle.2. The red sedan continues its turn, and as it completes the turn, the traffic light for the camera vehicle's direction turns green.3. Immediately after the light turns green, the camera vehicle begins to accelerate forward into the intersection. During this time, there's a pedestrian waiting to cross the street, standing on the camera vehicle's right-hand side at the crosswalk.4. As the camera vehicle enters the intersection, the pedestrian begins to cross in front of the camera vehicle. The pedestrian has started to cross against the traffic signal, as it is likely they had a Don't Walk indication due to the green light for vehicular traffic.5. While the pedestrian is crossing, a white SUV approaches from the left at a perpendicular angle to the camera vehicle. This white SUV does not have the right of way as it is facing a red light.6. The white SUV proceeds into the intersection, ignoring the red light, and collides with a black vehicle (which is out of view but its presence is indicated by the impact seen in later frames).7. The white SUV is hit on its left side and rolls over, tipping towards the camera vehicle and eventually landing on its roof in front of the camera vehicle.8. Debris is scattered across the intersection, and the black vehicle involved in the collision with the white SUV is now partially visible after the impact, showing the rear of the vehicle.9. The white SUV remains overturned in the intersection, the red car continues driving away, and the black car moves slowly forward after the collision.From this sequence of events, the fault for the accident appears to lie with the driver of the white SUV for failing to stop at the red light. The pedestrian also crossed inappropriately but does not seem to be involved in the collision between the vehicles. The camera vehicle appears not to have committed any traffic violations leading up to the accident."
        prompt = f" '{context}'. Le schéma doit clairement montrer la position des véhicules et les zones d'impact."


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
    selected_option = st.radio(
        "Image Input",
        ["Camera", "Image File"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if selected_option == "Camera":
        image = components.camera_uploader()
        if st.button("Upload"):
            if image is not None:
                image_url = generate_description_and_schema(image, api_key)
                st.image(image_url, use_column_width=True)
    else:
        image = components.image_uploader()
        if st.button("Upload"):
            if image is not None:
                image_url = generate_description_and_schema(image, api_key)
                st.image(image_url, use_column_width=True)

    if "extracted_text" in st.session_state:
        st.text_area(
            "Extracted Text",
            st.session_state.extracted_text,
            height=400,
        )


run()
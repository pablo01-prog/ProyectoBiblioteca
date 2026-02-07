# este archivo usa Stramlit y conecta con la API de Gemini. 

import streamlit as st
import joblib
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. cargar variables de seguridad (.env)

api_key = st.secrets["API_KEY"]
genai.configure(api_key=api_key)

# 2. Carga del modelo local entrenado anteriormente
modelo_local = joblib.load('modelo_libros.pkl')


# 3. Interfaz de usuario
st.set_page_config(page_title="BiblioIA")
st.title("Mi Recomendador de Libros")
st.write("Dime qué buscas y mi modelo + Gemini te ayudarán.")

user_input = st.text_input("¿Qué libro te apetece?")

if st.button("Recomendar"):
    if user_input:
        # Predicción del género
        genero = modelo_local.predict([user_input])[0]
        st.info(f"Género: {genero}")

        # Gemini
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Recomienda 3 libros de {genero} para: {user_input}"
        res = model.generate_content(prompt)

        st.success(res.text)

import streamlit as st
import joblib
import google.generativeai as genai

genai.configure(api_key=st.secrets["API_KEY"])
modelo_local = joblib.load('modelo_libros.pkl')

st.title("📚 Mi Recomendador de Libros")
user_input = st.text_input("¿Qué libro te apetece leer?")

if st.button("Recomendar"):
    if user_input:
        try:
            genero = modelo_local.predict([user_input])[0]
            st.info(f"🔍 Género detectado: {genero}")

            # USAMOS GEMINI-PRO QUE ES COMPATIBLE CON v1beta
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"Recomienda 3 libros de {genero} para: {user_input}."
            response = model.generate_content(prompt)
            
            st.success("🤖 Recomendaciones:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")

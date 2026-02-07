import streamlit as st
import joblib
import google.generativeai as genai

# 1. Configuración de API
genai.configure(api_key=st.secrets["API_KEY"])

# 2. Carga del modelo local
modelo_local = joblib.load('modelo_libros.pkl')

# 3. Interfaz
st.set_page_config(page_title="BiblioIA")
st.title("📚 Mi Recomendador de Libros")
st.write("Tu IA local detecta el género y Gemini te recomienda los mejores títulos.")

user_input = st.text_input("¿Qué libro te apetece leer hoy?")

if st.button("Recomendar"):
    if user_input:
        try:
            # A. Predicción con tu modelo local (esto ya te funciona bien)
            genero = modelo_local.predict([user_input])[0]
            st.info(f"🔍 Género detectado por el modelo local: **{genero}**")

            # B. Llamada a Gemini con la versión de modelo más estable
            # Usamos 'gemini-1.5-flash' sin prefijos para evitar el error 404 de v1beta
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Basado en que el usuario busca '{user_input}' y el género es '{genero}', recomienda 3 libros reales y explica brevemente por qué."
            
            response = model.generate_content(prompt)
            
            st.success("✨ **Sugerencias de Gemini:**")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Hubo un problema con la recomendación: {e}")
    else:
        st.warning("Por favor, escribe algo primero.")

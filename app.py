import streamlit as st
import joblib
import google.generativeai as genai

# Configuración de la API Key
genai.configure(api_key=st.secrets["API_KEY"])

# Carga del modelo local
modelo_local = joblib.load('modelo_libros.pkl')

st.title("📚 Mi Recomendador de Libros")
st.write("Mi IA local detecta el género y Gemini te recomienda el libro.")

user_input = st.text_input("¿Qué libro te apetece leer?")

if st.button("Recomendar"):
    if user_input:
        # 1. Predicción con modelo local (ESTO YA TE FUNCIONA)
        genero = modelo_local.predict([user_input])[0]
        st.info(f"🔍 Género detectado: {genero}")

        # 2. Llamada a Gemini con el nombre de modelo compatible
        try:
            # CAMBIO CLAVE: Usamos la versión estable sin prefijos extraños
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Como experto bibliotecario, recomienda 3 libros de género {genero} para alguien que busca: {user_input}."
            
            # Forzamos la respuesta
            response = model.generate_content(prompt)
            
            st.success("🤖 **Recomendaciones:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error en Gemini: {e}")

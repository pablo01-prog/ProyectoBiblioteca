import streamlit as st
import joblib
import google.generativeai as genai

# 1. Configuración de la API Key
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
            # A. Predicción con tu modelo local (Esto ya te funciona)
            genero = modelo_local.predict([user_input])[0]
            st.info(f"🔍 Género detectado: **{genero}**")

            # B. Llamada a Gemini (Nombre de modelo compatible)
            model = genai.GenerativeModel('gemini-1.5-flash')
                # Configuración avanzada para forzar compatibilidad
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 1000,
                }
            )
            
            prompt = f"Basado en que el usuario busca '{user_input}' y el género es '{genero}', recomienda 3 libros reales."
            
            response = model.generate_content(prompt)
            
            st.success("✨ **Sugerencias:**")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Hubo un problema: {e}")
    else:
        st.warning("Por favor, escribe algo primero.")

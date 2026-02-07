import streamlit as st
import joblib
import google.generativeai as genai

# 1. Configuración de la API Key desde Secrets
genai.configure(api_key=st.secrets["API_KEY"])

# 2. Carga del modelo local .pkl
# Asegúrate de que el nombre coincida con tu archivo en GitHub
modelo_local = joblib.load('modelo_libros.pkl')

# 3. Interfaz de usuario de Streamlit
st.set_page_config(page_title="BiblioIA", page_icon="📚")
st.title("📚 Mi Recomendador de Libros")
st.write("Dime qué buscas y mi IA clasificará el género para que Gemini te recomiende títulos.")

user_input = st.text_input("Describe el libro que te gustaría leer:", placeholder="Ej: Una historia de dragones y caballeros")

if st.button("Recomendar"):
    if user_input.strip() == "":
        st.warning("Por favor, escribe una descripción primero.")
    else:
        try:
            # Predicción del género con tu modelo local
            genero = modelo_local.predict([user_input])[0]
            st.info(f"🔍 Género detectado por el modelo: **{genero}**")

            # Configuración de Gemini (usando el nombre de modelo más compatible)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"El usuario busca un libro con esta descripción: {user_input}. El género es {genero}. Recomienda 3 libros reales y explica por qué."
            
            response = model.generate_content(prompt)

            # Mostrar la recomendación final
            st.success("🤖 **Recomendaciones de la IA:**")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Se ha producido un error: {e}")

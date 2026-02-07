import streamlit as st
import joblib
import google.generativeai as genai

# -----------------------------
# Configuración de la API Key
# -----------------------------
genai.configure(api_key=st.secrets["API_KEY"])

# -----------------------------
# Carga del modelo local
# -----------------------------
modelo_local = joblib.load('modelo_libros.pkl')

# -----------------------------
# Interfaz de Streamlit
# -----------------------------
st.title("Mi Recomendador")

user_input = st.text_input("Describe el libro que te gustaría leer:")

if st.button("Recomendar"):
    if user_input.strip() == "":
        st.write("Por favor, escribe una descripción primero 🙂")
    else:
        # Predicción del género con el modelo local
        genero = modelo_local.predict([user_input])[0]

        # -----------------------------
        # Llamada a Gemini (versión correcta del modelo)
        # -----------------------------
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash"
        )

        prompt = f"""
        El usuario busca un libro con esta descripción:
        "{user_input}"

        El género detectado es: {genero}

        Recomienda un libro adecuado y explica brevemente por qué.
        """

        response = model.generate_content(prompt)

        # -----------------------------
        # Mostrar resultados
        # -----------------------------
        st.write("📚 **Género detectado:**", genero)
        st.write("🤖 **Recomendación:**")
        st.write(response.text)

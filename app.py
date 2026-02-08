import streamlit as st
import joblib
import google.generativeai as genai

# 1. Configuración de la API Key
genai.configure(api_key=st.secrets["API_KEY"])

# 2. Carga del modelo local (Mantenemos tu trabajo previo)
modelo_local = joblib.load('modelo_libros.pkl')

st.title("📚 BiblioIA: Diagnóstico y Recomendador")

# --- SECCIÓN DE DIAGNÓSTICO (Añadida para ver la lista) ---
st.subheader("🔍 Paso 1: Ver modelos disponibles (Call ListModels)")
if st.button("Mostrar Lista de Modelos"):
    try:
        modelos = genai.list_models()
        st.write("Copia uno de estos nombres exactamente como aparecen:")
        for m in modelos:
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name) # Aquí verás los nombres para el Paso 2
    except Exception as e:
        st.error(f"Error al listar: {e}")

st.divider()

# --- SECCIÓN DEL RECOMENDADOR (Tu código original mejorado) ---
st.subheader("📖 Paso 2: Tu Recomendador")
user_input = st.text_input("Describe el libro que buscas:")

# IMPORTANTE: Aquí pondremos el nombre que copies de la lista de arriba
# Por ahora dejo uno que suele aparecer en v1beta, pero cámbialo si ves otro
nombre_modelo_elegido = "models/gemini-2.5-flash"

if st.button("Recomendar"):
    if user_input:
        try:
            # Predicción local
            genero = modelo_local.predict([user_input])[0]
            st.info(f"Género detectado: {genero}")

            # Llamada a Gemini
            model = genai.GenerativeModel(nombre_modelo_elegido)
            prompt = f"Recomienda 3 libros de {genero} para: {user_input}."
            response = model.generate_content(prompt)
            
            st.success("🤖 Sugerencias:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error en el Paso 2: {e}")
            st.info("Si sale error 404, asegúrate de que el nombre en 'nombre_modelo_elegido' coincide con uno de la lista del Paso 1.")

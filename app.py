# este archivo usa Stramlit y conecta con la API de Gemini. 

import streamlit as st
import joblib
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. cargar variables de seguridad (.env)

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# 2. cargar el modelo local entrenado anteriormente

modelo_local = joblib.load('modelo_libros.pkl')
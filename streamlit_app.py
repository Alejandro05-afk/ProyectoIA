import streamlit as st
import requests
import os

# Configuración para producción
API_BASE_URL = os.getenv("RAILWAY_URL", "http://localhost:8000")

# Resto del código de app.py original
# (Copiar todo el contenido de app.py aquí)

# Actualizar la línea 246:
# API_BASE_URL = "http://localhost:8000" 
# Por:
# API_BASE_URL = os.getenv("RAILWAY_URL", "http://localhost:8000")

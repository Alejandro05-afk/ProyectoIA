# 🚀 Deploy en Railway

## Pasos para Deploy

### 1. Preparar Repositorio
```bash
git add .
git commit -m "Agregar configuración para Railway deploy"
git push origin main
```

### 2. Configurar Railway
1. Ve a [railway.app](https://railway.app)
2. Conecta tu cuenta de GitHub
3. Selecciona el repositorio `ProyectoIA`
4. Railway detectará automáticamente el proyecto Python

### 3. Variables de Entorno
Configura estas variables en Railway:

**Base de Datos:**
- `MONGODB_URL`: `mongodb+srv://kogamaandres_db_user:fwsAYpZWhHb6Anq1@electroshop.q0k2ovr.mongodb.net/?appName=electroshop`
- `DATABASE_NAME`: `electroshop`
- `COLLECTION_NAME`: `electroshop`

**API de IA:**
- `GROQ_API_KEY`: `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`

**Configuración:**
- `PORT`: `8000`

### 4. Deploy Automático
- Railway hará deploy automáticamente
- La URL estará disponible en el dashboard de Railway
- El health check está configurado en `/health`

### 5. Verificación
Una vez desplegado:
- API: `https://tu-app.railway.app/docs`
- Health: `https://tu-app.railway.app/health`
- Productos: `https://tu-app.railway.app/products/`

### 6. Frontend (Streamlit Cloud)
Para el frontend:
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Conecta tu GitHub
3. Selecciona el repositorio y archivo `app.py`
4. Configura la URL del backend en las variables de entorno

## URLs Finales
- **Backend**: Railway URL
- **Frontend**: Streamlit Cloud URL
- **Base de Datos**: MongoDB Atlas

# 🖥️ ElectroShop – Tienda de productos electrónicos

Aplicación web full-stack con **FastAPI + MongoDB** (backend) y **Streamlit** (frontend) para gestionar y comprar productos electrónicos. Incluye stock en tiempo real, carrito dinámico y UI moderna.

---

## 🛠️ Stack

- **Backend**: FastAPI + Motor (MongoDB async)
- **Frontend**: Streamlit
- **Base de datos**: MongoDB (`electroshop`)
- **Python**: 3.13 (recomendado)

---

## 📂 Estructura

```
ProyectoIA/
├── backend/
│   ├── main.py          # App FastAPI (CRUD + stock)
│   ├── models.py        # Esquemas Pydantic
│   ├── crud.py          # Operaciones MongoDB
│   ├── database.py      # Conexión a MongoDB
│   ├── requirements.txt
│   └── README.md        # Instrucciones del backend
├── app.py              # Frontend Streamlit
├── .gitignore
└── README.md
```

---

## 🚀 Ejecutar el proyecto

### 1️⃣ Requisitos

- **MongoDB** corriendo en `mongodb://localhost:27017`
- **Python 3.13** (evita incompatibilidad con Pydantic/FastAPI)

### 2️⃣ Backend (FastAPI)

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

- **API Docs**: http://localhost:8000/docs
- **Productos seed**: se cargan automáticamente si la colección está vacía.

### 3️⃣ Frontend (Streamlit)

En otra terminal:

```bash
streamlit run app.py --server.port 8502
```

- Acceso: http://localhost:8502

---

## 📦 Funcionalidades

- ✅ Listado de productos con stock real
- ✅ Filtros por categoría
- ✅ Carrito dinámico con controles **➖/➕**
- ✅ Actualización automática de stock en MongoDB al comprar
- ✅ Botón “Actualizar productos” para refrescar desde el backend
- ✅ UI moderna con CSS personalizado

---

## 🔧 Endpoints clave (Backend)

- `GET /products/` – Listar productos (paginación, filtros)
- `PATCH /products/{id}/stock?stock_change=N` – Actualizar stock
- `GET /initialize/` – Cargar productos iniciales (seed)

---

## 📝 Notas

- Si el backend no responde, el frontend usa productos locales (fallback).
- El stock se valida en backend: no permite valores negativos.
- Los productos se identifican por `_id` (MongoDB) o `nombre` (fallback).

---

## 👤 Autores
**Mateo Barba**
**Alejandro Guanoluisa**
**Andrés Panchi**  
Proyecto académico – EPN  
Repositorio: https://github.com/Alejandro05-afk/ProyectoIA



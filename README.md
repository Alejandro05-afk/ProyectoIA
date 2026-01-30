# 🖥️ ElectroShop – Tienda de productos electrónicos

Aplicación web full-stack desarrollada con **FastAPI + MongoDB** (backend) y **Streamlit** (frontend) para la gestión y comercialización de productos electrónicos. El sistema integra un **Asistente Virtual inteligente** basado en el modelo **Llama 3.3 (70B)** a través de la infraestructura de **Groq**. Mediante una arquitectura de **Contexto Dinámico**, la IA accede en tiempo real a las especificaciones técnicas y al stock del inventario almacenado en MongoDB para ofrecer asesoría técnica especializada y recomendaciones de compra precisas. El proyecto incluye gestión de stock en tiempo real, carrito dinámico sincronizado y una interfaz de usuario moderna.

## 🤖 Implementación de Inteligencia Artificial

El núcleo inteligente del sistema se basa en un **Chatbot Asistente** diseñado bajo principios de **RAG (Retrieval-Augmented Generation)** simplificado:

* **Motor LLM**: Implementación del modelo **Llama 3.3 (70B) Versatile** a través de la infraestructura de **Groq**, permitiendo respuestas en milisegundos gracias a su tecnología de LPUs (Language Processing Units).
* **Inyección de Contexto Dinámico**: El backend actúa como orquestador, extrayendo en tiempo real el estado del inventario desde **MongoDB** (especificaciones técnicas, precios y stock) e inyectándolo en el prompt de la IA para garantizar respuestas precisas y evitar alucinaciones.
* **Asesoría Especializada**: Gracias al enriquecimiento de datos, la IA puede realizar comparativas de hardware (ej. DDR4 vs DDR5), verificar compatibilidades y recomendar productos según perfiles de usuario (ej. Gaming competitivo o Diseño gráfico).

---

## 🛠️ Stack Tecnológico

* **IA**: Groq Cloud API (Llama 3.3 70B).
* **Backend**: FastAPI (Framework asíncrono de alto rendimiento).
* **Base de Datos**: MongoDB + Motor (Driver asíncrono para Python).
* **Frontend**: Streamlit (Framework para aplicaciones de datos e IA).
* **Lenguaje**: Python 3.13 (Garantiza compatibilidad con las últimas versiones de Pydantic y el SDK de Groq).

---

## 📂 Estructura del Proyecto
```

### 2️⃣ Backend (FastAPI)
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3️⃣ Frontend (Streamlit) - En otra terminal
```bash
streamlit run app.py --server.port 8502
```

### 4️⃣ Acceso
- **Frontend**: http://localhost:8502
- **Backend API**: http://localhost:8000/docs
- **Inicializar productos**: http://localhost:8000/initialize/

---

## 🛠️ Stack

- **Backend**: FastAPI + Motor (MongoDB async)
- **Frontend**: Streamlit
- **Base de datos**: MongoDB Atlas
- **Python**: 3.13 (recomendado)

---

## 📂 Estructura

```text
ProyectoIA/
├── backend/
│   ├── main.py          # App FastAPI (CRUD + stock)
│   ├── models.py        # Esquemas Pydantic + productos iniciales
│   ├── crud.py          # Operaciones MongoDB
│   ├── database.py      # Conexión a MongoDB Atlas
│   ├── .env             # Variables de entorno (NO subir a Git)
│   └── requirements.txt
├── app.py              # Frontend Streamlit
├── .gitignore
└── README.md
```
* `GET /products/` – Listar productos con soporte para paginación y filtros.
* `POST /chat/` – Orquestador que procesa las consultas del usuario mediante la IA de Groq.
* `PATCH /products/{id}/stock?stock_change=N` – Actualización atómica de existencias.
* `GET /initialize/` – Carga de productos iniciales enriquecidos con especificaciones técnicas (Seed).

---

## 📝 Notas Técnicas

* **Arquitectura de IA**: El éxito del asistente se basa en la curación de datos; al enriquecer el campo `descripcion` en `models.py`, el modelo Llama 3 actúa como experto sin necesidad de re-entrenamiento (Fine-tuning).
* **Resiliencia (Fallback)**: Si el backend no responde, el frontend utiliza una lista de productos locales para mantener la interfaz operativa.
* **Integridad**: El stock se valida rigurosamente en el servidor; no se permiten transacciones que resulten en valores menores a cero.

---

## 👤 Autores
**Mateo Barba** | **Alejandro Guanoluisa** | **Andrés Panchi** *Proyecto académico – Escuela Politécnica Nacional (EPN)* **Repositorio:** [https://github.com/Alejandro05-afk/ProyectoIA](https://github.com/Alejandro05-afk/ProyectoIA)



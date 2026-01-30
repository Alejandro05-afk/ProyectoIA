import os
import streamlit as st
import requests

# -------- CONFIGURACIÓN --------
st.set_page_config(
    page_title="ElectroShop",
    page_icon="💻",
    layout="wide"
)

# URL DEL BACKEND (Render)
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# -------- ESTILOS --------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0F172A, #020617);
    color: white;
}

header[data-testid="stHeader"] {
    background-color: #020617 !important;
    border-bottom: 1px solid #00ADB5;
}

[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #00ADB5;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="column"] {
    background: linear-gradient(145deg, #0a0f1e, #020617);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(0,173,181,0.4);
    border: 1px solid rgba(0,173,181,0.2);
}

h1, h2, h3 {
    color: #00ADB5 !important;
}
</style>
""", unsafe_allow_html=True)

# -------- ESTADO --------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "mensaje" not in st.session_state:
    st.session_state.mensaje = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------- PRODUCTOS LOCALES (fallback) --------
productos_locales = [
    {
        "nombre": "RAM DDR4 16GB",
        "precio": 65,
        "categoria": "Memoria",
        "imagen": "https://nomadaware.com.ec/wp-content/uploads/VENG_LPX_BLK_01.png"
    },
    {
        "nombre": "GPU RTX 4060",
        "precio": 420,
        "categoria": "Tarjetas Gráficas",
        "imagen": "https://d2vfia6k6wrouk.cloudfront.net/productimages/6a308493-0e0b-4aff-b164-b00600f6f3f9/images/pny-rtx-4060-ti-8gb-verto-dual-fan-ra.png"
    }
]

# -------- FUNCIONES --------
def fetch_products():
    try:
        r = requests.get(f"{API_BASE_URL}/products/", params={"per_page": 100}, timeout=5)
        if r.status_code == 200:
            return r.json().get("products", productos_locales)
    except Exception:
        pass
    return productos_locales

# -------- SIDEBAR --------
st.sidebar.title("🛒 ElectroShop")
pagina = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Productos", "Carrito", "Chatbot"]
)

# -------- INICIO --------
if pagina == "Inicio":
    st.title("💻 ElectroShop")
    st.subheader("Tu tienda de tecnología inteligente")
    st.image("https://cdn-icons-png.flaticon.com/512/2777/2777142.png", width=200)

# -------- PRODUCTOS --------
elif pagina == "Productos":
    st.header("📦 Productos disponibles")

    productos = fetch_products()

    cols = st.columns(3)
    for i, producto in enumerate(productos):
        with cols[i % 3]:
            st.image(producto.get("imagen"), width=220)
            st.subheader(producto.get("nombre"))
            st.caption(producto.get("categoria"))
            st.write(f"💲 **${producto.get('precio')}**")

            if st.button("Agregar 🛒", key=f"add_{i}"):
                st.session_state.carrito.append(producto)
                st.success("Producto agregado")

# -------- CARRITO --------
elif pagina == "Carrito":
    st.header("🧾 Carrito")

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío")
    else:
        total = 0
        for p in st.session_state.carrito:
            st.write(f"- {p['nombre']} (${p['precio']})")
            total += p["precio"]

        st.subheader(f"💰 Total: ${total}")

        if st.button("Finalizar compra"):
            st.session_state.carrito.clear()
            st.success("Compra realizada 🎉")
            st.balloons()

# -------- CHATBOT --------
elif pagina == "Chatbot":
    st.header("🤖 Asistente ElectroShop")

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)

    if prompt := st.chat_input("¿En qué puedo ayudarte?"):
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("assistant"):
            try:
                r = requests.post(
                    f"{API_BASE_URL}/chat/",
                    json={"question": prompt},
                    timeout=15
                )
                respuesta = r.json().get("response", "Sin respuesta")
            except Exception as e:
                respuesta = f"❌ Error conectando al backend: {e}"

            st.markdown(respuesta)
            st.session_state.chat_history.append(("assistant", respuesta))

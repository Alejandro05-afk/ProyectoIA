import os
import streamlit as st
import requests

# ================== CONFIG ==================
st.set_page_config(
    page_title="ElectroShop",
    page_icon="💻",
    layout="wide"
)

API_BASE_URL = os.getenv(
    "BACKEND_URL",
    "https://electroshop-backend-9xa5.onrender.com"   
)

# ================== ESTILOS ==================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0F172A, #020617); color: white; }
h1, h2, h3 { color: #00ADB5; }
</style>
""", unsafe_allow_html=True)

# ================== ESTADO ==================
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# ================== API ==================
def fetch_products():
    try:
        r = requests.get(
            f"{API_BASE_URL}/products/",
            params={"per_page": 100},
            timeout=10
        )
        if r.status_code == 200:
            return r.json().get("products", [])
    except Exception as e:
        st.error(f"Error cargando productos: {e}")
    return []

# ================== SIDEBAR ==================
st.sidebar.title("🛒 ElectroShop")
pagina = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Productos", "Carrito", "Chatbot"]
)

# ================== INICIO ==================
if pagina == "Inicio":
    st.title("💻 ElectroShop")
    st.subheader("Tu tienda de artículos electrónicos")
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2777/2777142.png",
        width=200
    )

# ================== PRODUCTOS ==================
elif pagina == "Productos":
    st.header("📦 Productos disponibles")

    productos = fetch_products()

    if not productos:
        st.warning("No hay productos disponibles")
        st.stop()

    for i in range(0, len(productos), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(productos):
                p = productos[i + j]
                with cols[j]:
                    st.image(p.get("imagen"), width=220)
                    st.subheader(p.get("nombre"))
                    st.caption(p.get("categoria"))
                    st.write(f"💲 **${p.get('precio')}**")

                    stock = p.get("stock")
                    if stock is not None:
                        if stock <= 0:
                            st.error("Sin stock")
                        else:
                            st.write(f"Stock: {stock}")

                    if st.button(
                        "Agregar 🛒",
                        key=f"add_{p.get('_id')}"
                    ):
                        st.session_state.carrito.append(p)
                        st.success("Agregado al carrito")

# ================== CARRITO ==================
elif pagina == "Carrito":
    st.header("🧾 Carrito de compras")

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío")
        st.stop()

    conteo = {}
    total = 0

    for p in st.session_state.carrito:
        pid = p.get("_id") or p.get("id")
        if not pid:
            st.error(f"Producto sin ID: {p.get('nombre', 'Desconocido')}")
            continue
        conteo[pid] = conteo.get(pid, 0) + 1
        total += p.get("precio", 0)

    for pid, qty in conteo.items():
        prod = next((p for p in st.session_state.carrito if (p.get("_id") or p.get("id")) == pid), None)
        if prod:
            st.write(f"✔ {prod['nombre']} x{qty} — ${prod['precio'] * qty}")
        else:
            st.write(f"✔ Producto ID {pid} x{qty}")

    st.subheader(f"💰 Total: ${total}")

    if st.button("Finalizar compra"):
        ok = True
        actualizados = []
        for pid, qty in conteo.items():
            try:
                r = requests.patch(
                    f"{API_BASE_URL}/products/{pid}/stock",
                    params={"stock_change": -qty},
                    timeout=10
                )
                if r.status_code == 200:
                    actualizados.append(f"{pid}: -{qty}")
                else:
                    ok = False
                    st.error(f"Error actualizando {pid}: {r.text}")
            except Exception as e:
                ok = False
                st.error(f"Error de conexión: {e}")

        if ok:
            st.success(f"✅ Stock actualizado: {', '.join(actualizados)}")
            st.session_state.carrito.clear()
            st.success("Compra realizada con éxito 🎉")
            st.balloons()

# ================== CHATBOT ==================
elif pagina == "Chatbot":
    st.header("🤖 Asistente Virtual ElectroShop")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, text in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(text)

    if prompt := st.chat_input("¿En qué puedo ayudarte?"):
        with st.chat_message("user"):
            st.markdown(prompt)
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
                respuesta = f"Error: {e}"

            st.markdown(respuesta)
            st.session_state.chat_history.append(("assistant", respuesta))

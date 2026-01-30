import streamlit as st
import requests
import os

# -------- CONFIGURACIÓN --------
st.set_page_config(
    page_title="ElectroShop",
    page_icon="💻",
    layout="wide"
)

API_BASE_URL = os.getenv("RAILWAY_URL", "http://localhost:8000")

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #0F172A, #020617);
    color: white;
}

/* Header con fondo oscuro */
header[data-testid="stHeader"] {
    background-color: #020617 !important;
    border-bottom: 1px solid #00ADB5;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #00ADB5;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Título del sidebar */
[data-testid="stSidebar"] h1 {
    color: #00ADB5 !important;
    text-shadow: 0 0 10px rgba(0,173,181,0.5);
}

/* Estilo para las columnas de productos */
[data-testid="column"] {
    background: linear-gradient(145deg, #0a0f1e, #020617);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(0,173,181,0.4);
    border: 1px solid rgba(0,173,181,0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

[data-testid="column"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 30px rgba(0,173,181,0.6);
}

/* Botones compactos +/- */
button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, #00ADB5, #00868c) !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: bold !important;
    border: none !important;
    padding: 4px 12px !important;
    transition: all 0.2s ease !important;
    width: auto !important;
    min-width: 36px !important;
    font-size: 1.2em !important;
    line-height: 1.2 !important;
}

button[data-testid="baseButton-secondary"]:hover {
    background: linear-gradient(135deg, #00c9d1, #00ADB5) !important;
    transform: scale(1.1) !important;
}

/* Títulos */
h1 {
    color: #00ADB5 !important;
    text-shadow: 0 0 15px rgba(0,173,181,0.6);
}

h2, h3 {
    color: #00ADB5 !important;
}

/* Texto general */
.stMarkdown, p, span, div {
    color: white !important;
}

/* SelectBox */
.stSelectbox label {
    color: white !important;
    font-weight: 600 !important;
}

.stSelectbox > div > div {
    background-color: #0F172A !important;
    color: white !important;
    border: 1px solid #00ADB5 !important;
}

[data-baseweb="select"] {
    background-color: #0F172A !important;
}

[data-baseweb="select"] > div {
    background-color: #0F172A !important;
    color: white !important;
    border: 1px solid #00ADB5 !important;
}

[role="listbox"] {
    background-color: #0F172A !important;
}

[role="option"] {
    background-color: #0F172A !important;
    color: white !important;
}

[role="option"]:hover {
    background-color: #00ADB5 !important;
    color: white !important;
}

[data-baseweb="select"] span {
    color: white !important;
}

/* TextInput */
.stTextInput label {
    color: white !important;
}

.stTextInput input {
    background-color: #0F172A !important;
    color: white !important;
    border: 1px solid #00ADB5 !important;
    border-radius: 8px !important;
}

.stTextInput input::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

/* Divider */
hr {
    border-color: #00ADB5 !important;
    opacity: 0.5;
}

/* Mensajes */
.stSuccess, .stInfo, .stWarning {
    background-color: rgba(0,173,181,0.1) !important;
    border: 1px solid #00ADB5 !important;
    color: white !important;
}

.stSuccess > div, .stInfo > div, .stWarning > div {
    color: white !important;
}

/* Radio buttons */
.stRadio > label {
    color: white !important;
}

.stRadio > div {
    color: white !important;
}

.stRadio [role="radiogroup"] label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# -------- ESTADO --------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

if "mensaje" not in st.session_state:
    st.session_state.mensaje = None

# -------- DATOS SIMULADOS --------
productos = [
    {
        "nombre": "RAM DDR4 16GB",
        "precio": 65,
        "categoria": "Memoria",
        "imagen": "https://nomadaware.com.ec/wp-content/uploads/VENG_LPX_BLK_01.png"
    },
    {
        "nombre": "RAM DDR5 32GB",
        "precio": 140,
        "categoria": "Memoria",
        "imagen": "https://static.gigabyte.com/StaticFile/Image/Global/fe5413eea1b1be5c580a8c6a1945efb9/Product/30681"
    },
    {
        "nombre": "GIGABYTE SSD NVMe 1TB OARUS",
        "precio": 90,
        "categoria": "Almacenamiento",
        "imagen": "https://static.gigabyte.com/StaticFile/Image/Global/13fdaa6e6dc982d0753d32c70c23d92c/Product/30161"
    },
    {
        "nombre": "SSD SATA 512GB",
        "precio": 55,
        "categoria": "Almacenamiento",
        "imagen": "https://toners.ec/wp-content/uploads/2024/09/disco-solido-adata-512-gb-su650-ssd-azul-25-sata.png"
    },
    {
        "nombre": "HDD 2TB",
        "precio": 70,
        "categoria": "Almacenamiento",
        "imagen": "https://nanotroniconline.com/wp-content/uploads/2020/08/disco-duro-hdd-western-digital-blue-2tb-7200rpm-nanotronic.png"
    },
    {
        "nombre": "GPU RTX 4060",
        "precio": 420,
        "categoria": "Tarjetas Gráficas",
        "imagen": "https://d2vfia6k6wrouk.cloudfront.net/productimages/6a308493-0e0b-4aff-b164-b00600f6f3f9/images/pny-rtx-4060-ti-8gb-verto-dual-fan-ra.png"
    },
    {
        "nombre": "Teclado Mecánico RGB",
        "precio": 75,
        "categoria": "Accesorios",
        "imagen": "https://static.vecteezy.com/system/resources/thumbnails/052/855/199/small/white-rgb-mechanical-gaming-keyboard-with-cable-free-png.png"
    },
    {
        "nombre": "Mouse Gamer RGB",
        "precio": 25,
        "categoria": "Accesorios",
        "imagen": "https://perfectchoice.me/cdn/shop/products/V-930143_A_05_Mouse-Videojuegos_Trapper-Luz-RGB_DPI_Gaming-Mouse_LED-RGB_1_800x.png?v=1763143743"
    },
    {
        "nombre": "Monitor 24\" 144Hz",
        "precio": 210,
        "categoria": "Monitores",
        "imagen": "https://gameon.store/cdn/shop/files/01-MainFrontImage.png?v=1756818774&width=1200"
    }
]

API_BASE_URL = os.getenv("RAILWAY_URL", "http://localhost:8000")

def _fetch_products_from_api():
    try:
        _resp = requests.get(f"{API_BASE_URL}/products/", params={"per_page": 100}, timeout=3)
        if _resp.status_code == 200:
            _data = _resp.json()
            if isinstance(_data, dict) and _data.get("products"):
                return _data["products"]
    except Exception:
        pass
    return None

def _product_key(p: dict) -> str:
    if not isinstance(p, dict):
        return ""
    return str(p.get("_id") or p.get("id") or p.get("nombre") or "")

if "productos" not in st.session_state:
    st.session_state.productos = productos

try:
    _api_products = _fetch_products_from_api()
    if _api_products:
        st.session_state.productos = _api_products
except Exception:
    pass

productos = st.session_state.productos

# -------- SIDEBAR --------
st.sidebar.title("🛒 ElectroShop")
pagina = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Productos", "Carrito", "Chatbot"]
)

# -------- PÁGINA INICIO --------
if pagina == "Inicio":
    st.title("💻 ElectroShop")
    st.subheader("Tu tienda de artículos electrónicos")
    st.write(
        "Encuentra memorias RAM, discos SSD, tarjetas gráficas y más."
    )

    st.image(
        "https://cdn-icons-png.flaticon.com/512/2777/2777142.png",
        width=200
    )

# -------- PÁGINA PRODUCTOS --------
elif pagina == "Productos":
    st.header("📦 Productos disponibles")
    
    # Mostrar mensaje si existe
    if st.session_state.mensaje:
        st.success(st.session_state.mensaje)
        st.session_state.mensaje = None

    if st.button("Actualizar productos"):
        _api_products = _fetch_products_from_api()
        if _api_products:
            st.session_state.productos = _api_products
            productos = st.session_state.productos
        st.rerun()

    categoria = st.selectbox(
        "Filtrar por categoría",
        ["Todos", "Memoria", "Almacenamiento", "Tarjetas Gráficas", "Accesorios", "Monitores"]
    )

    # Filtrar productos
    productos_filtrados = [p for p in productos if categoria == "Todos" or p["categoria"] == categoria]
    
    # Crear filas de 3 columnas
    for i in range(0, len(productos_filtrados), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(productos_filtrados):
                producto = productos_filtrados[i + j]
                with cols[j]:
                    st.image(producto["imagen"], width=250)
                    st.subheader(producto["nombre"])
                    st.caption(producto["categoria"])
                    st.write(f"💲 **${producto['precio']}**")

                    stock = producto.get("stock")
                    if stock is not None:
                        if stock <= 0:
                            st.error("Sin stock")
                        elif stock <= 5:
                            st.warning(f"Stock bajo: {stock}")
                        else:
                            st.write(f"Stock: {stock}")

                    disabled_add = stock is not None and stock <= 0
                    if st.button(
                        "Agregar 🛒",
                        key=f"add_{producto['nombre']}_{i}_{j}",
                        disabled=disabled_add,
                    ):
                        st.session_state.carrito.append(producto)
                        st.session_state.mensaje = f"✅ {producto['nombre']} agregado al carrito"
                        st.rerun()

# -------- PÁGINA CARRITO --------
elif pagina == "Carrito":
    st.header("🧾 Carrito de compras")

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío")
    else:
        grouped = {}
        order = []
        for p in st.session_state.carrito:
            k = _product_key(p)
            if k not in grouped:
                grouped[k] = {"producto": p, "qty": 0}
                order.append(k)
            grouped[k]["qty"] += 1

        total = 0
        for idx, k in enumerate(order):
            producto = grouped[k]["producto"]
            qty = grouped[k]["qty"]
            precio_unit = producto.get("precio", 0)

            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            with col1:
                st.write(f"✔ **{producto.get('nombre', '')}**")

            with col2:
                st.write(f"x{qty}")

            with col3:
                if st.button("➖", key=f"dec_{k}", help="Quitar 1"):
                    for i, item in enumerate(st.session_state.carrito):
                        if _product_key(item) == k:
                            del st.session_state.carrito[i]
                            break
                    st.rerun()

            stock = producto.get("stock")
            disabled_inc = stock is not None and qty >= stock
            with col4:
                if st.button("➕", key=f"inc_{k}", disabled=disabled_inc, help="Agregar 1"):
                    st.session_state.carrito.append(producto)
                    st.rerun()

            subtotal = float(precio_unit) * qty
            total += subtotal
            with col5:
                st.write(f"**${subtotal}**")

            if idx < len(order) - 1:
                st.divider()

        st.divider()
        st.subheader(f"💰 Total a pagar: ${total}")

        if st.button("Finalizar compra"):
            name_to_id = {}
            for p in productos:
                if isinstance(p, dict) and p.get("nombre") and (p.get("_id") or p.get("id")):
                    name_to_id[p["nombre"]] = p.get("_id") or p.get("id")

            counts = {}
            missing_ids = []
            for p in st.session_state.carrito:
                pid = p.get("_id") or p.get("id") or name_to_id.get(p.get("nombre", ""))
                if not pid:
                    missing_ids.append(p.get("nombre", "(sin nombre)"))
                    continue
                counts[pid] = counts.get(pid, 0) + 1

            ok = True
            if missing_ids:
                ok = False
                st.error("No se pudo actualizar stock para: " + ", ".join(missing_ids))
            else:
                for pid, qty in counts.items():
                    try:
                        r = requests.patch(
                            f"{API_BASE_URL}/products/{pid}/stock",
                            params={"stock_change": -qty},
                            timeout=5,
                        )
                        if r.status_code != 200:
                            ok = False
                            st.error(f"Error actualizando stock: {r.text}")
                    except Exception as e:
                        ok = False
                        st.error(f"Error conectando al backend: {e}")

            if ok:
                st.session_state.carrito.clear()
                st.success("Compra realizada con éxito 🎉")
                st.balloons()


# -------- CHATBOT--------
elif pagina == "Chatbot":
    st.header("🤖 Asistente Virtual ElectroShop")
    
    if st.button("Limpiar historial de chat"):
        st.session_state.chat_history = []
        st.rerun()

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
                resp = requests.post("http://127.0.0.1:8000/chat/", json={"question": prompt}, timeout=15)
                respuesta = resp.json().get("response", "Sin respuesta del servidor.")
            except Exception as e:
                respuesta = f"🔌 Error de conexión: {str(e)}"
            
            st.markdown(respuesta)
            st.session_state.chat_history.append(("assistant", respuesta))
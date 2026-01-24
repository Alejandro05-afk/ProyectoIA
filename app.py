import streamlit as st

# -------- CONFIGURACIÓN --------
st.set_page_config(
    page_title="ElectroShop",
    page_icon="💻",
    layout="wide"
)

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

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #00ADB5, #00868c) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    border: none !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #00c9d1, #00ADB5) !important;
    box-shadow: 0 0 15px rgba(0,173,181,0.6) !important;
    transform: scale(1.05) !important;
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

                    if st.button("Agregar 🛒", key=f"add_{producto['nombre']}_{i}_{j}"):
                        st.session_state.carrito.append(producto)
                        st.session_state.mensaje = f"✅ {producto['nombre']} agregado al carrito"
                        st.rerun()


# -------- PÁGINA CARRITO --------
elif pagina == "Carrito":
    st.header("🧾 Carrito de compras")

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío")
    else:
        total = 0
        
        for i, producto in enumerate(st.session_state.carrito):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"✔ **{producto['nombre']}**")
            with col2:
                st.write(f"**${producto['precio']}**")
            
            total += producto["precio"]
            
            if i < len(st.session_state.carrito) - 1:
                st.divider()

        st.divider()
        st.subheader(f"💰 Total a pagar: ${total}")

        if st.button("Finalizar compra"):
            st.session_state.carrito.clear()
            st.success("Compra realizada con éxito 🎉")
            st.balloons()

            
# -------- CHATBOT --------
elif pagina == "Chatbot":
    st.header("🤖 Chatbot de productos")

    pregunta = st.text_input(
        "Pregunta por un producto",
        placeholder="Ej: especificaciones de la RAM DDR4 16GB"
    )

    if st.button("Consultar"):
        st.info("Función chatbot pendiente de implementar")
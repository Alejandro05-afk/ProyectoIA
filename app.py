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

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #020617;
}

/* Tarjetas */
.product-card {
    background-color: #020617;
    padding: 16px;
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(0,173,181,0.4);
    margin-bottom: 25px;
}

/* Botones Streamlit */
.stButton > button {
    background-color: #00ADB5 !important;
    color: black !important;
    border-radius: 10px !important;
    font-weight: bold !important;
}

/* Títulos */
h1, h2, h3 {
    color: #00ADB5 !important;
}

</style>
""", unsafe_allow_html=True)



# -------- ESTADO --------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# -------- DATOS SIMULADOS --------
productos = [
    {
        "nombre": "RAM DDR4 16GB",
        "precio": 65,
        "categoria": "Memoria",
        "imagen": "https://mundodigitalecuador.com/wp-content/uploads/2024/04/16GB-3200.webp"
    },
    {
        "nombre": "RAM DDR5 32GB",
        "precio": 140,
        "categoria": "Memoria",
        "imagen": "https://mexx-img-2019.s3.amazonaws.com/Memoria-Ram-DDR5-32Gb-5200-Mhz-Kingston-Fury-Beast-Rgb_48229_2.jpeg"
    },
    {
        "nombre": "SSD NVMe 1TB",
        "precio": 90,
        "categoria": "Almacenamiento",
        "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR480w22CvszJE5JSJadSqXJD03oAofL580NA&s"
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
        "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkUwAox2YRhMeol7gBBsJcBZv6CcAjqMamWg&s"
    },
    {
        "nombre": "GPU RTX 4060",
        "precio": 420,
        "categoria": "Tarjetas Gráficas",
        "imagen": "https://m.media-amazon.com/images/I/61q0rsE3ezL._AC_SL1500_.jpg"
    },
    {
        "nombre": "GPU RTX 4070",
        "precio": 620,
        "categoria": "Tarjetas Gráficas",
        "imagen": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS2dR-aM1jnZRYt9z_aCbswQLWwzvjMKQcaqg&s"
    },
    {
        "nombre": "Teclado Mecánico RGB",
        "precio": 75,
        "categoria": "Accesorios",
        "imagen": "https://http2.mlstatic.com/D_NQ_NP_883123-MCO51096929263_082022-O.webp"
    },
    {
        "nombre": "Mouse Gamer RGB",
        "precio": 25,
        "categoria": "Accesorios",
        "imagen": "https://www.computron.com.ec/wp-content/uploads/2025/11/EZA-GM1029.webp"
    },
    {
        "nombre": "Monitor 24\" 144Hz",
        "precio": 210,
        "categoria": "Monitores",
        "imagen": "https://lavictoria.ec/wp-content/uploads/2023/01/ODYSSEY-MONITOR-SAMSUNG24-C24RG50FQL-3-600x600.jpg"
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

    categoria = st.selectbox(
        "Filtrar por categoría",
        ["Todos", "Memoria", "Almacenamiento", "Tarjetas Gráficas", "Accesorios", "Monitores"]
    )

    cols = st.columns(3)
    index = 0

    for producto in productos:
        if categoria == "Todos" or producto["categoria"] == categoria:
            with cols[index % 3]:

                st.markdown("<div class='product-card'>", unsafe_allow_html=True)

                st.image(producto["imagen"], use_container_width=True)
                st.subheader(producto["nombre"])
                st.caption(producto["categoria"])
                st.write(f"💲 **${producto['precio']}**")

                if st.button(
                    "Agregar 🛒",
                    key=f"add_{producto['nombre']}"
                ):
                    st.session_state.carrito.append(producto)
                    st.success("Producto agregado al carrito")

                st.markdown("</div>", unsafe_allow_html=True)

            index += 1



# -------- PÁGINA CARRITO --------
elif pagina == "Carrito":
    st.header("🧾 Carrito de compras")

    if not st.session_state.carrito:
        st.info("Tu carrito está vacío")
    else:
        total = 0
        for producto in st.session_state.carrito:
            st.write(
                f"✔ {producto['nombre']} - ${producto['precio']}"
            )
            total += producto["precio"]

        st.divider()
        st.subheader(f"💰 Total a pagar: ${total}")

        if st.button("Finalizar compra"):
            st.success("Compra realizada con éxito 🎉")
            st.session_state.carrito.clear()

            
#------------CHATBOT---------
elif pagina == "Chatbot":
    st.header("🤖 Chatbot de productos")

    pregunta = st.text_input(
        "Pregunta por un producto",
        placeholder="Ej: especificaciones de la RAM DDR4 16GB"
    )

    if st.button("Consultar"):
        respuesta = chatbot(pregunta)
        st.markdown(respuesta)

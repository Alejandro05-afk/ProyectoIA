import streamlit as st

# -------- CONFIGURACIÓN --------
st.set_page_config(
    page_title="ElectroShop",
    page_icon="💻",
    layout="wide"
)

# -------- ESTADO --------
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# -------- DATOS SIMULADOS --------
productos = [
    {"nombre": "RAM DDR4 16GB", "precio": 65, "categoria": "Memoria"},
    {"nombre": "RAM DDR5 32GB", "precio": 140, "categoria": "Memoria"},
    {"nombre": "SSD NVMe 1TB", "precio": 90, "categoria": "Almacenamiento"},
    {"nombre": "HDD 2TB", "precio": 70, "categoria": "Almacenamiento"},
    {"nombre": "GPU RTX 4060", "precio": 420, "categoria": "Tarjetas Gráficas"},
    {"nombre": "Mouse Gamer", "precio": 25, "categoria": "Accesorios"},
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
        ["Todos", "Memoria", "Almacenamiento", "Tarjetas Gráficas", "Accesorios"]
    )

    cols = st.columns(3)

    for i, producto in enumerate(productos):
        if categoria == "Todos" or producto["categoria"] == categoria:
            with cols[i % 3]:
                st.subheader(producto["nombre"])
                st.write(f"Categoría: {producto['categoria']}")
                st.write(f"💲 Precio: ${producto['precio']}")

                if st.button(
                    f"Agregar 🛒",
                    key=producto["nombre"]
                ):
                    st.session_state.carrito.append(producto)
                    st.success("Producto agregado al carrito")

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

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from datetime import datetime
from bson import ObjectId

# Datos de productos para Atlas
PRODUCTOS_DATA = [
    {
        "nombre": "RAM DDR4 16GB",
        "precio": 65.0,
        "categoria": "Memoria",
        "imagen": "https://nomadaware.com.ec/wp-content/uploads/VENG_LPX_BLK_01.png",
        "descripcion": "Memoria Corsair Vengeance LPX de 16GB (2x8GB) a 3200MHz. Latencia CL16, disipador de aluminio puro, ideal para overclocking y gaming estable.",
        "stock": 50
    },
    {
        "nombre": "RAM DDR5 32GB",
        "precio": 140.0,
        "categoria": "Memoria",
        "imagen": "https://static.gigabyte.com/StaticFile/Image/Global/fe5413eea1b1be5c580a8c6a1945efb9/Product/30681",
        "descripcion": "Kit DDR5 de 32GB a 5200MHz. Mayor ancho de banda y eficiencia con gestión de energía integrada (PMIC) y On-die ECC para corrección de errores.",
        "stock": 30
    },
    {
        "nombre": "GIGABYTE SSD NVMe 1TB OARUS",
        "precio": 90.0,
        "categoria": "Almacenamiento",
        "imagen": "https://static.gigabyte.com/StaticFile/Image/Global/13fdaa6e6dc982d0753d32c70c23d92c/Product/30161",
        "descripcion": "SSD Gen4 con velocidades de lectura de hasta 5000MB/s. Factor de forma M.2 2280, ideal para reducir tiempos de carga en juegos y software pesado.",
        "stock": 40
    },
    {
        "nombre": "SSD SATA 512GB",
        "precio": 55.0,
        "categoria": "Almacenamiento",
        "imagen": "https://toners.ec/wp-content/uploads/2024/09/disco-solido-adata-512-gb-su650-ssd-azul-25-sata.png",
        "descripcion": "Unidad de estado sólido de 512GB con interfaz SATA III. Mejora el rendimiento de laptops antiguas con velocidades 10 veces superiores a un HDD.",
        "stock": 60
    },
    {
        "nombre": "HDD 2TB",
        "precio": 70.0,
        "categoria": "Almacenamiento",
        "imagen": "https://nanotroniconline.com/wp-content/uploads/2020/08/disco-duro-hdd-western-digital-blue-2tb-7200rpm-nanotronic.png",
        "descripcion": "Disco duro Western Digital Blue de 2TB a 7200RPM. Excelente para almacenamiento masivo de archivos, videos y copias de seguridad de largo plazo.",
        "stock": 25
    },
    {
        "nombre": "GPU RTX 4060",
        "precio": 420.0,
        "categoria": "Tarjetas Gráficas",
        "imagen": "https://d2vfia6k6wrouk.cloudfront.net/productimages/6a308493-0e0b-4aff-b164-b00600f6f3f9/images/pny-rtx-4060-ti-8gb-verto-dual-fan-ra.png",
        "descripcion": "NVIDIA GeForce RTX 4060 con 8GB GDDR6. Arquitectura Ada Lovelace, núcleos Tensor de 4ta gen para DLSS 3 y Ray Tracing en tiempo real.",
        "stock": 15
    },
    {
        "nombre": "Teclado Mecánico RGB",
        "precio": 75.0,
        "categoria": "Accesorios",
        "imagen": "https://static.vecteezy.com/system/resources/thumbnails/052/855/199/small/white-rgb-mechanical-gaming-keyboard-with-cable-free-png.png",
        "descripcion": "Teclado mecánico con switches Blue para respuesta táctil precisa. Iluminación RGB personalizable, anti-ghosting completo y diseño ergonómico.",
        "stock": 35
    },
    {
        "nombre": "Mouse Gamer RGB",
        "precio": 25.0,
        "categoria": "Accesorios",
        "imagen": "https://perfectchoice.me/cdn/shop/products/V-930143_A_05_Mouse-Videojuegos_Trapper-Luz-RGB_DPI_Gaming-Mouse_LED-RGB_1_800x.png?v=1763143743",
        "descripcion": "Mouse óptico de alta precisión con hasta 7200 DPI ajustables. 6 botones programables y luces RGB dinámicas para sesiones de juego intensas.",
        "stock": 50
    },
    {
        "nombre": "Monitor 24\" 144Hz",
        "precio": 210.0,
        "categoria": "Monitores",
        "imagen": "https://gameon.store/cdn/shop/files/01-MainFrontImage.png?v=1756818774&width=1200",
        "descripcion": "Pantalla Full HD de 24 pulgadas con panel IPS. Tasa de refresco de 144Hz y 1ms de respuesta. Colores vibrantes y fluidez total para eSports.",
        "stock": 20
    }
]

async def initialize_atlas_data():
    """Inicializar datos en MongoDB Atlas para producción"""
    
    print("🚀 Inicializando datos en MongoDB Atlas...")
    
    # Usar variable de entorno o URL por defecto para Atlas
    import os
    atlas_url = os.getenv("MONGODB_URL", "mongodb+srv://kogamaandres_db_user:fwsAYpZWhHb6Anq1@electroshop.q0k2ovr.mongodb.net/electroshop?retryWrites=true&w=majority")
    
    try:
        # Conectar a Atlas con timeout extendido
        print("⏳ Conectando a Atlas...")
        client = AsyncIOMotorClient(atlas_url, serverSelectionTimeoutMS=30000)
        
        # Probar conexión
        await client.admin.command('ping')
        print("✅ Conexión exitosa a Atlas")
        
        # Obtener base de datos y colección
        db = client.electroshop
        collection = db.electroshop
        
        # Verificar si ya hay datos
        count = await collection.count_documents({})
        if count > 0:
            print(f"📊 Ya existen {count} productos en Atlas")
            return
        
        # Agregar timestamps y preparar productos
        now = datetime.utcnow()
        for product in PRODUCTOS_DATA:
            product['created_at'] = now
            product['updated_at'] = now
        
        # Insertar productos
        result = await collection.insert_many(PRODUCTOS_DATA)
        print(f"✅ Insertados {len(result.inserted_ids)} productos en Atlas")
        
        # Crear índices
        await collection.create_index([("nombre", ASCENDING)])
        await collection.create_index([("categoria", ASCENDING)])
        await collection.create_index([("precio", ASCENDING)])
        print("📊 Índices creados exitosamente")
        
        # Verificación
        final_count = await collection.count_documents({})
        print(f"🔍 Verificación: {final_count} productos en Atlas")
        
        # Mostrar resumen
        print("\n📋 Productos inicializados en Atlas:")
        for product in PRODUCTOS_DATA:
            print(f"  - {product['nombre']}: ${product['precio']} (Stock: {product['stock']})")
        
    except Exception as e:
        print(f"❌ Error inicializando Atlas: {e}")
        raise
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(initialize_atlas_data())

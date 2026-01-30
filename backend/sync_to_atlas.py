import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
import json

# Configuración
LOCAL_URL = "mongodb://localhost:27017"
ATLAS_URL = "mongodb+srv://kogamaandres_db_user:fwsAYpZWhHb6Anq1@electroshop.q0k2ovr.mongodb.net/electroshop?retryWrites=true&w=majority"
DATABASE_NAME = "electroshop"
COLLECTION_NAME = "electroshop"

async def sync_to_atlas():
    """Sincronizar datos desde MongoDB local a Atlas"""
    
    print("🔄 Iniciando sincronización con MongoDB Atlas...")
    
    # Conectar a MongoDB local
    try:
        local_client = AsyncIOMotorClient(LOCAL_URL)
        local_db = local_client[DATABASE_NAME]
        local_collection = local_db[COLLECTION_NAME]
        print("✅ Conectado a MongoDB local")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB local: {e}")
        return
    
    # Conectar a MongoDB Atlas
    try:
        atlas_client = AsyncIOMotorClient(ATLAS_URL, serverSelectionTimeoutMS=30000)
        atlas_db = atlas_client[DATABASE_NAME]
        atlas_collection = atlas_db[COLLECTION_NAME]
        print("✅ Conectado a MongoDB Atlas")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB Atlas: {e}")
        return
    
    try:
        # Obtener todos los productos de MongoDB local
        products = await local_collection.find({}).to_list(length=None)
        print(f"📦 Encontrados {len(products)} productos en MongoDB local")
        
        # Limpiar colección en Atlas
        await atlas_collection.delete_many({})
        print("🧹 Colección en Atlas limpiada")
        
        # Insertar productos en Atlas
        if products:
            result = await atlas_collection.insert_many(products)
            print(f"✅ Insertados {len(result.inserted_ids)} productos en Atlas")
            
            # Crear índices en Atlas
            await atlas_collection.create_index([("nombre", ASCENDING)])
            await atlas_collection.create_index([("categoria", ASCENDING)])
            await atlas_collection.create_index([("precio", ASCENDING)])
            print("📊 Índices creados en Atlas")
            
            # Mostrar resumen
            print("\n📋 Resumen de productos sincronizados:")
            for product in products:
                print(f"  - {product['nombre']}: ${product['precio']} (Stock: {product['stock']})")
        else:
            print("⚠️ No hay productos para sincronizar")
            
    except Exception as e:
        print(f"❌ Error durante la sincronización: {e}")
    
    finally:
        # Cerrar conexiones
        local_client.close()
        atlas_client.close()
        print("🔌 Conexiones cerradas")

if __name__ == "__main__":
    asyncio.run(sync_to_atlas())

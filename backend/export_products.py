import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json
from datetime import datetime

# Configuración
LOCAL_URL = "mongodb://localhost:27017"
DATABASE_NAME = "electroshop"
COLLECTION_NAME = "electroshop"

async def export_products():
    """Exportar productos desde MongoDB local a JSON"""
    
    print("📤 Exportando productos desde MongoDB local...")
    
    try:
        # Conectar a MongoDB local
        client = AsyncIOMotorClient(LOCAL_URL)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Obtener todos los productos
        products = await collection.find({}).to_list(length=None)
        
        # Convertir ObjectId a string para JSON
        for product in products:
            if '_id' in product:
                product['_id'] = str(product['_id'])
            if 'created_at' in product and product['created_at']:
                product['created_at'] = product['created_at'].isoformat()
            if 'updated_at' in product and product['updated_at']:
                product['updated_at'] = product['updated_at'].isoformat()
        
        # Guardar a archivo JSON
        with open('products_export.json', 'w', encoding='utf-8') as f:
            json.dump({
                'database': DATABASE_NAME,
                'collection': COLLECTION_NAME,
                'export_date': datetime.now().isoformat(),
                'total_products': len(products),
                'products': products
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exportados {len(products)} productos a products_export.json")
        
        # Mostrar resumen
        print("\n📋 Productos exportados:")
        for i, product in enumerate(products, 1):
            print(f"  {i}. {product['nombre']}: ${product['precio']} (Stock: {product['stock']})")
        
    except Exception as e:
        print(f"❌ Error exportando productos: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(export_products())

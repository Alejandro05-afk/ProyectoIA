import pymongo
from pymongo import MongoClient
import json
from datetime import datetime
from bson import ObjectId

# Configuración Atlas con timeout extendido
ATLAS_URL = "mongodb+srv://kogamaandres_db_user:fwsAYpZWhHb6Anq1@electroshop.q0k2ovr.mongodb.net/electroshop?retryWrites=true&w=majority&connectTimeoutMS=60000&socketTimeoutMS=60000&serverSelectionTimeoutMS=60000"

def import_to_atlas():
    """Importar productos a MongoDB Atlas usando pymongo síncrono"""
    
    print("🚀 Importando productos a MongoDB Atlas...")
    
    try:
        # Conectar a Atlas con timeout extendido
        print("⏳ Conectando a Atlas...")
        client = MongoClient(ATLAS_URL, serverSelectionTimeoutMS=60000)
        
        # Probar conexión
        client.admin.command('ping')
        print("✅ Conexión exitosa a Atlas")
        
        # Obtener base de datos y colección
        db = client.electroshop
        collection = db.electroshop
        
        # Cargar datos del archivo JSON
        with open('products_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        products = data['products']
        print(f"📦 Cargados {len(products)} productos desde JSON")
        
        # Limpiar colección existente
        result = collection.delete_many({})
        print(f"🧹 Eliminados {result.deleted_count} documentos existentes")
        
        # Preparar productos para inserción
        products_to_insert = []
        for product in products:
            # Convertir _id de string a ObjectId si es necesario
            if '_id' in product:
                try:
                    product['_id'] = ObjectId(product['_id'])
                except:
                    # Si no es un ObjectId válido, dejarlo como string o generar nuevo
                    del product['_id']
            
            # Convertir fechas si es necesario
            if 'created_at' in product and product['created_at']:
                try:
                    product['created_at'] = datetime.fromisoformat(product['created_at'].replace('Z', '+00:00'))
                except:
                    pass
            
            if 'updated_at' in product and product['updated_at']:
                try:
                    product['updated_at'] = datetime.fromisoformat(product['updated_at'].replace('Z', '+00:00'))
                except:
                    pass
            
            products_to_insert.append(product)
        
        # Insertar productos
        if products_to_insert:
            result = collection.insert_many(products_to_insert)
            print(f"✅ Insertados {len(result.inserted_ids)} productos en Atlas")
            
            # Crear índices
            collection.create_index([("nombre", pymongo.ASCENDING)])
            collection.create_index([("categoria", pymongo.ASCENDING)])
            collection.create_index([("precio", pymongo.ASCENDING)])
            print("📊 Índices creados exitosamente")
            
            # Verificar inserción
            count = collection.count_documents({})
            print(f"🔍 Verificación: {count} productos en Atlas")
            
            # Mostrar algunos productos
            print("\n📋 Productos en Atlas:")
            for product in collection.find({}).limit(3):
                print(f"  - {product['nombre']}: ${product['precio']} (Stock: {product['stock']})")
        
        else:
            print("⚠️ No hay productos para insertar")
            
    except Exception as e:
        print(f"❌ Error durante la importación: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'client' in locals():
            client.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    import_to_atlas()

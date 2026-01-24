from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from typing import Optional
import os

# Configuración de la base de datos
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "electroshop"
COLLECTION_NAME = "electroshop"

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect_to_mongodb(cls):
        """Conectar a MongoDB"""
        cls.client = AsyncIOMotorClient(MONGODB_URL)
        cls.database = cls.client[DATABASE_NAME]
        
        # Crear índices para mejor rendimiento
        await cls.database[COLLECTION_NAME].create_index([("nombre", ASCENDING)])
        await cls.database[COLLECTION_NAME].create_index([("categoria", ASCENDING)])
        await cls.database[COLLECTION_NAME].create_index([("precio", ASCENDING)])
        
        print(f"✅ Conectado a MongoDB: {MONGODB_URL}")
        print(f"📊 Base de datos: {DATABASE_NAME}")
        print(f"📁 Colección: {COLLECTION_NAME}")

    @classmethod
    async def disconnect_from_mongodb(cls):
        """Desconectar de MongoDB"""
        if cls.client:
            cls.client.close()
            print("🔌 Desconectado de MongoDB")

    @classmethod
    def get_collection(cls):
        """Obtener la colección de productos"""
        if cls.database is None:
            raise RuntimeError("La base de datos no está conectada. Llama a connect_to_mongodb() primero.")
        return cls.database[COLLECTION_NAME]


def get_collection():
    return Database.get_collection()

# Instancia global de la base de datos
db = Database()

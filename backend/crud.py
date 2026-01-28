from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId

from database import Database
from models import ProductCreate, ProductUpdate, ProductResponse, INITIAL_PRODUCTS

class ProductCRUD:
    def __init__(self):
        pass

    def _collection(self):
        return Database.get_collection()

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        collection = self._collection()
        product_dict = product.model_dump()
        product_dict["created_at"] = datetime.now(timezone.utc)
        product_dict["updated_at"] = datetime.now(timezone.utc)
        
        result = await collection.insert_one(product_dict)
        created_product = await collection.find_one({"_id": result.inserted_id})
        return ProductResponse(**created_product)

    async def get_product_by_id(self, product_id: str) -> Optional[ProductResponse]:
        collection = self._collection()
        try:
            obj_id = ObjectId(product_id)
            product = await collection.find_one({"_id": obj_id})
            if product:
                return ProductResponse(**product)
        except Exception:
            pass
        return None

    async def get_products(self, skip: int = 0, limit: int = 100, categoria: Optional[str] = None, 
                          precio_min: Optional[float] = None, precio_max: Optional[float] = None, 
                          search: Optional[str] = None, sort_by: str = "created_at", sort_order: int = -1) -> tuple[List[ProductResponse], int]:
        collection = self._collection()
        query = {}
        
        if categoria:
            query["categoria"] = categoria
            
        if precio_min is not None or precio_max is not None:
            query["precio"] = {}
            if precio_min is not None:
                query["precio"]["$gte"] = precio_min
            if precio_max is not None:
                query["precio"]["$lte"] = precio_max
                
        if search:
            query["$or"] = [
                {"nombre": {"$regex": search, "$options": "i"}},
                {"descripcion": {"$regex": search, "$options": "i"}}
            ]

        total_count = await collection.count_documents(query)
        cursor = collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        
        products = []
        async for product in cursor:
            products.append(ProductResponse(**product))
            
        return products, total_count

    async def update_product(self, product_id: str, product_update: ProductUpdate) -> Optional[ProductResponse]:
        collection = self._collection()
        try:
            obj_id = ObjectId(product_id)
            update_dict = {"updated_at": datetime.now(timezone.utc)}
            update_data = product_update.model_dump(exclude_unset=True)
            update_dict.update(update_data)
            
            result = await collection.update_one({"_id": obj_id}, {"$set": update_dict})
            
            if result.modified_count > 0:
                updated_product = await collection.find_one({"_id": obj_id})
                return ProductResponse(**updated_product)
        except Exception:
            pass
        return None

    async def delete_product(self, product_id: str) -> bool:
        collection = self._collection()
        try:
            obj_id = ObjectId(product_id)
            result = await collection.delete_one({"_id": obj_id})
            return result.deleted_count > 0
        except Exception:
            return False

    async def get_categories(self) -> List[str]:
        collection = self._collection()
        categories = await collection.distinct("categoria")
        return sorted(categories)

    async def initialize_products(self) -> int:
        """Inicializar y actualizar la base de datos con descripciones mejoradas"""
        collection = self._collection()
        
        for product_data in INITIAL_PRODUCTS:
            now = datetime.now(timezone.utc)
            doc = dict(product_data)
            doc["updated_at"] = now
            
            await collection.update_one(
                {"nombre": doc["nombre"]},
                {
                    "$set": doc, 
                    "$setOnInsert": {"created_at": now}
                },
                upsert=True
            )

        return await collection.count_documents({})

# Instancia global del CRUD
product_crud = ProductCRUD()

import sys
import os
sys.path.append(os.path.dirname(__file__))  # Agrega la carpeta backend al path


from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from contextlib import asynccontextmanager

from database import Database
from models import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from crud import product_crud

from chatbot import IAAssistant
from pydantic import BaseModel

chatbot_service = IAAssistant()

class ChatRequest(BaseModel):
    question: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Iniciar la aplicación
    await Database.connect_to_mongodb()
    yield
    # Cerrar la aplicación
    await Database.disconnect_from_mongodb()

app = FastAPI(
    title="ElectroShop API",
    description="API para gestión de productos de ElectroShop",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenido a la API de ElectroShop", "version": "1.0.0"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.post("/products/", response_model=ProductResponse, tags=["Products"])
async def create_product(product: ProductCreate):
    """Crear un nuevo producto"""
    try:
        return await product_crud.create_product(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/products/", response_model=ProductListResponse, tags=["Products"])
async def get_products(
    page: int = Query(1, ge=1, description="Número de página"),
    per_page: int = Query(20, ge=1, le=100, description="Productos por página"),
    categoria: Optional[str] = Query(None, description="Filtrar por categoría"),
    precio_min: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    search: Optional[str] = Query(None, description="Buscar en nombre y descripción"),
    sort_by: str = Query("created_at", description="Campo para ordenar"),
    sort_order: int = Query(-1, ge=-1, le=1, description="Orden: -1 descendente, 1 ascendente")
):
    """Obtener productos con filtros y paginación"""
    try:
        skip = (page - 1) * per_page
        products, total_count = await product_crud.get_products(
            skip=skip,
            limit=per_page,
            categoria=categoria,
            precio_min=precio_min,
            precio_max=precio_max,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        has_next = skip + per_page < total_count
        has_prev = page > 1
        
        return ProductListResponse(
            products=products,
            total_count=total_count,
            page=page,
            per_page=per_page,
            has_next=has_next,
            has_prev=has_prev
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def get_product(product_id: str):
    """Obtener un producto por su ID"""
    product = await product_crud.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
async def update_product(product_id: str, product_update: ProductUpdate):
    """Actualizar un producto"""
    product = await product_crud.update_product(product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


@app.patch("/products/{product_id}/stock", response_model=ProductResponse, tags=["Products"])
async def update_product_stock(
    product_id: str,
    stock_change: int = Query(..., description="Cambio de stock (positivo suma, negativo resta)"),
):
    product = await product_crud.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    new_stock = product.stock + stock_change
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    updated = await product_crud.update_product(product_id, ProductUpdate(stock=new_stock))
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return updated

@app.delete("/products/{product_id}", tags=["Products"])
async def delete_product(product_id: str):
    """Eliminar un producto"""
    success = await product_crud.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}

@app.get("/categories/", response_model=List[str], tags=["Products"])
async def get_categories():
    """Obtener todas las categorías disponibles"""
    try:
        return await product_crud.get_categories()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/initialize/", tags=["Products"])
async def initialize_products():
    """Inicializar la base de datos con productos por defecto"""
    try:
        count = await product_crud.initialize_products()
        return {"message": f"Se inicializaron {count} productos"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/chat/", tags=["Chatbot"])
async def chat_endpoint(request: ChatRequest):
    products, _ = await product_crud.get_products(limit=20)

    contexto = "\n".join([
        f"- {p.nombre}: ${p.precio}. Stock: {p.stock}. Info técnica: {p.descripcion}" 
        for p in products
    ])
    
    respuesta = chatbot_service.responder(request.question, contexto_productos=contexto)
    return {"response": respuesta}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

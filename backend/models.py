from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from pydantic import ConfigDict
from pydantic import field_validator

class ProductBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    precio: float = Field(..., gt=0)
    categoria: str = Field(..., min_length=1, max_length=50)
    imagen: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1, max_length=500)
    stock: int = Field(..., ge=0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    categoria: Optional[str] = Field(None, min_length=1, max_length=50)
    imagen: Optional[str] = Field(None, min_length=1)
    descripcion: Optional[str] = Field(None, min_length=1, max_length=500)
    stock: Optional[int] = Field(None, ge=0)

class ProductResponse(ProductBase):
    id: Optional[str] = Field(alias="_id", default=None)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("id", mode="before")
    @classmethod
    def _coerce_objectid(cls, v):
        if v is None:
            return v
        return str(v)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
    )

class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total_count: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool

# Datos iniciales de productos
INITIAL_PRODUCTS = [
    {
        "nombre": "RAM DDR4 16GB",
        "precio": 65.0,
        "categoria": "Memoria",
        "imagen": "https://nomadaware.com.ec/wp-content/uploads/VENG_LPX_BLK_01.png",
        "descripcion": "Producto de ElectroShop",
        "stock": 50
    },
    {
        "nombre": "RAM DDR5 32GB",
        "precio": 140.0,
        "categoria": "Memoria",
        "imagen": "https://static.gigabyte.com/StaticFile/Image/Global/fe5413eea1b1be5c580a8c6a1945efb9/Product/30681",
        "descripcion": "Producto de ElectroShop",
        "stock": 30
    },
    {
        "nombre": "GIGABYTE SSD NVMe 1TB OARUS",
        "precio": 90.0,
        "categoria": "Almacenamiento",
        "imagen": "https://static.gigabyte.com/StaticFile/Image/Global/13fdaa6e6dc982d0753d32c70c23d92c/Product/30161",
        "descripcion": "Producto de ElectroShop",
        "stock": 40
    },
    {
        "nombre": "SSD SATA 512GB",
        "precio": 55.0,
        "categoria": "Almacenamiento",
        "imagen": "https://toners.ec/wp-content/uploads/2024/09/disco-solido-adata-512-gb-su650-ssd-azul-25-sata.png",
        "descripcion": "Producto de ElectroShop",
        "stock": 60
    },
    {
        "nombre": "HDD 2TB",
        "precio": 70.0,
        "categoria": "Almacenamiento",
        "imagen": "https://nanotroniconline.com/wp-content/uploads/2020/08/disco-duro-hdd-western-digital-blue-2tb-7200rpm-nanotronic.png",
        "descripcion": "Producto de ElectroShop",
        "stock": 25
    },
    {
        "nombre": "GPU RTX 4060",
        "precio": 420.0,
        "categoria": "Tarjetas Gráficas",
        "imagen": "https://d2vfia6k6wrouk.cloudfront.net/productimages/6a308493-0e0b-4aff-b164-b00600f6f3f9/images/pny-rtx-4060-ti-8gb-verto-dual-fan-ra.png",
        "descripcion": "Producto de ElectroShop",
        "stock": 15
    },
    {
        "nombre": "Teclado Mecánico RGB",
        "precio": 75.0,
        "categoria": "Accesorios",
        "imagen": "https://static.vecteezy.com/system/resources/thumbnails/052/855/199/small/white-rgb-mechanical-gaming-keyboard-with-cable-free-png.png",
        "descripcion": "Producto de ElectroShop",
        "stock": 35
    },
    {
        "nombre": "Mouse Gamer RGB",
        "precio": 25.0,
        "categoria": "Accesorios",
        "imagen": "https://perfectchoice.me/cdn/shop/products/V-930143_A_05_Mouse-Videojuegos_Trapper-Luz-RGB_DPI_Gaming-Mouse_LED-RGB_1_800x.png?v=1763143743",
        "descripcion": "Producto de ElectroShop",
        "stock": 50
    },
    {
        "nombre": "Monitor 24\" 144Hz",
        "precio": 210.0,
        "categoria": "Monitores",
        "imagen": "https://gameon.store/cdn/shop/files/01-MainFrontImage.png?v=1756818774&width=1200",
        "descripcion": "Producto de ElectroShop",
        "stock": 20
    }
]

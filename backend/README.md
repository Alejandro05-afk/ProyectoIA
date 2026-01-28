# ElectroShop Backend API

Backend FastAPI con MongoDB para la gestión de productos de ElectroShop.

## 🚀 Características

- ✅ API RESTful con FastAPI
- ✅ Base de datos MongoDB
- ✅ CRUD completo de productos
- ✅ Filtros avanzados (categoría, precio, búsqueda)
- ✅ Paginación y ordenamiento
- ✅ Validación de datos con Pydantic
- ✅ Documentación automática con Swagger
- ✅ CORS configurado

## 📋 Requisitos

- Python 3.8+
- MongoDB corriendo en localhost:27017
- Pip

## 🛠️ Instalación

1. **Clonar el repositorio y navegar al backend:**
```bash
cd backend
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
```

3. **Activar entorno virtual:**
```bash
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

## 🗄️ Configuración de MongoDB

Asegúrate de que MongoDB esté corriendo:

```bash
# Windows
mongod

# Linux/Mac
sudo systemctl start mongod

# Docker
docker run -d -p 27017:27017 --name mongodb mongo
```

La aplicación se conectará a `mongodb://localhost:27017` y usará la base de datos `electroshop`.

## 🚀 Ejecución

### Desarrollo
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 Documentación

Una vez iniciado el servidor, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 Endpoints

### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Verificar estado del servidor |
| POST | `/products/` | Crear producto |
| GET | `/products/` | Listar productos (con filtros) |
| GET | `/products/{id}` | Obtener producto por ID |
| PUT | `/products/{id}` | Actualizar producto |
| DELETE | `/products/{id}` | Eliminar producto |
| GET | `/categories/` | Obtener categorías |
| POST | `/initialize/` | Inicializar productos por defecto |

### Filtros de productos

Puedes usar los siguientes query parameters en `GET /products/`:

- `page`: Número de página (default: 1)
- `per_page`: Productos por página (default: 20, max: 100)
- `categoria`: Filtrar por categoría
- `precio_min`: Precio mínimo
- `precio_max`: Precio máximo
- `search`: Buscar en nombre y descripción
- `sort_by`: Campo para ordenar (default: created_at)
- `sort_order`: Orden (-1 descendente, 1 ascendente)

### Ejemplos de uso

```bash
# Obtener todos los productos
curl http://localhost:8000/products/

# Filtrar por categoría
curl "http://localhost:8000/products/?categoria=Memoria"

# Buscar productos
curl "http://localhost:8000/products/?search=RAM"

# Filtrar por precio
curl "http://localhost:8000/products/?precio_min=50&precio_max=200"

# Paginación
curl "http://localhost:8000/products/?page=2&per_page=5"

# Crear un producto
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Producto Test",
    "precio": 100.0,
    "categoria": "Test",
    "imagen": "https://example.com/image.jpg",
    "descripcion": "Descripción del producto",
    "stock": 10
  }'

# Inicializar productos por defecto
curl -X POST "http://localhost:8000/initialize/"
```

## 📊 Modelo de Datos

### Producto
```json
{
  "_id": "ObjectId",
  "nombre": "string",
  "precio": "number",
  "categoria": "string",
  "imagen": "string",
  "descripcion": "string",
  "stock": "number",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🧪 Pruebas

Para probar la API, puedes usar:

1. **Swagger UI**: `http://localhost:8000/docs`
2. **curl**: Ver ejemplos arriba
3. **Postman**: Importar la colección desde Swagger

## 🏗️ Estructura del Proyecto

```
backend/
├── main.py              # Aplicación FastAPI principal
├── database.py          # Conexión a MongoDB
├── models.py            # Modelos Pydantic
├── crud.py              # Operaciones CRUD
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## 🔧 Variables de Entorno

Opcionalmente puedes configurar:

```bash
# URL de MongoDB (default: mongodb://localhost:27017)
MONGODB_URL=mongodb://localhost:27017
```

## 🚨 Errores Comunes

1. **MongoDB no está corriendo**: Asegúrate de que MongoDB esté iniciado
2. **Puerto en uso**: Cambia el puerto si 8000 está ocupado
3. **Permisos**: Ejecuta con permisos suficientes

## 📝 Licencia

MIT License

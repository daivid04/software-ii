from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import SessionLocal
from schemas.producto_schema import ProductoCreate, ProductoResponse
from services.producto_service import ProductoService
from core.auth import require_supabase_user

router = APIRouter(tags=["Productos"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 

def get_producto_service(db: Session = Depends(get_db)) -> ProductoService:
    return ProductoService(db)

@router.post("/", response_model=ProductoResponse, dependencies=[Depends(require_supabase_user)], summary="Crear nuevo producto")
def create_producto(
    data: ProductoCreate,
    service: ProductoService = Depends(get_producto_service)
):
    """
    Crea un nuevo producto en el inventario.
    
    Este endpoint permite registrar productos estándar (no autopartes) con validaciones completas.
    
    **Validaciones:**
    - Nombre: Mínimo 3 caracteres, máximo 200
    - Marca: Mínimo 2 caracteres, máximo 100
    - Descripción: Mínimo 10 caracteres, máximo 500
    - Precio de venta: Debe ser mayor al precio de compra
    - Stock: No puede ser negativo
    - Código de barras: Único en el sistema
    
    **Ejemplo de Request correcto:**
    ```json
    {
        "nombre": "Filtro de Aceite Premium",
        "marca": "Bosch",
        "descripcion": "Filtro de aceite de alta calidad para motores de 4 cilindros, compatible con múltiples marcas",
        "precio_compra": 150.00,
        "precio_venta": 250.00,
        "stock": 25,
        "imagen_url": "https://example.com/filtro.jpg",
        "cod_barras": "T-P001-FIL"
    }
    ```
    
    **Response exitosa:**
    ```json
    {
        "id": 15,
        "nombre": "Filtro de Aceite Premium",
        "marca": "Bosch",
        "descripcion": "Filtro de aceite de alta calidad...",
        "precio_compra": 150.00,
        "precio_venta": 250.00,
        "stock": 25,
        "imagen_url": "https://example.com/filtro.jpg",
        "cod_barras": "T-P001-FIL",
        "tipo": "producto"
    }
    ```
    
    
    **Ejemplos de Requests incorrectos:**
    
    1. Precio de venta menor o igual al de compra:
    ```json
    {
        "nombre": "Producto Test",
        "precio_compra": 300.00,
        "precio_venta": 250.00  // Debe ser > precio_compra
    }
    ```
    **Error:** `400 Bad Request - "Precio de venta debe ser mayor al precio de compra"`
    
    
    2. Descripción muy corta:
    ```json
    {
        "nombre": "Producto Test",
        "descripcion": "Corta"  // Mínimo 10 caracteres
    }
    ```
    **Error:** `400 Bad Request - "La descripción debe tener al menos 10 caracteres"`
    
    
    3. Código de barras duplicado:
    ```json
    {
        "nombre": "Producto Test",
        "cod_barras": "T-P001-FIL"  // Ya existe
    }
    ```
    **Error:** `400 Bad Request - "El código de barras ya existe"`
    
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    try:
        return service.create_producto(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/", response_model=list[ProductoResponse], summary="Listar todos los productos")
def list_productos(
    service: ProductoService = Depends(get_producto_service)
):
    """
    Obtiene el listado completo de productos.
    
    Retorna todos los productos registrados en el inventario (excluyendo autopartes).
    Los productos se retornan ordenados por ID descendente (más recientes primero).
    
    **Response exitosa:**
    ```json
    [
        {
            "id": 15,
            "nombre": "Filtro de Aceite Premium",
            "marca": "Bosch",
            "descripcion": "Filtro de alta calidad...",
            "precio_compra": 150.00,
            "precio_venta": 250.00,
            "stock": 25,
            "imagen_url": "https://example.com/filtro.jpg",
            "cod_barras": "T-P001-FIL",
            "tipo": "producto"
        },
        {
            "id": 14,
            "nombre": "Aceite Motor 5W-30",
            "marca": "Castrol",
            "descripcion": "Aceite sintético premium...",
            "precio_compra": 250.00,
            "precio_venta": 400.00,
            "stock": 50,
            "imagen_url": null,
            "cod_barras": "T-P002-ACE",
            "tipo": "producto"
        }
    ]
    ```
    
    
    **Campos retornados:**
    - **id**: Identificador único del producto
    - **nombre**: Nombre del producto
    - **marca**: Marca del producto
    - **descripcion**: Descripción detallada
    - **precio_compra**: Precio al que se compró
    - **precio_venta**: Precio al público
    - **stock**: Cantidad disponible
    - **imagen_url**: URL de la imagen (puede ser null)
    - **cod_barras**: Código único del producto
    - **tipo**: Siempre "producto" (no incluye autopartes)
    
    **Autenticación:
    No requiere autenticación (público)
    """
    return service.list_productos()


@router.get("/barcode/{codBarras}", response_model=ProductoResponse, summary="Buscar producto por código de barras")
def get_producto_by_barcode(codBarras: str, service: ProductoService = Depends(get_producto_service)):
    """
    Busca un producto usando su código de barras.
    
    Endpoint útil para lectores de código de barras en el punto de venta.
    
    **Parámetros:**
    - **codBarras** (path): Código de barras del producto (ej: "T-P001-FIL")
    
    **Response EXITOSA:
    ```json
    {
        "id": 15,
        "nombre": "Filtro de Aceite Premium",
        "marca": "Bosch",
        "descripcion": "Filtro de alta calidad...",
        "precio_compra": 150.00,
        "precio_venta": 250.00,
        "stock": 25,
        "imagen_url": "https://example.com/filtro.jpg",
        "cod_barras": "T-P001-FIL",
        "tipo": "producto"
    }
    ```
    
    **Producto NO encontrado:
    ```json
    {
        "detail": "Producto no encontrado"
    }
    ```
    **Status:** `404 Not Found`
    
    **Autenticación:
    No requiere autenticación (público)
    """
    producto = service.get_by_barcode(codBarras)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.get("/{id}", response_model=ProductoResponse, summary="Obtener producto por ID")
def get_producto(id: int, service: ProductoService = Depends(get_producto_service)):
    """
    Obtiene un producto específico por su ID.
    
    **Parámetros:**
    - **id** (path): ID único del producto (ej: 15)
    
    **Response EXITOSA:
    ```json
    {
        "id": 15,
        "nombre": "Filtro de Aceite Premium",
        "marca": "Bosch",
        "descripcion": "Filtro de alta calidad...",
        "precio_compra": 150.00,
        "precio_venta": 250.00,
        "stock": 25,
        "imagen_url": "https://example.com/filtro.jpg",
        "cod_barras": "T-P001-FIL",
        "tipo": "producto"
    }
    ```
    
    **Producto NO encontrado:
    ```json
    {
        "detail": "Producto no encontrado"
    }
    ```
    **Status:** `404 Not Found`
    
    **Autenticación:
    No requiere autenticación (público)
    """
    producto = service.get_by_id(id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{id}", response_model=ProductoResponse, dependencies=[Depends(require_supabase_user)], summary="Actualizar producto")
def update_producto(
    id: int,
    data: ProductoCreate,
    service: ProductoService = Depends(get_producto_service)
):
    """
    Actualiza la información de un producto existente.
    
    **Parámetros:**
    - id: ID del producto a actualizar
    - data: Nuevos datos del producto (mismo formato que crear producto)
    
    **Response exitosa:**
    Retorna el producto actualizado con los nuevos valores.
    
    **Errores:**
    - 404 Not Found: Si el producto no existe
    - 400 Bad Request: Si los datos no cumplen las validaciones
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    producto = service.update_producto(id, data)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/{id}", dependencies=[Depends(require_supabase_user)], summary="Eliminar producto")
def delete_producto(id: int, service: ProductoService = Depends(get_producto_service)):
    """
    Elimina un producto del sistema.
    
    **Parámetros:**
    - id: ID del producto a eliminar
    
    **Response exitosa:**
    ```json
    {
        "detail": "Producto eliminado"
    }
    ```
    
    **Errores:**
    - 404 Not Found: Si el producto no existe
    - 409 Conflict: Si el producto tiene dependencias (ventas, etc.)
    
    **Autenticación:**
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    try:
        producto = service.delete_producto(id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"detail": "Producto eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

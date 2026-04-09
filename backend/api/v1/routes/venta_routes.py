from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.base import SessionLocal
from schemas.venta_schema import VentaCreate, VentaResponse
from services.venta_service import VentaService
from core.auth import require_supabase_user

router = APIRouter(tags=["Ventas"])



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 

def get_venta_service(db: Session = Depends(get_db)) -> VentaService:
    return VentaService(db)

@router.post("/", response_model=VentaResponse, dependencies=[Depends(require_supabase_user)], summary="Registrar nueva venta")
def create_venta(
    data: VentaCreate,
    service: VentaService = Depends(get_venta_service)
):
    """
    Registra una nueva venta en el sistema
    
    Permite registrar ventas de productos con múltiples ítems y actualiza el inventario automáticamente.
    
    **Validaciones:
    - **Cliente**: Mínimo 3 caracteres, máximo 200
    - **Productos**: Debe incluir al menos 1 producto
    - **Cantidad**: Debe ser mayor a 0
    - **Stock**: Verifica que haya suficiente stock disponible
    - **Total**: Se calcula automáticamente según productos y cantidades
    
    **Ejemplo de Request CORRECTO:
    ```json
    {
        "cliente": "Juan Pérez",
        "fecha_venta": "2025-12-04",
        "productos": [
            {
                "producto_id": 15,
                "cantidad": 2,
                "precio_unitario": 250.00
            },
            {
                "producto_id": 14,
                "cantidad": 1,
                "precio_unitario": 400.00
            }
        ]
    }
    ```
    
    **Response EXITOSA:
    ```json
    {
        "id": 42,
        "cliente": "Juan Pérez",
        "fecha_venta": "2025-12-04",
        "total": 900.00,
        "productos": [
            {
                "id": 85,
                "producto_id": 15,
                "cantidad": 2,
                "precio_unitario": 250.00,
                "subtotal": 500.00
            },
            {
                "id": 86,
                "producto_id": 14,
                "cantidad": 1,
                "precio_unitario": 400.00,
                "subtotal": 400.00
            }
        ]
    }
    ```
    
    **Ejemplos de Requests INCORRECTOS:
    
    **1. Stock insuficiente:**
    ```json
    {
        "cliente": "Juan Pérez",
        "productos": [
            {
                "producto_id": 15,
                "cantidad": 100  // Solo hay 25 en stock
            }
        ]
    }
    ```
    **Error:** `400 Bad Request - "Stock insuficiente para el producto"`
    
    **2. Sin productos:**
    ```json
    {
        "cliente": "Juan Pérez",
        "productos": []  // Debe tener al menos 1 producto
    }
    ```
    **Error:** `400 Bad Request - "La venta debe incluir al menos un producto"`
    
    **3. Producto no existe:**
    ```json
    {
        "cliente": "Juan Pérez",
        "productos": [
            {
                "producto_id": 9999,  // No existe
                "cantidad": 1
            }
        ]
    }
    ```
    **Error:** `404 Not Found - "Producto no encontrado"`
    
    **Nota:
    - El stock se descuenta automáticamente al registrar la venta
    - El total se calcula como: Σ(cantidad × precio_unitario)
    - La fecha_venta es opcional (por defecto usa la fecha actual)
    
    **Autenticación:
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    return service.create_venta(data)


@router.get("/", response_model=list[VentaResponse], summary="Listar todas las ventas")
def list_ventas(
    service: VentaService = Depends(get_venta_service)
):
    """
    Obtiene el listado completo de ventas
    
    Retorna todas las ventas registradas con sus productos asociados.
    
    **Response EXITOSA:
    ```json
    [
        {
            "id": 42,
            "cliente": "Juan Pérez",
            "fecha_venta": "2025-12-04",
            "total": 900.00,
            "productos": [
                {
                    "id": 85,
                    "producto_id": 15,
                    "cantidad": 2,
                    "precio_unitario": 250.00,
                    "subtotal": 500.00
                },
                {
                    "id": 86,
                    "producto_id": 14,
                    "cantidad": 1,
                    "precio_unitario": 400.00,
                    "subtotal": 400.00
                }
            ]
        }
    ]
    ```
    
    **Estructura de datos:
    - **id**: Identificador único de la venta
    - **cliente**: Nombre del cliente
    - **fecha_venta**: Fecha de la transacción
    - **total**: Monto total de la venta
    - **productos**: Array de productos vendidos con:
      - **producto_id**: ID del producto en inventario
      - **cantidad**: Unidades vendidas
      - **precio_unitario**: Precio al momento de la venta
      - **subtotal**: cantidad × precio_unitario
    
    **Autenticación:
    No requiere autenticación (público)
    """
    return service.list_ventas()


@router.get("/{id}", response_model=VentaResponse, summary="Obtener venta por ID", description="Busca una venta específica usando su ID único.")
def get_venta_by_id(id: int, service: VentaService = Depends(get_venta_service)):
    """
    Obtiene los detalles de una venta por su ID.

    Args:
        id: ID único de la venta.

    Returns:
        VentaResponse: La venta encontrada.

    Raises:
        HTTPException(404): Si la venta no existe.
    """
    venta = service.get_by_id(id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta


@router.get("/fecha/{fecha}", response_model=list[VentaResponse], summary="Buscar ventas por fecha", description="Busca todas las ventas registradas en una fecha específica.")
def get_ventas_by_fecha(fecha: datetime, service: VentaService = Depends(get_venta_service)):
    """
    Busca ventas por fecha.

    Args:
        fecha: Fecha a buscar.

    Returns:
        list[VentaResponse]: Lista de ventas de esa fecha.
    """
    return service.get_by_fecha(fecha)


@router.delete("/{id}", dependencies=[Depends(require_supabase_user)], summary="Eliminar venta", description="Elimina una venta del sistema.")
def delete_venta(id: int, service: VentaService = Depends(get_venta_service)):
    """
    Elimina una venta por su ID.

    Args:
        id: ID de la venta a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException(404): Si la venta no existe.
    """
    result = service.delete_venta(id)
    if not result:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return {"detail": "Venta eliminada"}

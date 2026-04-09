from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.base import SessionLocal
from schemas.orden_schema import OrdenCreate, OrdenResponse
from services.orden_service import OrdenService
from datetime import date
from core.auth import require_supabase_user

router = APIRouter(tags=["Ordenes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_orden_service(db: Session = Depends(get_db)) -> OrdenService:
    return OrdenService(db)

@router.post("/", response_model=OrdenResponse, dependencies=[Depends(require_supabase_user)], summary="Crear nueva orden de trabajo")
def create_orden(
    data: OrdenCreate,
    service: OrdenService = Depends(get_orden_service)
):
    """
    Registra una nueva orden de trabajo
    
    Las órdenes de trabajo permiten gestionar servicios mecánicos con servicios y empleados asignados.
    
    **Validaciones:
    - **Cliente**: Mínimo 3 caracteres, máximo 200
    - **Placa**: Formato válido de placa vehicular
    - **Estado**: Debe ser uno de: "pendiente", "en_proceso", "completado", "cancelado"
    - **Servicios**: Debe incluir al menos 1 servicio
    - **Empleados**: Puede incluir 0 o más empleados
    
    **Ejemplo de Request CORRECTO:
    ```json
    {
        "cliente": "María González",
        "placa": "ABC-123",
        "vehiculo": "Toyota Corolla 2020",
        "fecha_ingreso": "2025-12-04",
        "fecha_salida": null,
        "estado": "pendiente",
        "observaciones": "Revisión general de motor y cambio de aceite",
        "servicios": [
            {
                "servicio_id": 5,
                "cantidad": 1,
                "precio_unitario": 150.00
            },
            {
                "servicio_id": 12,
                "cantidad": 1,
                "precio_unitario": 80.00
            }
        ],
        "empleados": [
            {
                "empleado_id": 3
            }
        ]
    }
    ```
    
    **Response EXITOSA:
    ```json
    {
        "id": 78,
        "cliente": "María González",
        "placa": "ABC-123",
        "vehiculo": "Toyota Corolla 2020",
        "fecha_ingreso": "2025-12-04",
        "fecha_salida": null,
        "estado": "pendiente",
        "total": 230.00,
        "observaciones": "Revisión general de motor y cambio de aceite",
        "servicios": [
            {
                "id": 120,
                "servicio_id": 5,
                "cantidad": 1,
                "precio_unitario": 150.00,
                "subtotal": 150.00
            },
            {
                "id": 121,
                "servicio_id": 12,
                "cantidad": 1,
                "precio_unitario": 80.00,
                "subtotal": 80.00
            }
        ],
        "empleados": [
            {
                "id": 45,
                "empleado_id": 3
            }
        ]
    }
    ```
    
    **Ejemplos de Requests INCORRECTOS:
    
    **1. Estado inválido:**
    ```json
    {
        "cliente": "María González",
        "estado": "finalizado"  // Debe ser: pendiente, en_proceso, completado, cancelado
    }
    ```
    **Error:** `422 Unprocessable Entity - "Estado no válido"`
    
    **2. Sin servicios:**
    ```json
    {
        "cliente": "María González",
        "servicios": []  // Debe tener al menos 1 servicio
    }
    ```
    **Error:** `400 Bad Request - "La orden debe incluir al menos un servicio"`
    
    **3. Servicio no existe:**
    ```json
    {
        "cliente": "María González",
        "servicios": [
            {
                "servicio_id": 9999  // No existe
            }
        ]
    }
    ```
    **Error:** `404 Not Found - "Servicio no encontrado"`
    
    **Estados disponibles:
    - **pendiente**: Orden creada, esperando inicio
    - **en_proceso**: Trabajo en curso
    - **completado**: Trabajo finalizado
    - **cancelado**: Orden cancelada
    
    **Autenticación:
    Requiere token JWT en header: `Authorization: Bearer <token>`
    """
    return service.create_orden(data)

@router.get("/", response_model=list[OrdenResponse], summary="Listar todas las órdenes de trabajo")
def list_ordens(
    service: OrdenService = Depends(get_orden_service)
):
    """
    Obtiene el listado completo de órdenes de trabajo
    
    Retorna todas las órdenes registradas con servicios y empleados asignados.
    
    **Response EXITOSA:
    ```json
    [
        {
            "id": 78,
            "cliente": "María González",
            "placa": "ABC-123",
            "vehiculo": "Toyota Corolla 2020",
            "fecha_ingreso": "2025-12-04",
            "fecha_salida": null,
            "estado": "pendiente",
            "total": 230.00,
            "observaciones": "Revisión general de motor",
            "servicios": [
                {
                    "id": 120,
                    "servicio_id": 5,
                    "cantidad": 1,
                    "precio_unitario": 150.00,
                    "subtotal": 150.00
                }
            ],
            "empleados": [
                {
                    "id": 45,
                    "empleado_id": 3
                }
            ]
        }
    ]
    ```
    
    **Estructura de datos:
    - **placa**: Identificador del vehículo
    - **vehiculo**: Descripción del vehículo
    - **fecha_ingreso**: Cuándo ingresó el vehículo
    - **fecha_salida**: Cuándo se entregó (puede ser null)
    - **estado**: Estado actual de la orden
    - **servicios**: Array de servicios aplicados
    - **empleados**: Array de empleados asignados
    
    **Autenticación:
    No requiere autenticación (público)
    """
    return service.list_ordens()

@router.get("/{id}", response_model=OrdenResponse, summary="Obtener orden por ID", description="Busca una orden específica usando su ID único.")
def get_orden_by_id(id: int, service: OrdenService = Depends(get_orden_service)):
    """
    Obtiene los detalles de una orden por su ID.

    Args:
        id: ID único de la orden.

    Returns:
        OrdenResponse: La orden encontrada.

    Raises:
        HTTPException(404): Si la orden no existe.
    """
    orden = service.get_by_id(id)
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return orden

@router.get("/fecha/{fecha}", response_model=list[OrdenResponse], summary="Buscar órdenes por fecha", description="Busca todas las órdenes registradas en una fecha específica.")
def get_ordens_by_fecha(fecha: date, service: OrdenService = Depends(get_orden_service)):
    """
    Busca órdenes por fecha.

    Args:
        fecha: Fecha a buscar.

    Returns:
        list[OrdenResponse]: Lista de órdenes de esa fecha.
    """
    return service.get_by_fecha(fecha)

@router.delete("/{id}", dependencies=[Depends(require_supabase_user)], summary="Eliminar orden", description="Elimina una orden del sistema.")
def delete_orden(id: int, service: OrdenService = Depends(get_orden_service)):
    """
    Elimina una orden por su ID.

    Args:
        id: ID de la orden a eliminar.

    Returns:
        dict: Mensaje de confirmación.

    Raises:
        HTTPException(404): Si la orden no existe.
    """
    result = service.delete_orden(id)
    if not result:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return {"detail": "Orden eliminada"}
